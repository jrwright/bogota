import sys
import csv
from warnings import warn
from numpy import std, sqrt, log
from scipy.stats import t as tdist
from .db import mle_param, MissingData, index_str
from .tasks import fit_fold

def csv_fig(fname, rows, report_intermediate=False,
            row_headings=None, col_headings=None,
            **commonKwArgs):
    with open(fname, 'wt') as s:
        f = csv.writer(s, delimiter='\t')
        defaults = {'parameter_name':'LL', 'by_game':True, 'stratified':False}
        for row in rows:
            csvrow = []
            for cell in row:
                args = dict(defaults)
                args.update(commonKwArgs)
                args.update(cell)
                pool_obj = eval(args['pool_name'], sys.modules)
                unif_ll = pool_obj.uniform_log_likelihood() / log(10.0) / args['num_folds']
                (avg, err) = mle_parameter_interval(**args)
                csvrow.append('%.8f' % ((avg/log(10.0))-unif_ll))
                csvrow.append('%.4f' % (err/log(10.0)))
            f.writerow(csvrow)

def mle_parameter_interval(parameter_name,
                           solver_name, pool_name, fold_seeds, num_folds,
                           by_game, stratified,
                           p_val=0.05, queue_missing=False):
    missing_count = 0
    avgs = []

    # Caching for restarts
    queued = None
    completed_restarts = None

    for fold_seed in fold_seeds:
        data = []
        for fold_idx in xrange(max(num_folds, 1)):
            try:
                data.append(mle_param(parameter_name,
                                      solver_name, pool_name, fold_seed, num_folds, fold_idx,
                                      by_game, stratified))
            except MissingData:
                missing_count += 1
            if queue_missing:
                completed_restarts, queued = \
                    fit_fold(solver_name, pool_name, fold_seed, num_folds, fold_idx,
                             by_game, stratified,
                             completed_restarts=completed_restarts, queued=queued)
        if len(data) > 0:
            avgs.append(sum(data)/len(data))

    if missing_count > 0:
        warn("%d/%d rows missing for %s" % (missing_count, max(len(fold_seeds)*num_folds, 1),
                                            index_str(solver_name, pool_name, fold_seeds, num_folds, "", by_game, stratified)))
    if len(avgs) > 0:
        return tdist_confidence_interval(avgs, p_val)
    else:
        raise MissingData(solver_name, pool_name, fold_seeds, num_folds, None, by_game, stratified)

def tdist_confidence_interval(avgs, p_val):
    """
    Return ``(a,e)``, where ``a`` is the average of ``avgs``, and ``e`` is the
    magnitude of an error bar for a ``(1-p_val)`` confidence interval.
    """
    n = float(len(avgs))
    assert n > 1
    avg = sum(avgs) / n
    q = 1.0 - (p_val / 2.0)
    width = tdist.ppf(q, n-1) / sqrt(n)
    return (avg, width*std(avgs))
