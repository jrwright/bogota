"""
Tasks that can be potentially queued for offline runs.
"""
from __future__ import absolute_import
import os.path
import sys
from timeit import default_timer as tick
import logging
info = logging.getLogger(__name__).info
debug = logging.getLogger(__name__).debug
warning = logging.getLogger(__name__).warning

import json
import base64
import redis
from celery import group
import pymc as pm

from .celeryapp import app
from .db import mle_restarts, save_mle_params, _solver, _ensure_jobid
from .mc import multinomial_rvs, find_MAP, posterior_dbname, posterior_chains
import bogota.cfg as cfg

@app.task(name='bogota.tasks._sample_posterior_task', ignore_result=True)
def _sample_posterior_task(predictor_name, pool_name, prior_rvs_expr,
                           iter, burn, thin, chain):
    info("Setting up for chain %d of posterior %s/%s/%s/%d/%d/%d",
         chain, predictor_name, pool_name, prior_rvs_expr, iter, burn, thin)
    # Construct python objects
    preimport(predictor_name)
    preimport(pool_name)
    preimport(prior_rvs_expr)
    pool = eval(pool_name, sys.modules)
    predictor = eval(predictor_name, sys.modules)
    prior_rvs = eval(prior_rvs_expr, sys.modules)
    rvs = multinomial_rvs(pool, predictor, prior_rvs)

    # Connect to backend and create sampler
    fname = posterior_dbname(predictor_name, pool_name, prior_rvs_expr,
                             iter, burn, thin, chain)

    if os.path.isfile(fname):
        db = pm.database.pickle.load(fname, 'a')
        completed = len(db.trace(rvs.keys()[0], chain=None)[:]) if db.chains > 0 else 0
        debug("Loaded '%s' [%d samples in %d chains]", fname, completed, db.chains)
    else:
        db = 'pickle'
        completed = 0

    if completed >= (iter - burn) / thin:
        info("Skipping completed chain %d for posterior %s/%s/%s/%d/%d/%d",
             chain, predictor_name, pool_name, prior_rvs_expr, iter, burn, thin)
        return

    info("Sampling from posterior %s/%s/%s/%d/%d/%d [chain %d]",
         predictor_name, pool_name, prior_rvs_expr, iter, burn, thin, chain)

    # Construct/restore chain
    mc = pm.MCMC(rvs, db=db, dbname=fname, dbmode='a') #TODO compression

    # Find starting point
    info("Optimizing MAP")
    find_MAP(rvs, verbose=False)

    # Burn-in is not restartable
    if burn > 0 and isinstance(db, str):
        info("Sampling 1..%d for burn-in", burn)
        mc.sample(iter=burn, burn=burn, progress_bar=False)
        debug("Checkpointing after burning %d samples", burn)
        mc.db.commit()

    # Take actual samples
    info("Sampling 1..%d (thin=%d)", iter, thin)
    mc.sample(iter=iter, thin=thin, burn=0, progress_bar=False)
    mc.db.close()
    info("Writing results to %s", fname)

def sample_posterior(predictor_name, pool_name, prior_rvs_expr,
                     iter, burn, thin, num_chains=1,
                     queued=None, completed_chains=None):
    """
    Draw samples from a model's posterior distribution, possibly
    asynchronously.
    Returns immediately is the requested chains are completed or queued.
    Returns a pair `queued, completed` to enable caching operation.
    """
    # Return immediately if all chains located
    if completed_chains is None:
        completed_chains = posterior_chains(predictor_name, pool_name, prior_rvs_expr,
                                            iter, burn, thin)
        debug("Completed chains: %s" % completed_chains)

    all_chains = set(range(num_chains))
    if all_chains.issubset(completed_chains):
        debug("All chains completed for posterior %s/%s/%s/%d/%d/%d",
              predictor_name, pool_name, prior_rvs_expr, iter, burn, thin)
        return completed_chains, queued

    # Query for queued chains
    if queued is None:
        queued = posterior_queued_chains()

    queued_chains = queued.get((predictor_name, pool_name, prior_rvs_expr,
                                iter, burn, thin), [])

    subtasks = []

    # Queue up unqueued, uncompleted chains
    for chx in xrange(num_chains):
        if chx in completed_chains or chx in queued_chains:
            continue
        if cfg.app.async:
            info("Queueing chain %d for posterior %s/%s/%s/%d/%d/%d",
                 chx, predictor_name, pool_name, prior_rvs_expr,
                 iter, burn, thin)
            subtasks.append(_sample_posterior_task.s(predictor_name, pool_name,
                                                     prior_rvs_expr,
                                                     iter, burn, thin, chx))
        else:
            _sample_posterior_task(predictor_name, pool_name, prior_rvs_expr,
                                   iter, burn, thin, chx)
        queued_chains.append(chx)

    if cfg.app.async and len(subtasks) > 0:
        g = group(subtasks)
        g.apply_async()

    return completed_chains, queued

def posterior_queued_chains():
    """
    Query for active and reserved restarts and return a dictionary from
    fold-keys to lists of queued restart indices.
    """
    if not cfg.app.async:
        return {}

    ret = {}
    tasks = all_pending_tasks()
    for task in tasks:
        if task['name'] <> 'bogota.tasks._sample_posterior_task':
            continue
        args = task['args']
        key = tuple(args[0:-1])
        val = args[-1]
        ret[key] = ret.get(key, []) + [val]

    return ret

@app.task(name='bogota.tasks._fit_fold_task', ignore_result=True)
def _fit_fold_task(restart_idx, solver_name, pool_name, fold_seed, num_folds, fold_idx,
                   by_game, stratified):
    # Make sure we don't double-work
    completed_restarts = mle_restarts(solver_name, pool_name, [fold_seed], num_folds, 
                                      by_game, stratified)
    if (fold_seed, fold_idx, restart_idx) in completed_restarts:
        info("Skipping completed fold %s/%s/%s/%s/%s/%s/%s/%s",
         restart_idx, solver_name, pool_name, fold_seed, num_folds, fold_idx,
         by_game, stratified)
        return

    info("Fitting fold %s/%s/%s/%s/%s/%s/%s/%s",
         restart_idx, solver_name, pool_name, fold_seed, num_folds, fold_idx,
         by_game, stratified)
    preimport(pool_name)
    preimport(solver_name)
    pool = eval(pool_name, sys.modules)
    if num_folds == 0:
        train_fold = pool
        test_fold = pool
    else:
        if by_game:
            (train_fold, test_fold) = pool.train_fold_gamewise(fold_seed, num_folds, fold_idx, True, stratified)
        else:
            (train_fold, test_fold) = pool.train_fold(fold_seed, num_folds, fold_idx, True)

    solver_inst = _solver(solver_name)
    solver_inst.random_start()
    walltime_s = tick()
    ps = solver_inst.fit(train_fold.log_likelihood,
                         **solver_inst.fit_args)
    walltime = tick() - walltime_s
    train_ll = train_fold.log_likelihood(solver_inst.predict)
    test_ll = test_fold.log_likelihood(solver_inst.predict)
    save_mle_params(train_ll, test_ll, walltime,
                    solver_inst.fittable_parameters, ps, restart_idx,
                    solver_name, pool_name, fold_seed, num_folds, fold_idx,
                    by_game, stratified)

def fit_fold(solver_name, pool_name, fold_seed, num_folds, fold_idx,
             by_game, stratified,
             num_restarts=3, queued=None, completed_restarts=None,
             create_job=True):
    """
    Fit a single fold, possibly asynchronously depending on configuration.
    Returns immediately if all requested restarts are completed or queued.
    Returns a pair `queued, completed_restarts` to enable caching operation.
    """
    if completed_restarts is None:
        completed_restarts = mle_restarts(solver_name, pool_name, [fold_seed], num_folds,
                                          by_game, stratified)

    # Don't bother querying celery if everything is done
    all_restarts = set((fold_seed, fold_idx, rsx) for rsx in range(num_restarts))
    if all_restarts.issubset(completed_restarts):
        debug("All restarts completed for fold %s/%s/%s/%s/%s/%s/%s",
              solver_name, pool_name, fold_seed, num_folds, fold_idx,
              by_game, stratified)
        return completed_restarts, queued

    if queued is None:
        queued = mle_queued_restarts()
    queued_restarts = queued.get((solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified), [])

    subtasks = []

    for rsx in xrange(num_restarts):
        if (fold_seed, fold_idx, rsx) in completed_restarts or rsx in queued_restarts:
            continue
        if cfg.app.async:
            info("Queueing fold %s/%s/%s/%s/%s/%s/%s/%s",
                 rsx, solver_name, pool_name, fold_seed, num_folds, fold_idx,
                 by_game, stratified)
            if create_job:
                _ensure_jobid(None,
                              solver_name, pool_name, fold_seed, num_folds, fold_idx,
                              by_game, stratified)
                create_job = False
            subtasks.append(_fit_fold_task.s(rsx, solver_name, pool_name, fold_seed, num_folds, fold_idx,
                                             by_game, stratified))
        else:
            _fit_fold_task(rsx, solver_name, pool_name, fold_seed, num_folds, fold_idx,
                           by_game, stratified)
        queued_restarts.append(rsx)

    if cfg.app.async and len(subtasks) > 0:
        g = group(subtasks)
        g.apply_async()

    return completed_restarts, queued

def mle_queued_restarts():
    """
    Query for active and reserved restarts and return a dictionary from
    fold-keys to lists of queued restart indices.
    """
    if not cfg.app.async:
        return {}

    tasks = all_pending_tasks()
    ret = {}
    for task in tasks:
        if task['name'] <> 'bogota.tasks._fit_fold_task':
            continue
        args = task['args']
        key = tuple(args[1:])
        val = args[0]
        ret[key] = ret.get(key, []) + [val]

    return ret


def preimport(name):
    """
    Attempt to import all prerequisite modules and packages for `name`.
    """
    dotx = name.find('.')
    try:
        while dotx > 0:
            mod = __import__(name[:dotx])
            info("reload %s", name[:dotx])
            reload(mod) # Use the most recent version
            dotx = name.find('.', dotx+1)
    except ImportError:
        pass

def all_pending_tasks():
    i = app.control.inspect()
    info("Querying active tasks")
    h1 = i.active()
    if h1 is None:
        warning("Cannot query active tasks")
        h1 = {}

    info("Querying reserved tasks")
    h2 = i.reserved()
    if h2 is None:
        warning("Cannot query reserved tasks")
        h2 = {}

    info("Querying queued tasks")
    qt = queued_tasks()

    tasks = qt
    for vs in h1.values() + h2.values():
        for v in vs:
            tasks.append({'name':v['name'], 'args':eval(v['args'])})

    return tasks

def queued_tasks(url=cfg.app.backend):
    r = redis.StrictRedis.from_url(url)
    tasks = []
    for x in r.lrange('celery', 0, -1):
        j = json.loads(x)
        decoded = base64.b64decode(j['body'])
        task = json.loads(decoded)
        tasks.append({'name':task['task'], 'args':task['args']})
    return tasks
