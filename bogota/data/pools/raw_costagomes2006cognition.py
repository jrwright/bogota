import decimal
import gambit
new_table = gambit.Game.new_table
# from bogota.pool_utils import cents_normalize

def cents_normalize(x,y):
    return x

# inflation times 4c/pt time 5/16 games chosen at random
CGC06_CENTS_PER_POINT = 1.17 * 4 * 5 / 16

def make_cgc06_game(title, range1, target1, range2, target2, binsize=1):
    if binsize==1:
        Ai = list(range(range1[0], range1[1]+1))
        Aj = list(range(range2[0], range2[1]+1))
    else:
        Ai = list(range(range1[0], range1[1], binsize))
        Aj = list(range(range2[0], range2[1], binsize))

    g = new_table([len(Ai), len(Aj)])

    # Hack to avoid conflicting with initial labels
    for ix in range(len(g.strategies)):
        g.strategies[ix].label = "old%d" % ix

    # Set up labels
    g.title = title
    for aix,ai in enumerate(Ai):
        if binsize==1:
            g.players[0].strategies[aix].label = str(ai)
        else:
            g.players[0].strategies[aix].label = "%d--%d" % (ai, ai+binsize-1)

    # Set up payoffs
    for ajx,aj in enumerate(Aj):
        if binsize==1:
            g.players[1].strategies[ajx].label = str(aj)
        else:
            g.players[1].strategies[ajx].label = "%d--%d" % (aj, aj+binsize-1)

    for aix, ai in enumerate(Ai):
        for ajx, aj in enumerate(Aj):
            ei = abs(aj*target1 - ai)
            si = max(0, 200-ei) + max(0, 100 - ei/10)

            ej = abs(ai*target2 - aj)
            sj = max(0, 200-ej) + max(0, 100 - ej/10)

            g[aix,ajx][0] = decimal.Decimal(si)
            g[aix,ajx][1] = decimal.Decimal(sj)

    return g

# Ranges
alpha = [100, 500]
beta = [100, 900]
gamma = [300, 500]
delta = [300, 900]

# Targets
t1 = 0.5
t2 = 0.7
t3 = 1.3
t4 = 1.5

GAME_PARAMS = [(alpha, t2, beta, t1),
               (beta, t1, alpha, t2),
               (beta, t1, gamma, t2),
               (gamma, t2, beta, t1),
               (gamma, t4, delta, t3),
               (delta, t3, gamma, t4),
               (delta, t3, delta, t3),
               (delta, t3, delta, t3),
               (beta, t1, alpha, t4),
               (alpha, t3, beta, t1),
               (delta, t2, beta, t3),
               (beta, t3, delta, t2),
               (gamma, t2, beta, t4),
               (beta, t4, gamma, t2),
               (alpha, t2, alpha, t4),
               (alpha, t4, alpha, t2)]

GAME_ORDER = [1,3,5,7,9,11,13,15,2,4,6,8,10,12,14,16]
GAME_IXS = {}
for ix,g in zip(list(range(1,17)), GAME_ORDER):
    GAME_IXS[g] = ix

def get_aix(interval, binsize, guess):
    best_aix = -1
    if binsize == 1:
        Ai = list(range(interval[0], interval[1]+1))
    else:
        Ai = list(range(interval[0], interval[1], binsize))
    for aix, ai in enumerate(Ai):
        if ai <= guess:
            best_aix = aix
    best_aix = max(0, best_aix)
    return best_aix

def profile_size(params, binsize):
    """
    Return the dimensions of a flat profile for a game constructed from
    `params` with `binsize`.
    """
    if binsize==1:
        Ai = list(range(params[0][0], params[0][1]+1))
        Aj = list(range(params[2][0], params[2][1]+1))
    else:
        Ai = list(range(params[0][0], params[0][1], binsize))
        Aj = list(range(params[2][0], params[2][1], binsize))

    return len(Ai) + len(Aj)

def parse_data(fname, binsize, treatments=[]):
    binstr = "" if binsize==1 else "_bin%s" % binsize
    h = {}
    for gix in range(16):
        gname = "cn_cgc06%s_%d" % (binstr, gix+1)
        h[gname] = [0]*profile_size(GAME_PARAMS[gix], binsize)
        print("%s = make_cgc06_game('%s',%s%s)" % (gname,
                                                   gname,
                                                   ','.join(map(str, GAME_PARAMS[gix])),
                                                   "" if binsize==1 else ",%s" % binsize))
    with open(fname, 'rt') as f:
        print("cn_costagomes2006cognition%s_traces=TraceSet([" % (binstr))
        for line in f:
            print("[", end=' ')
            cols = line.split('\t')
            for colx,gid in enumerate(GAME_ORDER):
                guess = int(round(float(cols[colx+1])))
                aix = get_aix(GAME_PARAMS[gid-1][0], binsize, guess)
                gname = "cn_cgc06%s_%d" % (binstr, gid)
                print("%s.strategies[%d]," % (gname, aix), end=' ')
                h[gname][aix] += 1
            print("],")
        print("])")

    print("\ncn_costagomes2006cognition%s=DataPool([" % (binstr))
    for gstr in sorted(h):
        p = h[gstr]
        print("WeightedUncorrelatedProfile(None,make_profile(%s,%s))," % (gstr, list(map(int, p))))
    print("])")

cn_cgc06_1 = None
cn_cgc06_2 = None
cn_cgc06_3 = None
cn_cgc06_4 = None
cn_cgc06_5 = None
cn_cgc06_6 = None
cn_cgc06_7 = None
cn_cgc06_8 = None
cn_cgc06_9 = None
cn_cgc06_10 = None
cn_cgc06_11 = None
cn_cgc06_12 = None
cn_cgc06_13 = None
cn_cgc06_14 = None
cn_cgc06_15 = None
cn_cgc06_16 = None

def construct_unbinned():
    global cn_cgc06_1, cn_cgc06_2, cn_cgc06_3, cn_cgc06_4, cn_cgc06_5, cn_cgc06_6, cn_cgc06_7, cn_cgc06_8,\
        cn_cgc06_9, cn_cgc06_10, cn_cgc06_11, cn_cgc06_12, cn_cgc06_13, cn_cgc06_14, cn_cgc06_15, cn_cgc06_16

    print("cn_cgc06_1...")
    cn_cgc06_1 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_1',[100, 500],0.7,[100, 900],0.5), CGC06_CENTS_PER_POINT)
    print("cn_cgc06_2...")
    cn_cgc06_2 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_2',[100, 900],0.5,[100, 500],0.7), CGC06_CENTS_PER_POINT)
    print("cn_cgc06_3...")
    cn_cgc06_3 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_3',[100, 900],0.5,[300, 500],0.7), CGC06_CENTS_PER_POINT)
    print("cn_cgc06_4...")
    cn_cgc06_4 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_4',[300, 500],0.7,[100, 900],0.5), CGC06_CENTS_PER_POINT)
    print("cn_cgc06_5...")
    cn_cgc06_5 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_5',[300, 500],1.5,[300, 900],1.3), CGC06_CENTS_PER_POINT)
    print("cn_cgc06_6...")
    cn_cgc06_6 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_6',[300, 900],1.3,[300, 500],1.5), CGC06_CENTS_PER_POINT)
    print("cn_cgc06_7...")
    cn_cgc06_7 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_7',[300, 900],1.3,[300, 900],1.3), CGC06_CENTS_PER_POINT)
    print("cn_cgc06_8...")
    cn_cgc06_8 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_8',[300, 900],1.3,[300, 900],1.3), CGC06_CENTS_PER_POINT)
    print("cn_cgc06_9...")
    cn_cgc06_9 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_9',[100, 900],0.5,[100, 500],1.5), CGC06_CENTS_PER_POINT)
    print("cn_cgc06_10...")
    cn_cgc06_10 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_10',[100, 500],1.3,[100, 900],0.5), CGC06_CENTS_PER_POINT)
    print("cn_cgc06_11...")
    cn_cgc06_11 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_11',[300, 900],0.7,[100, 900],1.3), CGC06_CENTS_PER_POINT)
    print("cn_cgc06_12...")
    cn_cgc06_12 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_12',[100, 900],1.3,[300, 900],0.7), CGC06_CENTS_PER_POINT)
    print("cn_cgc06_13...")
    cn_cgc06_13 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_13',[300, 500],0.7,[100, 900],1.5), CGC06_CENTS_PER_POINT)
    print("cn_cgc06_14...")
    cn_cgc06_14 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_14',[100, 900],1.5,[300, 500],0.7), CGC06_CENTS_PER_POINT)
    print("cn_cgc06_15...")
    cn_cgc06_15 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_15',[100, 500],0.7,[100, 500],1.5), CGC06_CENTS_PER_POINT)
    print("cn_cgc06_16...")
    cn_cgc06_16 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_16',[100, 500],1.5,[100, 500],0.7), CGC06_CENTS_PER_POINT)

cn_cgc06_bin10_1 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin10_1',[100, 500],0.7,[100, 900],0.5,10), CGC06_CENTS_PER_POINT)
cn_cgc06_bin10_2 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin10_2',[100, 900],0.5,[100, 500],0.7,10), CGC06_CENTS_PER_POINT)
cn_cgc06_bin10_3 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin10_3',[100, 900],0.5,[300, 500],0.7,10), CGC06_CENTS_PER_POINT)
cn_cgc06_bin10_4 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin10_4',[300, 500],0.7,[100, 900],0.5,10), CGC06_CENTS_PER_POINT)
cn_cgc06_bin10_5 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin10_5',[300, 500],1.5,[300, 900],1.3,10), CGC06_CENTS_PER_POINT)
cn_cgc06_bin10_6 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin10_6',[300, 900],1.3,[300, 500],1.5,10), CGC06_CENTS_PER_POINT)
cn_cgc06_bin10_7 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin10_7',[300, 900],1.3,[300, 900],1.3,10), CGC06_CENTS_PER_POINT)
cn_cgc06_bin10_8 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin10_8',[300, 900],1.3,[300, 900],1.3,10), CGC06_CENTS_PER_POINT)
cn_cgc06_bin10_9 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin10_9',[100, 900],0.5,[100, 500],1.5,10), CGC06_CENTS_PER_POINT)
cn_cgc06_bin10_10 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin10_10',[100, 500],1.3,[100, 900],0.5,10), CGC06_CENTS_PER_POINT)
cn_cgc06_bin10_11 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin10_11',[300, 900],0.7,[100, 900],1.3,10), CGC06_CENTS_PER_POINT)
cn_cgc06_bin10_12 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin10_12',[100, 900],1.3,[300, 900],0.7,10), CGC06_CENTS_PER_POINT)
cn_cgc06_bin10_13 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin10_13',[300, 500],0.7,[100, 900],1.5,10), CGC06_CENTS_PER_POINT)
cn_cgc06_bin10_14 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin10_14',[100, 900],1.5,[300, 500],0.7,10), CGC06_CENTS_PER_POINT)
cn_cgc06_bin10_15 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin10_15',[100, 500],0.7,[100, 500],1.5,10), CGC06_CENTS_PER_POINT)
cn_cgc06_bin10_16 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin10_16',[100, 500],1.5,[100, 500],0.7,10), CGC06_CENTS_PER_POINT)

cn_cgc06_bin25_1 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin25_1',[100, 500],0.7,[100, 900],0.5,25), CGC06_CENTS_PER_POINT)
cn_cgc06_bin25_2 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin25_2',[100, 900],0.5,[100, 500],0.7,25), CGC06_CENTS_PER_POINT)
cn_cgc06_bin25_3 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin25_3',[100, 900],0.5,[300, 500],0.7,25), CGC06_CENTS_PER_POINT)
cn_cgc06_bin25_4 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin25_4',[300, 500],0.7,[100, 900],0.5,25), CGC06_CENTS_PER_POINT)
cn_cgc06_bin25_5 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin25_5',[300, 500],1.5,[300, 900],1.3,25), CGC06_CENTS_PER_POINT)
cn_cgc06_bin25_6 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin25_6',[300, 900],1.3,[300, 500],1.5,25), CGC06_CENTS_PER_POINT)
cn_cgc06_bin25_7 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin25_7',[300, 900],1.3,[300, 900],1.3,25), CGC06_CENTS_PER_POINT)
cn_cgc06_bin25_8 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin25_8',[300, 900],1.3,[300, 900],1.3,25), CGC06_CENTS_PER_POINT)
cn_cgc06_bin25_9 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin25_9',[100, 900],0.5,[100, 500],1.5,25), CGC06_CENTS_PER_POINT)
cn_cgc06_bin25_10 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin25_10',[100, 500],1.3,[100, 900],0.5,25), CGC06_CENTS_PER_POINT)
cn_cgc06_bin25_11 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin25_11',[300, 900],0.7,[100, 900],1.3,25), CGC06_CENTS_PER_POINT)
cn_cgc06_bin25_12 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin25_12',[100, 900],1.3,[300, 900],0.7,25), CGC06_CENTS_PER_POINT)
cn_cgc06_bin25_13 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin25_13',[300, 500],0.7,[100, 900],1.5,25), CGC06_CENTS_PER_POINT)
cn_cgc06_bin25_14 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin25_14',[100, 900],1.5,[300, 500],0.7,25), CGC06_CENTS_PER_POINT)
cn_cgc06_bin25_15 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin25_15',[100, 500],0.7,[100, 500],1.5,25), CGC06_CENTS_PER_POINT)
cn_cgc06_bin25_16 = cents_normalize(make_cgc06_game('bogota.data.cn_costagomes2006cognition.cn_cgc06_bin25_16',[100, 500],1.5,[100, 500],0.7,25), CGC06_CENTS_PER_POINT)

def write_games(unbinned):
    s = len("bogota.data.cn_costagomes2006cognition.")
    for g in [cn_cgc06_bin10_1, cn_cgc06_bin10_2, cn_cgc06_bin10_3, cn_cgc06_bin10_4, cn_cgc06_bin10_5, cn_cgc06_bin10_6, cn_cgc06_bin10_7, cn_cgc06_bin10_8, cn_cgc06_bin10_9, cn_cgc06_bin10_10, cn_cgc06_bin10_11, cn_cgc06_bin10_12, cn_cgc06_bin10_13, cn_cgc06_bin10_14, cn_cgc06_bin10_15, cn_cgc06_bin10_16,
              cn_cgc06_bin25_1, cn_cgc06_bin25_2, cn_cgc06_bin25_3, cn_cgc06_bin25_4, cn_cgc06_bin25_5, cn_cgc06_bin25_6, cn_cgc06_bin25_7, cn_cgc06_bin25_8, cn_cgc06_bin25_9, cn_cgc06_bin25_10, cn_cgc06_bin25_11, cn_cgc06_bin25_12, cn_cgc06_bin25_13, cn_cgc06_bin25_14, cn_cgc06_bin25_15, cn_cgc06_bin25_16]:
        fname = g.title[s:] + '.nfg'
        with open(fname, 'wt') as f:
            print(fname)
            f.write(repr(g))

    if unbinned:
        print("Constructing unbinned...")
        construct_unbinned()
        for g in [cn_cgc06_1, cn_cgc06_2, cn_cgc06_3, cn_cgc06_4, cn_cgc06_5, cn_cgc06_6, cn_cgc06_7, cn_cgc06_8, cn_cgc06_9, cn_cgc06_10, cn_cgc06_11, cn_cgc06_12, cn_cgc06_13, cn_cgc06_14, cn_cgc06_15, cn_cgc06_16]:
            fname = g.title[s:] + '.nfg'
            with open(fname, 'wt') as f:
                print(fname)
                f.write(repr(g))

