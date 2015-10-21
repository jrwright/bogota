"""
Tasks that can be potentially queued for offline runs.
"""
from __future__ import absolute_import
import sys
from logging import info, debug
from timeit import default_timer as tick
from .celeryapp import app
from .db import mle_restarts, save_mle_params, _solver
import bogota.cfg as cfg

@app.task(name='bogota.tasks._fit_fold_task')
def _fit_fold_task(restart_idx, solver_name, pool_name, fold_seed, num_folds, fold_idx,
                   by_game, stratified):
    # Make sure we don't double-work
    completed_restarts = mle_restarts(solver_name, pool_name, fold_seed, num_folds, fold_idx,
                                      by_game, stratified)
    if restart_idx in completed_restarts:
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
             num_restarts=3, queued=None, completed_restarts=None):
    """
    Fit a single fold, possibly asynchronously depending on configuration.
    Returns immediately if all requested restarts are completed or queued.
    Returns a pair `queued, completed_restarts` to enable caching operation.
    """
    if completed_restarts is None:
        completed_restarts = mle_restarts(solver_name, pool_name, fold_seed, num_folds, fold_idx,
                                          by_game, stratified)

    # Don't bother querying celery if everything is done
    if set(range(num_folds)).issubset(completed_restarts):
        debug("All restarts completed for fold %s/%s/%s/%s/%s/%s/%s",
              solver_name, pool_name, fold_seed, num_folds, fold_idx,
              by_game, stratified)
        return completed_restarts, queued

    if queued is None:
        queued = mle_queued_restarts()
    queued_restarts = queued.get((solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified), [])

    for rsx in xrange(num_restarts):
        if rsx in completed_restarts or rsx in queued_restarts:
            continue
        if cfg.app.async:
            info("Queueing fold %s/%s/%s/%s/%s/%s/%s/%s",
                 rsx, solver_name, pool_name, fold_seed, num_folds, fold_idx,
                 by_game, stratified)
            _fit_fold_task.delay(rsx, solver_name, pool_name, fold_seed, num_folds, fold_idx,
                                 by_game, stratified)
        else:
            _fit_fold_task(rsx, solver_name, pool_name, fold_seed, num_folds, fold_idx,
                           by_game, stratified)
        queued_restarts.append(rsx)

    return completed_restarts, queued

def mle_queued_restarts():
    """
    Query for active and reserved restarts and return a dictionary from
    fold-keys to lists of queued restart indices.
    """
    if not cfg.app.async:
        return {}

    i = app.control.inspect()
    h1 = i.active()
    h2 = i.reserved()

    assert h1 is not None and h2 is not None, "Cannot query workers"

    ret = {}
    for h in [h1,h2]:
        for tasks in h.values():
            for task in tasks:
                if task['name'] <> 'bogota.tasks._fit_fold_task':
                    continue
                key = tuple(task['args'][1:])
                val = task['args'][0]
                ret.get(key, []).append(val)

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
