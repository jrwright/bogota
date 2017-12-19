"""
Linear level-0 meta-model.
"""
from numpy import inf
from bogota.cognitive_hierarchy import multi_logit
from bogota.utils import action_profiles, normalize, proportionally_mix_profiles, zero_profile, fast_contingencies

# ================================ Meta-models ================================

def weighted_linear_l0_prediction(features, weights, game, applicable_only, normalize_activations=True, eps=1e-6):
    """
    Return a mixed profile representing a level-0 prediction for ``game``
    computed by taking a normalized weighted average of ``features`` according
    to ``weights``.
    """
    ws = []
    fps = []
    for (w,f) in zip(weights, features):
        fp = f(game)
        if normalize_activations:
            fp = normalize(fp)
            if '_inv' in dir(f) and f._inv:
                for i in xrange(len(fp)):
                    fp[i] = 1.0 - fp[i]
                fp = normalize(fp)
        elif '_inv' in dir(f) and f._inv:
            for i in xrange(len(fp)):
                fp[i] = 1.0 / (fp[i] + eps)
                
        if f is constant_binary or applicable_only is False or applicable(fp):
            ws.append(w)
            fps.append(fp)

    mixed = proportionally_mix_profiles(ws, fps)
    return normalize(mixed)

def applicable(fp):
    """
    Return True if ``fp`` differs between some pair of actions for some agent.
    """
    for pl in fp.game.players:
        si = fp[pl]
        for i in xrange(len(si)):
            if si[i] != si[0]:
                return True
    return False

def logit_l0_prediction(features, weights, link_lam, game, normalize_activations=False):
    """
    Take the weighted sum of activations from ``features``, and return a
    prediction using a logit link.
    """
    # By default weight everything equally
    if weights is None:
        weights = [1.0 / len(features)] * len(features)

    activations = zero_profile(game)
    for (w,f) in zip(weights, features):
        fp = f(game)
        if normalize_activations:
            fp = normalize(fp)
        if '_inv' in dir(f) and f._inv:
            for i in xrange(len(fp)):
                fp[i] = -fp[i]
        for i in xrange(len(activations)):
            activations[i] += w*fp[i]

    new_p = game.mixed_strategy_profile()
    for pl in game.players:
        q = multi_logit(link_lam, activations[pl])
        pi = new_p[pl]
        for i in xrange(len(pi)):
            pi[i] = q[i]

    return new_p

# ================================== Features =================================

# Copied from <http://code.activestate.com/recipes/578231-probably-the-fastest-memoization-decorator-in-the-/>
def memodict(f):
    """ Memoization decorator for a function taking a single argument """
    class memodict(dict):
        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret
    m = memodict()
    def fn(arg):
        return m.__getitem__(arg).copy()
    fn.__name__ = f.__name__
    return fn

@memodict
def constant_binary(game):
    """
    Every action is equally salient.
    """
    p = game.mixed_strategy_profile()
    for i in xrange(len(p)):
        p[i] = 1.0
    return p

# ------------------------------- Raw payoffs -------------------------------

@memodict
def max_payoff(game):
    """
    The max payoff of each action.
    """
    m = game.mixed_strategy_profile()
    for i in xrange(len(m)):
        m[i] = -inf
    for pl in game.players:
        for p in action_profiles(game, pl, game.mixed_strategy_profile()):
            vs = p.strategy_values(pl)
            for i in xrange(len(vs)):
                m[pl][i] = max(vs[i], m[pl][i])
    return m

@memodict
def min_payoff(game):
    """
    The min payoff of each action.
    """
    m = game.mixed_strategy_profile()
    for i in xrange(len(m)):
        m[i] = inf
    for pl in game.players:
        for p in action_profiles(game, pl, game.mixed_strategy_profile()):
            vs = p.strategy_values(pl)
            for i in xrange(len(vs)):
                m[pl][i] = min(vs[i], m[pl][i])
    return m


@memodict
def relative_max_regret(game, digits=6):
    """
    The max regret for each action, normalized by the player's maximum possible
    payoff.
    """
    mx = dict((pl, -inf) for pl in game.players)
    r = game.mixed_strategy_profile()
    for i in xrange(len(r)):
        r[i] = 0.0
    for pl in game.players:
        for p in action_profiles(game, pl, game.mixed_strategy_profile()):
            vs = p.strategy_values(pl)
            M = reduce(max, vs)
            mx[pl] = max(mx[pl], M)
            for i in xrange(len(vs)):
                r[pl][i] = max(r[pl][i], round(M-vs[i], digits))

    for pl in game.players:
        for ix in xrange(len(r[pl])):
            r[pl][ix] = round(r[pl][ix] / mx[pl], digits)

    return r

@memodict
def max_regret(game, digits=6):
    """
    The max regret for each action.
    """
    mx = dict((pl, -inf) for pl in game.players)
    r = game.mixed_strategy_profile()
    for i in xrange(len(r)):
        r[i] = 0.0
    for pl in game.players:
        for p in action_profiles(game, pl, game.mixed_strategy_profile()):
            vs = p.strategy_values(pl)
            M = reduce(max, vs)
            mx[pl] = max(mx[pl], M)
            for i in xrange(len(vs)):
                r[pl][i] = max(r[pl][i], round(M-vs[i], digits))

    return r
max_regret._inv = True

@memodict
def max_efficiency(game):
    """
    The maximum combined payoffs (efficiency) of each action.
    """
    m = game.mixed_strategy_profile()
    for i in xrange(len(m)):
        m[i] = -inf
    actions = [None]*len(game.players)
    for p in action_profiles(game, reuseProfile=game.mixed_strategy_profile(), actions=actions):
        v = sum(p.payoff(pl) for pl in game.players)
        for ai in actions:
            m[ai] = max(m[ai], v)
    return m

@memodict
def min_unfairness(game):
    """
    The lowest max-min spread for each action.
    """
    m = game.mixed_strategy_profile()
    for i in xrange(len(m)):
        m[i] = inf
    actions = [None]*len(game.players)
    for p in action_profiles(game, reuseProfile=game.mixed_strategy_profile(), actions=actions):
        vs = [p.payoff(pl) for pl in game.players]
        dev = max(vs) - min(vs)
        for ai in actions:
            m[ai] = min(m[ai], dev)
    return m
min_unfairness._inv = True

@memodict
def symmetric_payoffs(game):
    """
    The payoff for each action if the other agents play the 'same' action.
    Not informative for asymmetric games.
    """
    p = game.mixed_strategy_profile()
    m = game.mixed_strategy_profile()
    for i in xrange(len(m)):
        m[i] = 0.0
        p[i] = 0.0

    if not is_symmetric_game(game):
        return m

    for ai in xrange(len(m[game.players[0]])):
        for pl in game.players:
            p[pl][ai] = 1.0
        for pl in game.players:
            m[pl][ai] = p.payoff(pl)
        for pl in game.players:
            p[pl][ai] = 0.0
    return m

def is_symmetric_game(game):
    """
    Return true if ``game`` is symmetric in the restricted sense that every
    player has the same number of actions.
    """
    p0 = game.players[0]

    # Are all the strategy sets the same size?
    for pl in game.players:
        if len(pl.strategies) != len(p0.strategies):
            return False

    # TODO: Should we also require off-diagonal symmetry?
    return True

def is_strictly_symmetric_game(game):
    """
    Return true if `game` is symmetric in the strong sense that permutations of
    action profiles lead to the same permutation of payoffs.
    """
    if not is_symmetric_game(game):
        return False

    p0 = game.players[0]
    for c in fast_contingencies(game):
        U = [ game[c][pl] for pl in game.players ]

        revC = tuple(reversed(c))
        revU = [game[revC][pl] for pl in game.players ]
        revU.reverse()
        if revU <> U:
            return False

    return True

        
        
# -------------------------- Payoff binary features -------------------------

def gen_binary_feature(feature_name, raw_feature, reduce_op, docstring):
    """
    Construct a binary feature that picks the action with the most
    ``raw_feature``, where 'most' is defined by ``reduceOp``.  The feature will
    have ``docstring``.
    """
    def feature(game):
        p = raw_feature(game)
        for pl in game.players:
            M = reduce(reduce_op, p[pl])
            for ai in pl.strategies:
                if p[ai] == M:
                    p[ai] = 1.0
                else:
                    p[ai] = 0.0
        return p

    feature.__doc__ = docstring
    feature.func_name = feature_name
    return memodict(feature)

minimax_regret = gen_binary_feature('minimax_regret', max_regret, min,
    """
    Binary feature: Minimax regret action(s) for each player get a 1.
    """)

maxmax = gen_binary_feature('maxmax', max_payoff, max,
    """
    Binary feature: Maximum best-case payoff actions get a 1.
    """)

maxmin = gen_binary_feature('maxmin', min_payoff, max,
    """
    Binary feature: Maximum worst-case payoff actions get a 1.
    """)

maxmax_efficiency = gen_binary_feature('maxmax_efficiency', max_efficiency, max,
    """
    Binary feature: Actions that can lead to (maximally) efficient outcomes are salient.
    """)

minmin_unfairness = gen_binary_feature('minmin_unfairness', min_unfairness, min,
    """
    Binary feature: Actions that can lead to minimally unfair outcomes are
    salient.
    """)

max_symmetric = gen_binary_feature('max_symmetric', symmetric_payoffs, max,
    """
    Binary feature: Actions with the best payoff if everyone plays the
    same action.
    """)
