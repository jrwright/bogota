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
        defaults = {'parameter_name':'LL', 'by_game':True, 'stratified':False, 'uncooked':False}

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
                uncooked = args['uncooked']
                del args['uncooked']
                pool_obj = eval(args['pool_name'], sys.modules)
                try:
                    (avg, err) = mle_parameter_interval(**args)

                    if not uncooked:
                        if args['parameter_name'] == 'LL':
                            unif_ll = pool_obj.uniform_log_likelihood() / log(10.0) / (args['num_folds'] or 1)
                            avg = (avg / log(10.0)) - unif_ll
                            err = err / log(10.0)
                        elif args['parameter_name'] == 'TRAIN_LL':
                            num_train = args['num_folds'] - 1 if args['num_folds'] > 1 else 1
                            unif_ll = pool_obj.uniform_log_likelihood() / log(10.0) / num_train
                            avg = (avg / num_train / log(10.0)) - unif_ll
                            err = err / num_train / log(10.0)

                    csvrow.append('%.8f' % avg)
                    csvrow.append('%.4f' % err)
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
                           iter, burn, thin, param_name, key, prefix)
    if len(xs) == 0:
        warning("Skipping '%s', no samples found" % fname)
        return
    else:
        debug("Writing %d-sample CDF to '%s'", len(xs), fname)

    with console_or_file(fname, 'wt') as f:
        f.write("# Val\tpct\n")
        for x, pct in cdf(xs):
            f.write("%f\t%f\n" % (x, pct))

def cdf(xs):
    """
    WARNING: Sorts destructively!
    """
    xs.sort()
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

# =========================== reusable main function ==========================

def main(mod):
    """
    Main function for use in figure-generating scripts.

    Args:
      mod: dictionary of the main-module's symbols.

    Usage:
      Place the following code at the end of the script:
        ```
        if __name__ == '__main__':
            bogota.analysis.main(globals())
        ```

      Every function named `fig_*` will be run in unspecified order.  These
      functions will be passed a dictionary containing keywords parsed from the
      command-line; this dictionary can be passed directly to analysis
      functions such as `csv_fig`:
        ```
        def fig_foo(args):
            return csv_fig('foo.dat', [...], **args)
        ```

      The module documentation string will be used as the script documentation.
    """
    def int_range_or_list(string):
        ints = []
        strs = string.split(',')
        for s in strs:
            dash = s.find('-')
            if dash >= 0:
                L = int(s[:dash])
                R = int(s[dash+1:])
                ints += range(L, R+1)
            else:
                ints.append(int(s))
        return ints
    def yesno(string):
        s = string.lower()
        if s is False or s=='no' or s=='false' or s=='0':
            return False
        elif s is True or s=='yes' or s=='true' or s=='1':
            return True
        else:
            raise ValueError("Unrecognized bool arg '%s'", s)
    def yesnofast(string):
        if string.lower() == 'fast':
            return 'fast'
        else:
            return yesno(string)

    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=mod['__doc__'])
    parser.add_argument('--fold-seeds', type=int_range_or_list,
                        help="Seeds to use when creating partitions",
                        default=None if 'FOLD_SEEDS' not in mod else mod['FOLD_SEEDS'])
    parser.add_argument('--num-folds', type=int,
                        help="Number of folds per partition",
                        default=None if 'NUM_FOLDS' not in mod else mod['NUM_FOLDS'])
    gr = parser.add_mutually_exclusive_group()
    gr.add_argument('--by-game', type=yesno, nargs='?', const=True,
                        help="Divide at the level of games rather than observations",
                        default=None if 'BY_GAME' not in mod else mod['BY_GAME'])
    gr.add_argument('--no-by-game', action='store_false', dest='by_game')
    gr = parser.add_mutually_exclusive_group()
    gr.add_argument('--stratified',  type=yesno, nargs='?', const=True,
                        help="Stratify by original dataset",
                        default=None if 'STRATIFIED' not in mod else mod['STRATIFIED'])
    gr.add_argument('--no-stratified', action='store_false', dest='stratified')
    gr = parser.add_mutually_exclusive_group()
    gr.add_argument('--queue-missing', type=yesnofast, nargs='?', const=True, dest='queue_missing',
                    help="Whether to queue missing restarts",
                    default=False if 'QUEUE_MISSING' not in mod else mod['QUEUE_MISSING'])
    gr.add_argument('--no-queue-missing', action='store_false', dest='queue_missing')
    gr.add_argument('--queue-fast', '--fast', action='store_const', const='fast', dest='queue_missing',
                    help="Whether to queue missing restarts in 'fast' mode (i.e., cells will not be calculated).  Overrides --queue-missing.",
                    default='fast' if 'QUEUE_MISSING' in mod and mod['QUEUE_MISSING'] == 'fast' else None)
    gr = parser.add_mutually_exclusive_group()
    gr.add_argument('--report-intermediate', type=yesno, nargs='?', const=True,
                        help="Report intermediate values based on incomplete fits",
                        default=False if 'REPORT_INTERMEDIATE' not in mod else mod['REPORT_INTERMEDIATE'])
    gr.add_argument('--no-report-intermediate', action='store_false', dest='report_intermediate')
    parser.add_argument('--debug', action='store_true',
                        help="Set logging level to debug")
    kwargs = dict(cell for cell in parser.parse_args()._get_kwargs() if cell[1] is not None)

    if 'logging' not in mod:
        import logging
        if 'debug' in kwargs and kwargs['debug']:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)
        logging.info("Starting up")
        logging.debug("Debugging enabled")

    elif 'debug' in kwargs and kwargs['debug']:
        mod['logging'].getLogger().setLevel(mod['logging'].DEBUG)

    if 'debug' in kwargs:
        del kwargs['debug']

    fig_fns = [ mod[n] for n in mod if n[:4] == 'fig_' ]
    missing = 0
    for fn in fig_fns:
        info("RUNNING FIGURE %s", fn.__name__)
        missing += fn(kwargs)

    if kwargs['queue_missing'] <> 'fast':
        info("%d cells missing in total" % missing)
