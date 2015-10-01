"""
Tasks that can be potentially queued for offline runs.
"""
from __future__ import absolute_import
from .celeryapp import app
from .db import mle_restarts
import bogota.cfg as cfg

@app.task
def _fit_fold_task(restart_idx, solver_name, pool_name, fold_seed, num_folds, fold_idx,
                   by_game, stratified):
    #TODO
    pass

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

