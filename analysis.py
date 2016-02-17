import sys
import csv
import logging
info = logging.getLogger(__name__).info
debug = logging.getLogger(__name__).debug
warning = logging.getLogger(__name__).warning
from numpy import std, sqrt, log
from scipy.stats import t as tdist
from .db import mle_param, mle_params, mle_restarts, MissingData, index_str, _solver, _create_jobids
from .mc import posterior_samples
from .tasks import fit_fold

def csv_fig(fname, rows,
            row_headings=None, col_headings=None,
            **commonKwArgs):
    missing = 0

    with console_or_file(fname, 'wt') as s:
        f = csv.writer(s, delimiter='\t')
        defaults = {'parameter_name':'LL', 'by_game':True, 'stratified':False,}

        if col_headings:
            cooked_headings = reduce(lambda x,y: x+y, ([ch, '        err'] for ch in col_headings))
            cooked_headings[0] = "# " + cooked_headings[0]
            f.writerow(cooked_headings)

        for row, rh in zip(rows, row_headings or [None]*len(rows)):
            csvrow = []
            for cell in row:
                if isinstance(cell, str):
                    csvrow.append(cell)
                    continue
                args = dict(defaults)
                args.update(commonKwArgs)
                args.update(cell)
                pool_obj = eval(args['pool_name'], sys.modules)
                unif_ll = pool_obj.uniform_log_likelihood() / log(10.0) / (args['num_folds'] or 1)
                try:
                    (avg, err) = mle_parameter_interval(**args)
                    csvrow.append('%.8f' % ((avg/log(10.0))-unif_ll))
                    csvrow.append('%.4f' % (err/log(10.0)))
                except MissingData:
                    missing += 1
                    csvrow.append("None")
                    csvrow.append("None")
            if rh:
                csvrow.append("# " + rh)
            f.writerow(csvrow)
    return missing


def mle_avg_solver(solver_name, pool_name, fold_seeds, num_folds,
                   by_game, stratified):
    """
    Return a solver initialized to the average fitted parameters.
    """
    s = _solver(solver_name)
    for p in s.fittable_parameters:
        val = mle_parameter_interval(p, solver_name, pool_name, fold_seeds, num_folds,
                                     by_game, stratified)
        s.parameters[p] = val

    return s

def mle_solver(solver_name, pool_name, fold_seeds, num_folds, fold_idx,
               by_game, stratified):
    """
    Return a solver initialized to the parameters with the highest training LL.
    """
    params = mle_params(solver_name, pool_name, fold_seeds, num_folds, fold_idx,
                        by_game, stratified)
    s = _solver(solver_name)
    for p in s.fittable_parameters:
        s.parameters[p] = params[p]

    return s

def mle_parameter_interval(parameter_name,
                           solver_name, pool_name, fold_seeds, num_folds,
                           by_game, stratified,
                           p_val=0.05,
                           report_intermediate=True, queue_missing=False):
    missing = 0
    avgs = []

    info("Fetching folds %s/%s/%s/%s/[]/%s/%s",
         solver_name, pool_name, fold_seeds, num_folds,
         by_game, stratified)

    # Fetch restart list for the entire collection in a single shot to speed up
    # the common case where literally every restart needs to be queued
    queued = None
    if queue_missing:
        completed_restarts = mle_restarts(solver_name, pool_name, fold_seeds, num_folds,
                                          by_game, stratified)
    else:
        completed_restarts = []

    if queue_missing == 'fast':
        _create_jobids(solver_name, pool_name, fold_seeds, num_folds, by_game, stratified)

    for fold_seed in fold_seeds:
        data = []
        for fold_idx in xrange(max(num_folds, 1)):
            idx_done = [c for c in completed_restarts if c[0]==fold_seed and c[1]==fold_idx]
            try:
                if queue_missing=='fast':
                    # skip the actual computation of the figure
                    raise MissingData(solver_name, pool_name, fold_seed, num_folds, fold_idx,
                                      by_game, stratified)
                elif not queue_missing or len(idx_done) > 0:
                    data.append(mle_param(parameter_name,
                                          solver_name, pool_name, fold_seed, num_folds, fold_idx,
                                          by_game, stratified))
                else:
                    debug("No restarts done for %s, skipping parameter fetch",
                          index_str(solver_name, pool_name, fold_seed, num_folds, fold_idx,
                                    by_game, stratified))
                    raise MissingData(solver_name, pool_name, fold_seed, num_folds, fold_idx,
                                      by_game, stratified)
            except MissingData as ex:
                if report_intermediate:
                    missing += 1
                else:
                    missing = ex
            if queue_missing and missing:
                completed_restarts, queued = \
                    fit_fold(solver_name, pool_name, fold_seed, num_folds, fold_idx,
                             by_game, stratified,
                             completed_restarts=completed_restarts, queued=queued,
                             create_job=(queue_missing<>'fast'))
        if len(data) > 0:
            avgs.append(sum(data)/len(data))

    if missing and not report_intermediate:
        raise missing
    if missing > 0 and queue_missing <> 'fast':
        warning("%d/%d rows missing for %s" % (missing, max(len(fold_seeds)*num_folds, 1),
                                            index_str(solver_name, pool_name, fold_seeds, num_folds, [], by_game, stratified)))
    if len(avgs) > 1:
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


def posterior_cdf_fig(fname,
                      predictor_name, pool_name, prior_rvs_expr,
                      iter, burn, thin, param_name, prefix=None,
                      key=lambda x:x):
    """
    Generate a file in 'fname' containing an empirical CDF of the specified
    parameter of the specified posterior.  
    """
    xs = posterior_samples(predictor_name, pool_name, prior_rvs_expr,
                           iter, burn, thin, param_name, prefix)
    if len(xs) == 0:
        warning("Skipping '%s', no samples found" % fname)
        return

    with console_or_file(fname, 'wt') as f:
        f.write("# Val\tpct\n")
        for x, pct in cdf(map(key, xs)):
            f.write("%f\t%f\n" % (x, pct))

def cdf(xs):
    xs = sorted(xs)
    n = 1.0 / float(len(xs))

    mass = 0.0
    ret = []
    for x in xs:
        mass += n
        ret.append((x, mass))

    return ret

# =================================== Utils ===================================

class NullExit(object):
    """
    Return a no-op `__exit__` method
    """
    def __init__(self, obj):
        self.obj = obj
    def __enter__(self):
        return self
    def __exit__(self, exception_type, exception_value, traceback):
        pass
    def __getattr__(self, name):
        return getattr(self.obj, name)

def console_or_file(fname, arg=None):
    import sys
    if fname is None:
        return NullExit(sys.stdout)
    elif isinstance(fname, file):
        return NullExit(fname)
    else:
        return open(fname, arg)

def elm(ix):
    """
    Helper key for extracting elements of multidimensional rvs.
    """
    if ix == 0:
        return lambda vec: max(0.0, 1.0 - sum(vec))
    else:
        return lambda vec: vec[ix - 1]
