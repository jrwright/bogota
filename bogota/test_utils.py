from itertools import product as cross_product
import gambit
import numpy.random
from bogota.utils import zero_profile, near

try:
    import os.path
    dirname=os.path.dirname(os.path.abspath(__file__))
    nfg = gambit.Game.read_game(dirname+'/2x2.nfg')
    agg = gambit.Game.read_game(dirname+'/2x2.agg')
except NameError:
    from warnings import warn
    warn("test_utils loaded instead of imported; `nfg` will be a dummy table, `agg` will not be created.")
    nfg = gambit.new_table([2,2])

def leftmost(game, eps=0.3):
    """
    Predict the 'leftmost' action, with ``eps`` proportion of uniform noise.
    """
    profile = game.mixed_strategy_profile()
    for p in game.players:
        si = profile[p]
        m = len(si)
        for i in range(m):
            if i == 0:
                si[i] = si[i]*eps + (1.0 - eps)
            else:
                si[i] *= eps
    return profile

def profile(probs=[0.0, 0.0, 0.0, 0.0]):
    p = nfg.mixed_strategy_profile()
    assert(len(probs) == len(p))
    for (i, prob) in enumerate(probs):
        p[i] = prob
    return p

def constantly(x):
    return (lambda *args: x)

def u(g, i, j):
    p = zero_profile(g)
    p[g.players[0]][i] = 1.0
    p[g.players[1]][j] = 1.0
    return (round(p.payoff(0)), round(p.payoff(1)))

def compare_nfgs(g1, g2):
    if len(g1.players) != len(g2.players):
        return False, "different player counts"
    for i in range(len(g1.players)):
        if len(g1.players[i].strategies) != len(g2.players[i].strategies):
            return False, "different strategy counts for player %d" % i
    assert len(g1.players) == 2
    for i in range(len(g1.players[0].strategies)):
        for j in range(len(g1.players[1].strategies)):
            if u(g1, i, j) != u(g2, i, j):
                return False, "payoffs differ at %d,%d" % (i,j)
    return True

def random_nfg(max_players, max_actions, min_utility=0, max_utility=100, seed=None):
    assert max_actions >= 2
    r = numpy.random.RandomState(seed)
    N = r.randint(max_players) + 1
    dims = [r.randint(max_actions-1) + 2 for n in range(N)]
    g = gambit.Game.new_table(dims)
    for c in cross_product(*map(range, dims)):
        for i in range(N):
            u = r.randint(max_utility - min_utility) + min_utility
            g[c][i] = u
    return g

