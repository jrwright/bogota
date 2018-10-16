import tempfile
import gambit
from bogota.utils import zero_profile, near
from posec.pyagg import AGG, FN_TYPE_SUM, FN_TYPE_WEIGHTED_MAX

def make_travellers_dilemma(min_claim=2, max_claim=100, penalty=2):
    """
    Construct an instance of Traveller's Dilemma encoded as an AGG, with bounds
    'min_claim' and 'max_claim' and 'penalty' as a miscoordination
    penalty/reward.
    """
    N = ['row', 'col']
    A = range(min_claim, max_claim+1)
    S = {'row':A, 'col':A}
    F = ['lt_%d' % a for a in A[1:]] + \
        ['gt_%d' % a for a in A[:-1]] + \
        ['mx_%d' % a for a in A[1:]]
    f = dict((n, (FN_TYPE_WEIGHTED_MAX, 0) if n[0:2] == 'mx' else FN_TYPE_SUM) for n in F)
    v = []

    # Connections from function nodes to claims
    for a in A:
        if a > min_claim:
            v.append(('lt_%d' % a, a))
            v.append(('mx_%d' % a, a))
        if a < max_claim:
            v.append(('gt_%d' % a, a))

    # Connections from claims to function nodes
    for a in A:
        for b in A:
            if a < b:
                v.append((a, 'lt_%d' % b))
                v.append((a, 'mx_%d' % b, a))
            if a > b:
                v.append((a, 'gt_%d' % b))

    def gen_ufcn(a):
        def ufcn(cfg):
            lt, mx, gt = cfg
            if lt == 0 and gt == 0:
                return a
            elif gt > 0:
                return a + penalty
            else:
                return mx - penalty
        return ufcn

    u = {max_claim:lambda cfg: max_claim if cfg[0]==0 else cfg[1] - penalty,
         min_claim:lambda cfg: min_claim if cfg[0]==0 else min_claim + penalty}
    for a in A[1:-1]:
        u[a]=gen_ufcn(a)

    agg = AGG(N,A,S,F,v,f,u)

    with tempfile.NamedTemporaryFile(suffix='.agg', prefix="td_%d_%d_%d_" % (min_claim, max_claim, penalty), delete=True) as f:
        agg.saveToFile(f.name)
        g = gambit.Game.read_game(f.name)

    # Add back metadata that doesn't persist through the file format
    g.title = "Traveller's Dilemma min=%d/max=%d/r=%d" % (min_claim, max_claim, penalty)
    for i in xrange(max_claim, min_claim-1, -1): # Descending order to avoid name collisions
        g.players[0].strategies[i-min_claim].label=str(i)
        g.players[1].strategies[i-min_claim].label=str(i)

    return g

def u(g, i, j):
    p = zero_profile(g)
    p[g.players[0]][i] = 1.0
    p[g.players[1]][j] = 1.0
    return (round(p.payoff(0)), round(p.payoff(1)))

def compare_nfgs(g1, g2):
    if len(g1.players) != len(g2.players):
        return False, "different player counts"
    for i in xrange(len(g1.players)):
        if len(g1.players[i].strategies) != len(g2.players[i].strategies):
            return False, "different strategy counts for player %d" % i
    assert len(g1.players) == 2
    for i in xrange(len(g1.players[0].strategies)):
        for j in xrange(len(g1.players[1].strategies)):
            p1 = zero_profile(g1)
            p2 = zero_profile(g2)
            p1[g1.players[0]][i] = 1.0
            p1[g1.players[1]][j] = 1.0
            p2[g2.players[0]][i] = 1.0
            p2[g2.players[1]][j] = 1.0
            if not near(p1.payoff(0), p2.payoff(0)):
                return False, "payoffs differ for p1 at %d,%d" % (i,j)
            if not near(p1.payoff(1), p2.payoff(1)):
                return False, "payoffs differ for p2 at %d,%d" % (i,j)
    return True

def makeGH01():
    td_low = make_travellers_dilemma(180, 300, 2)
    td_low.saveToFile('travellers_dilemma_low.agg')
    td_high = make_travellers_dilemma(180, 300, 180)
    td_high.saveToFile('travellers_dilemma_high.agg')

