"""
Tasks that can be potentially queued for offline runs.
"""
from __future__ import absolute_import
import sys
from timeit import default_timer as tick
from .celeryapp import app
from .db import mle_restarts, save_mle_params, _solver
import bogota.cfg as cfg

@app.task
def _fit_fold_task(restart_idx, solver_name, pool_name, fold_seed, num_folds, fold_idx,
                   by_game, stratified):
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
             num_restarts=3, completed_restarts=None):
    """
    Fit a single fold, possibly asynchronously depending on configuration.
    If `completed_restarts` is non-None, it should be a
    list of 0-based restart indices that have already completed.
    Returns immediately if all requested restarts are completed or queued.
    """
    if completed_restarts is None:
        completed_restarts = mle_restarts(solver_name, pool_name, fold_seed, num_folds, fold_idx,
                                          by_game, stratified)
    queued_restarts = [] #TODO

    for rsx in xrange(num_restarts):
        if rsx in completed_restarts or rsx in queued_restarts:
            continue
        if cfg.async:
            _fit_fold_task.delay(rsx, solver_name, pool_name, fold_seed, num_folds, fold_idx,
                                 by_game, stratified)
        else:
            _fit_fold_task(rsx, solver_name, pool_name, fold_seed, num_folds, fold_idx,
                           by_game, stratified)

