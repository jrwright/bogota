"""
Support for Bayesian estimation using pymc (version 2).
"""
import hashlib
import numpy as np
import pymc as pm

def multinomial_rvs(pool, predictor, fittable_parameters, fixed_parameters={}, debug=False):
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

    'fixed_parameters' should be a dict mapping from argument name to a value;
    these values will not be fit.  (This is a convenience parameter to make
    currying unnecessary).

    When 'debug' is True, prints the parameters that will be assigned to every
    observation variable before assigning them.

    Returns a dictionary from variable name to variable of all the fittable
    parameters, plus a new set of variables called `obs`.
    """
    rvs = dict((str(p), p) for p in fittable_parameters)
    args = dict(fixed_parameters.items() + rvs.items())

    dnps = []
    for wp in pool.weighted_profiles:
        dnp_ = wp.denormalized_profile()
        for pl in wp.game.players:
            if sum(dnp_[pl]) > 0:
                dnps.append(dnp_[pl])

    @pm.deterministic
    def prediction(args = args):
        return [predictor(dnp.player.game, **args)[dnp.player] for dnp in dnps]

    if debug:
        for (idx, dnp) in enumerate(dnps):
            print "observations_%d" % idx, sum(dnp), prediction[idx].value, dnp

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
                     iter, burn, thin, chain=None):
    """
    Return a filename suitable for storing sampling results.
    """
    m = hashlib.md5(prior_rvs_expr)
    if chain:
        fname = "%s__%s__%s__%d_%d_%d__%s.hdf5" % (predictor_name, pool_name,
                                                   m.hexdigest()[0:4],
                                                   iter, burn, thin, chain)
    else:
        fname = "%s__%s__%s__%d_%d_%d.hdf5" % (predictor_name, pool_name,
                                               m.hexdigest()[0:4],
                                               iter, burn, thin)
    return fname

