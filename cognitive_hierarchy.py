"""
Implement cognitive hierarchy-based solution concepts.
"""
import numpy as np
import scipy.stats
from bogota.solver import solver
from bogota.utils import proportionally_mix_profiles, normalize

# ============================= Solution concepts =============================

@solver(['a1', 'a2', 'lam1', 'lam2', 'lam1_2'],
        parameter_bounds={'lam1':(0.0,None), 'lam2':(0.0,None), 'lam1_2':(0.0,None)},
        simplex_parameters=[('a1', 'a2')])
def qlk(game, a1, a2, lam1, lam2, lam1_2, l0_prediction=None):
    if l0_prediction is None:
        l0_prediction = game.mixed_strategy_profile()
    a0 = max(0.0, 1.0-a1-a2)

    l1_prediction = logit_br_all(l0_prediction, lam1)
    l1_2_prediction = logit_br_all(l0_prediction, lam1_2)
    l2_prediction = logit_br_all(l1_2_prediction, lam2)

    return proportionally_mix_profiles([a0, a1, a2],
                                       [l0_prediction,
                                        l1_prediction,
                                        l2_prediction])

@solver(['a1', 'a2', 'eps1', 'eps2'],
        parameter_bounds={'eps1':(0.0,1.0), 'eps2':(0.0,1.0)},
        simplex_parameters=[('a1', 'a2')])
def lk(game, a1, a2, eps1, eps2, lam=1000.0, l0_prediction=None):
    unif = game.mixed_strategy_profile()
    if l0_prediction is None:
        l0_prediction = game.mixed_strategy_profile()
    a0 = max(0.0, 1.0-a1-a2)

    l1 = logit_br_all(l0_prediction, lam)
    l1_prediction = proportionally_mix_profiles([eps1, 1.0-eps1], [unif, l1])

    l2 = logit_br_all(l1, lam)
    l2_prediction = proportionally_mix_profiles([eps2, 1.0-eps2], [unif, l2])

    return proportionally_mix_profiles([a0, a1, a2],
                                       [l0_prediction,
                                        l1_prediction,
                                        l2_prediction])

@solver(['tau'],
        parameter_bounds={'tau':(0.0, None)})
def poisson_ch(game, tau, l0_prediction=None, top_level=7):
    return quantal_ch(game, poisson_alphas(tau, top_level),
                      1000.0, l0_prediction)

@solver(['a1', 'a2', 'a3', 'a4', 'a5', 'lam'],
        parameter_bounds={'a1':(0.0,1.0), 'a2':(0.0,1.0), 'a3':(0.0,1.0), 'a4':(0.0,1.0), 'a5':(0.0,1.0), 'lam':(0.0,None)},
        simplex_parameters=[('a1', 'a2', 'a3', 'a4', 'a5')])
def qch5(game, a1, a2, a3, a4, a5, lam):
    a0 = 1.0 - sum([a1,a2,a3,a4,a5])
    return quantal_ch(game, [a0,a1,a2,a3,a4,a5], lam)


@solver(['eps', 'tau', 'lam'],
        parameter_bounds={'eps':(0.0,1.0), 'tau':(0.0, None), 'lam':(0.0, None)})
def spike_poisson_qch(game, eps, tau, lam, l0_prediction=None, top_level=7, per_level=False):
    """
    Returns a quantal cognitive hierarchy prediction for ``game`` where the
    levels are assumed to be distributed according to a 'spike-Poisson'
    distribution (from Wright & Leyton-Brown 2013) with parameters ``eps`` and
    ``tau``. See `quantal_ch`.
    """
    return quantal_ch(game, normalize(spike_poisson_alphas(eps, tau, top_level)), lam, l0_prediction, per_level)

@solver(['tau', 'lam'],
        parameter_bounds={'tau':(0.0, None), 'lam':(0.0, None)})
def poisson_qch(game, tau, lam, l0_prediction=None, top_level=7, per_level=False):
    """
    Returns a quantal cognitive hierarchy prediction for ``game`` where the
    levels are assumed to be distributed according to a Poisson distribution
    with intensity parameter ``tau``.  See `quantal_ch`.
    """
    return quantal_ch(game, poisson_alphas(tau, top_level),
                      lam, l0_prediction, per_level)

def quantal_ch (game, alphas, lam, l0_prediction=None, per_level=False):
    """
    Returns a predicted strategy profile for ``game``, assuming that each agent is
    level k with probability ``alphas[k]``, and logit responds with precision
    ``lam``.  If ``alphas`` has length k, then probability of level k and
    higher agents is considered to be 0.  ``l0_prediction`` is a
    `MixedStrategyProfile` representing the prediction of how a profile of
    level-0 agents would act.  If it is not provided, then the uniform
    distribution is assumed.
    """
    lams = [lam] * (len(alphas) - 1)
    return heterogenous_quantal_ch(game, alphas, lams, l0_prediction, per_level)

def heterogenous_quantal_ch(game, alphas, lams, l0_prediction=None, per_level=False):
    assert len(lams) == len(alphas) - 1
    if l0_prediction is None:
        l0_prediction = game.mixed_strategy_profile()
    level_profiles = [l0_prediction]
    accum = alphas[0]
    belief = l0_prediction
    for k,lam in zip(xrange(1, len(alphas)), lams):
        qbr = logit_br_all(belief, lam)
        level_profiles.append(qbr)
        belief = proportionally_mix_profiles([accum, alphas[k]], [belief, qbr])
        accum = accum + alphas[k]
    if per_level:
        return level_profiles
    else:
        return proportionally_mix_profiles(alphas, level_profiles)

# =========================== distribution utilities ==========================

def spike_poisson_alphas(eps, tau, top_level=7):
    """
    Return a list of _unnormalized_ alphas for a "Spike-Poisson" distribution,
    with parameters ``eps`` and ``tau``, truncated at ``top_level``

    A Spike-Poisson distribution is an (eps, 1.0-eps) mixture between a
    point-mass at 0 and a Poisson distribution with mean ``tau``.
    """
    assert eps >= 0.0
    assert tau >= 0.0
    if tau == 0.0 or eps == 1.0:
        return [1.0] + ([0.0] * top_level)
    nonzero = 1.0-eps
    alphas = [nonzero * scipy.stats.poisson.pmf(k, tau) for k in xrange(0, top_level+1)]
    alphas[0] += eps
    return alphas

def poisson_alphas(tau, top_level=7):
    if tau <= 0.0:
        return [1.0] + ([0.0]*top_level)
    return [scipy.stats.poisson.pmf(k, tau) for k in xrange(0, top_level+1)]


# =============================== Logit response ==============================

def logit_br_all(profile, lam):
    """
    Return a new mixed profile in which each agent logit responds to
    ``profile`` with precision ``lam``.
    """
    new_profile = profile.game.mixed_strategy_profile()
    for p in profile.game.players:
        logit_br(profile, lam, p, new_profile)
    return new_profile

def logit_br(profile, lam, agent, new_profile=None):
    """
    Return a logit response for ``agent`` to ``profile`` with precision
    ``lam``.
    """
    if new_profile is None:
        new_profile=profile.game.mixed_strategy_profile()
    ps = multi_logit(lam, profile.strategy_values(agent))
    new_strategy = new_profile[agent]
    for j in xrange(len(new_strategy)):
        new_strategy[j] = ps[j]
    return new_strategy

def multi_logit(lam, xs):
    """
    Return a normalized array of probabilities, where each is proportional to
    $exp(``lam``*``x``)$.
    """
    if not isinstance(xs, np.ndarray) or xs.dtype <> np.dtype('float64'):
        xs = np.asarray(xs, dtype='float64')
    xs *= lam
    max_x = max(xs)
    xs = np.exp(xs - max_x)
    xs /= np.sum(xs)
    return xs
