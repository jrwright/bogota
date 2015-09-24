"""
Miscellaneous utilities.
"""
from numbers import Number
import sys
import numpy as np
from warnings import warn

def normalize(ps):
    """
    Return a list of probabilities that have the same proportional relationship
    as ``ps``, but sum to unity.  ``ps`` is assumed to be either a sequence of
    floats or a profile.  If ``ps`` is a profile, then every player's
    probabilities will be normalized.
    """
    if 'game' in dir(ps):
        new_p = ps.game.mixed_strategy_profile()
        for pl in ps.game.players:
            total = sum(ps[pl])
            if total <= 0.0:
                z = 1.0 / len(ps[pl])
                for i in xrange(len(ps[pl])):
                    new_p[pl][i] = z
            else:
                for i in xrange(len(ps[pl])):
                    new_p[pl][i] = ps[pl][i]/total
        return new_p
    else:
        total = sum(ps)
        if total == 1.0:
            return ps
        elif total <= 0.0:
            z = 1.0 / len(ps)
            return [z for p in ps]
        else:
            return [p/total for p in ps]


def proportionally_mix_profiles(weights, profiles):
    """
    Return a new profile that is a mixture of ``profiles`` proportionally to
    the corresponding ``weights``.  If ``profiles`` is shorter than
    ``weights``, then unmatched weights will be ignored.

    If ``weights`` sum to 0, then the profiles will be mixed over uniformly.
    """
    denom=sum(weights[0:len(profiles)])
    new_profile = profiles[0].game.mixed_strategy_profile()
    if denom > 0:
        for (j, ps) in enumerate(apply(zip, profiles)):
            new_profile[j]=sum([w * x / denom for (w, x) in zip(weights, ps)])
    else:
        denom = len(profiles)
        for (j,ps) in  enumerate(apply(zip, profiles)):
            new_profile[j] = sum(x/denom for x in ps)
    return new_profile

def contingency_profile(game, contingency):
    """
    Return a pure strategy profile representing ``contingency`` in ``game``.
    """
    p = zero_profile(game)
    for i,ai in enumerate(contingency):
        p[game.players[i].strategies[ai]] = 1.0
    return p

def fast_contingencies(game, skip=None):
    """
    Fast replacement for `contingencies` generators in games.
    If `skip` is provided, the named player will be skipped.
    ??? Does this only work for nfgs and aggs?
    """
    M = [len(pl.strategies) for pl in game.players]
    N = len(game.players)
    cur = [0] * len(game.players)
    if skip is not None and not isinstance(skip, int):
        skip = skip.number
    last = 0 if skip != 0 else 1

    yield tuple(cur)
    while cur[last] < M[last]:
        for idx in xrange(N-1, -1, -1):
            if idx == skip:
                continue
            cur[idx] += 1
            if cur[idx] < M[idx]:
                yield tuple(cur)
                break
            elif idx != last:
                cur[idx] = 0

# ??? Can we get rid of this and use the `contingencies` member of games instead?
# AGGs seem to now support`contingencies`...
# OTOH, `contingencies` is ludicrously slow.
def action_profiles(game, excludePlayer=None, reuseProfile=None, maxPlayer=None, actions=None):
    """
    Iterate over all action profiles of ``game``, possibly excluding
    ``excludePlayer``.  If ``reuseProfile`` is provided, it will be updated
    in-place; otherwise a new profile will be created and returned.  If
    ``actions`` is provided, it will be updated in place to contain the pure
    strategies corresponding to the "current" profile.
    """
    if maxPlayer is None:
        maxPlayer = len(game.players)-1
    if maxPlayer < 0:
        if (reuseProfile is None) or (not reuseProfile):
            yield game.mixed_strategy_profile()
        else:
            yield reuseProfile
    elif excludePlayer == maxPlayer or excludePlayer == game.players[maxPlayer]:
        for p in action_profiles(game, excludePlayer, reuseProfile, maxPlayer-1, actions):
            yield p
    else:
        pl = game.players[maxPlayer]
        for p in action_profiles(game, excludePlayer, reuseProfile, maxPlayer-1, actions):
            for ai in pl.strategies:
                if reuseProfile is None:
                    q = p.copy()
                else:
                    q = p
                set_pure_strategy(q, ai)
                if actions is not None:
                    actions[pl.number] = ai
                yield q

def set_pure_strategy(profile, strategy):
    """
    Set ``strategy``s entry in ``profile`` to 1.0, and all other strategies of
    its player to 0.0.
    """
    for s in strategy.player.strategies:
        profile[s] = 0.0
    profile[strategy] = 1.0
    return profile

def all_subsets(S):
    if len(S)==0:
        return [[]]
    else:
        head = S[0]
        tail_sets = all_subsets(S[1:])
        return map(lambda x: [head]+x, tail_sets) + tail_sets

def zero_profile(game):
    """
    Return a mixed profile for 'game' with all the entries initialized to 0.
    """
    return make_profile(game, 0.0)

def make_profile(game, profile_probabilities):
    """
    Construct a profile for 'game' from 'profile_probabilities'.
    """
    p = game.mixed_strategy_profile()
    if isinstance(profile_probabilities, Number):
        for i in xrange(len(p)):
            p[i] = profile_probabilities
    elif len(profile_probabilities) == len(p):
        for i in xrange(len(p)):
            p[i]=profile_probabilities[i]
    else:
        raise TypeError("profile_probabilities should be a number or a sequence of length %d" % len(p))

    return p

def marginalize_outcomes(pl, outcomes):
    """
    For 'outcomes' mapping from contingency to probability, return a list of
    marginal probabilities for each of player 'pl's strategies.
    """
    target = [0.0]*len(pl.strategies)
    for c in fast_contingencies(pl.game):
        target[c[pl.number]] += outcomes[c]

    return normalize(target)

def outcomes_joint(profile):
    """
    Return a dict representing a distribution over outcomes, computed by
    taking the cross product of the action probabilities in 'profile'.
    """
    op = dict((c,1.0) for c in fast_contingencies(profile.game))
    for pl in profile.game.players:
        p = profile[pl]
        i = pl.number
        for c in fast_contingencies(profile.game):
            op[c] *= p[c[i]]

    return op

def filter_float(x):
    if np.isfinite(x):
        return x
    elif np.isneginf(x):
        warn("Negative inf value detected")
        return -sys.float_info.max
    elif np.isinf(x):
        warn("Positive inf value detected")
        return sys.float_info.max
    elif np.isnan(x):
        raise ValueError("NaN detected")
    else:
        raise ValueError("Unknown non-finite value '%s'" % x)
