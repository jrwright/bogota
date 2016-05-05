"""
Support for Bayesian estimation using pymc (version 2).
"""
import glob
import hashlib
import itertools
import logging
debug = logging.getLogger(__name__).debug

import numpy as np
import pymc as pm

def multinomial_rvs(pool, predictor, fittable_parameters, fixed_parameters={}):
    """
    Construct a pymc model of the data in 'pool' based on the function
    'predictor'.  The observation counts in each weighted profile are assumed
    to be iid draws from a multinomial whose parameters are the prediction by
    'predictor' for the corresponding game.

    'predictor' should be a function whose first positional argument is a game,
    which returns a distribution over the actions of the game.  The other
    arguments will be set based on 'fittable_parameters' and 'fixed_parameters.'

    'fittable_parameters' should be a list of pymc random variables, with
    names that correspond to the appropriate arguments of 'predictor'.
    **WARNING**: These variables will be destructively updated!
    (This may optionally be a dictionary, in which case the variables' names
    will be ignored and their dictionary keys will be used instead.)

    'fixed_parameters' should be a dict mapping from argument name to a value;
    these values will not be fit.  (This is a convenience parameter to make
    currying unnecessary).

    Returns a dictionary from variable name to variable of all the fittable
    parameters, plus a new set of variables called `obs`.
    """
    if isinstance(fittable_parameters, dict):
        rvs = dict(fittable_parameters.items())
    else:
        rvs = dict((str(p), p) for p in fittable_parameters)
    args = dict(fixed_parameters.items() + rvs.items())

    debug("Constructing RVs for predictor '%s'", predictor)
    debug("fittable_parameters=%s", fittable_parameters)

    dnps = []
    for wp in pool.weighted_profiles:
        dnp_ = wp.denormalized_profile()
        for pl in wp.game.players:
            if sum(dnp_[pl]) > 0:
                dnps.append(dnp_[pl])

    @pm.deterministic
    def prediction(args = args):
        return [predictor(dnp.player.game, **args)[dnp.player] for dnp in dnps]

    obs = [ pm.Multinomial("observations_%d" % idx,
                           n=sum(dnp),
                           p=prediction[idx],
                           value=dnp,
                           observed=True) \
            for (idx, dnp) in enumerate(dnps) ]
    rvs['obs'] = obs
    return rvs


def find_MAP(rvs, restarts = 10,
             method='fmin_powell', iterlim=1000, tol=0.0001, verbose=1):
    """
    Find the maximum a posteriori (MAP) estimate of the model specified by
    random variables `rvs` using `restarts` random restarts.  This is a
    simple wrapper around [pymc.MAP] that performs random restarts and returns
    the best setting.

    Additional parameters are passed through as arguments to [pymc.MAP.fit].
    """
    stochastic = []
    simple = []
    for j in rvs:
        try:
            j.random()
            if j.observed == False:
                stochastic.append(j)
            else:
                simple.append(j)
        except AttributeError:
            simple.append(j)

    m = pm.MAP(rvs)
    best_values = []
    maxm = -np.inf
    for j in stochastic:
        best_values.append(0)

    for r in xrange(restarts):
        m.fit(method=method, verbose=verbose, iterlim=iterlim, tol=tol)
        if m.logp > maxm:
            maxm = m.logp
            for j in xrange(len(stochastic)):
                best_values[j] = stochastic[j].value
        for j in xrange(len(stochastic)):
            stochastic[j].random()

    for j in xrange(len(stochastic)):
        stochastic[j].value = best_values[j]


# =================================== Utils ===================================

class UniformSimplex(pm.Dirichlet):
    """
    An extension of `pymc.Dirichlet` that represents a uniform distribution
    over the *closed* 'k'-dimensional simplex; that is, the boundary is also
    assigned positive probability.
    """
    def __init__(self, name, **args):
        if 'theta' in args:
            raise TypeError("Keyword 'theta' not recognized; use 'k' instead")
        if 'k' not in args:
            raise ValueError("Keyword 'k' must be provided")
        _args = dict(args)
        del _args['k']
        _args['theta'] = np.ones(args['k'])
        super(UniformSimplex, self).__init__(name, **_args)

    @property
    def logp(self):
        try:
            if min(self.value) < 0.0 or max(self.value) > 1.0 or sum(self.value) > 1.0:
                raise pm.ZeroProbability()
            return self._cached_logp
        except AttributeError:
            self._cached_logp = super(UniformSimplex, self).logp
            return self._cached_logp


def posterior_dbname(predictor_name, pool_name, prior_rvs_expr,
                     iter, burn, thin, chain=None, prefix=None):
    """
    Return a filename suitable for storing sampling results.
    """
    m = hashlib.md5(prior_rvs_expr)
    if chain is None:
        fname = "%s__%s__%s__%d_%d_%d.pickle" % (predictor_name, pool_name,
                                                 m.hexdigest()[0:4],
                                                 iter, burn, thin)
    else:
        fname = "%s__%s__%s__%d_%d_%d__%s.pickle" % (predictor_name, pool_name,
                                                     m.hexdigest()[0:4],
                                                     iter, burn, thin, chain)
    if prefix is not None:
        fname = "%s/%s" % (prefix, fname)
    return fname

def posterior_dbs(predictor_name, pool_name, prior_rvs_expr,
                  iter, burn, thin, prefix=None):
    """
    Returns a dictionary mapping from chain id to database object for the
    specified posterior.  If 'prefix' is specified it will be prepended to the
    database name.  Empty dbs are skipped.

    *NOTE* Closing the returned database is the caller's responsibility!
    """
    pattern = posterior_dbname(predictor_name, pool_name, prior_rvs_expr,
                               iter, burn, thin, '*', prefix)
    fnames = glob.glob(pattern)
    debug("%d files match '%s'" % (len(fnames), pattern))
    ret = {}

    EXTLEN = len('.pickle')
    for fname in fnames:
        ix = fname[:-EXTLEN].rfind('_')
        chain = int(fname[ix+1:-EXTLEN])

        db = pm.database.pickle.load(fname)
        if db.chains > 0:
            ret[chain] = db

    return ret

def posterior_chains(predictor_name, pool_name, prior_rvs_expr,
                     iter, burn, thin, prefix=None, target=None):
    """
    Return a list of ids for all the chains for the specified posterior that
    are "completed" (i.e., have all requested samples completed).  If 'target'
    is specified, then it will be used as the notion of completed; otherwise
    iter/thin.
    """
    if target is None:
        target = iter / thin
    h = posterior_dbs(predictor_name, pool_name, prior_rvs_expr,
                        iter, burn, thin, prefix)
    ret = []
    for chain, db in h.items():
        k = db.trace_names[0][0]
        completed = len(db.trace(k, chain=None)[:])
        db.close()
        debug("chain %s: %d/%d completed" % (chain, completed, target))
        if completed >= target:
            ret.append(chain)

    return ret

def posterior_samples(predictor_name, pool_name, prior_rvs_expr,
                      iter, burn, thin, param_name, key, prefix=None):
    """
    Return an array of all samples for the specified parameter of the specified
    posterior.
    """
    h = posterior_dbs(predictor_name, pool_name, prior_rvs_expr,
                      iter, burn, thin, prefix)
    ret = []
    sz = 0
    for db in h.values():
        tr = db.trace(param_name, chain=None)
        sz += tr.length()
        ret = itertools.chain(ret, (key(x) for x in tr if np.isfinite(key(x))))
        db.close()

    return np.fromiter(ret, np.float, sz)
