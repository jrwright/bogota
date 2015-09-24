import csv
from bogota.pool_utils import make_nfg, cents_normalize
from bogota.utils import zero_profile

# Points are $0.15 in one randomly chosen game in 2000.
CGW08_CENTS_PER_POINT = 15.0 / 14

cgw08_1 = make_nfg([[(78,73), (69,23), (12,14)],
                    [(67,52), (59,61), (78,53)],
                    [(16,76), (65,87), (94,79)]])

cgw08_2 = make_nfg([[(21,67), (59,57), (85,63)],
                    [(71,76), (50,65), (74,14)],
                    [(12,10), (61,76), (77,92)]])

cgw08_3 = make_nfg([[(74,38), (78,71), (46,43)],
                    [(96,12), (10,89), (57,25)],
                    [(15,51), (83,18), (69,62)]])

cgw08_4 = make_nfg([[(73,80), (20,85), (91,12)],
                    [(45,48), (64,71), (27,59)],
                    [(40,76), (53,17), (14,98)]])

cgw08_5 = make_nfg([[(78,49), (60,68), (27,35)],
                    [(10,82), (49,10), (98,38)],
                    [(69,64), (42,39), (85,86)]])

cgw08_6 = make_nfg([[(39,99), (36,28), (57,86)],
                    [(83,11), (50,79), (65,70)],
                    [(11,50), (69,61), (40,43)]])

cgw08_7 = make_nfg([[(84,82), (33,95), (12,73)],
                    [(21,28), (39,37), (68,64)],
                    [(70,39), (31,48), (59,81)]])

cgw08_8 = make_nfg([[(47,30), (94,32), (36,38)],
                    [(38,69), (81,83), (27,20)],
                    [(80,58), (72,11), (63,67)]])

cgw08_9 =  make_nfg([[(57,58), (46,34), (74,70)],
                     [(89,32), (31,83), (12,41)],
                     [(41,94), (16,37), (53,23)]])

cgw08_10 = make_nfg([[(60,59), (34,91), (96,43)],
                     [(36,48), (85,33), (39,18)],
                     [(72,76), (43,14), (25,55)]])

cgw08_11 = make_nfg([[(43,91), (38,81), (92,64)],
                     [(39,27), (79,68), (68,19)],
                     [(69,10), (66,21), (74,54)]])

cgw08_12 = make_nfg([[(25,27), (90,43), (38,60)],
                     [(49,39), (53,73), (78,52)],
                     [(64,85), (20,46), (19,78)]])

cgw08_13 = make_nfg([[(83,40), (23,68), (70,81)],
                     [(93,45), (12,71), (29,41)],
                     [(66,94), (56,76), (21,70)]])

cgw08_14 = make_nfg([[(82,61), (36,46), (24,22)],
                     [(43,17), (70,50), (40,87)],
                     [(75,16), (49,75), (57,35)]])

cn_cgw08_1 = cents_normalize(cgw08_1, CGW08_CENTS_PER_POINT)
cn_cgw08_2 = cents_normalize(cgw08_2, CGW08_CENTS_PER_POINT)
cn_cgw08_3 = cents_normalize(cgw08_3, CGW08_CENTS_PER_POINT)
cn_cgw08_4 = cents_normalize(cgw08_4, CGW08_CENTS_PER_POINT)
cn_cgw08_5 = cents_normalize(cgw08_5, CGW08_CENTS_PER_POINT)
cn_cgw08_6 = cents_normalize(cgw08_6, CGW08_CENTS_PER_POINT)
cn_cgw08_7 = cents_normalize(cgw08_7, CGW08_CENTS_PER_POINT)
cn_cgw08_8 = cents_normalize(cgw08_8, CGW08_CENTS_PER_POINT)
cn_cgw08_9 = cents_normalize(cgw08_9, CGW08_CENTS_PER_POINT)
cn_cgw08_10 = cents_normalize(cgw08_10, CGW08_CENTS_PER_POINT)
cn_cgw08_11 = cents_normalize(cgw08_11, CGW08_CENTS_PER_POINT)
cn_cgw08_12 = cents_normalize(cgw08_12, CGW08_CENTS_PER_POINT)
cn_cgw08_13 = cents_normalize(cgw08_13, CGW08_CENTS_PER_POINT)
cn_cgw08_14 = cents_normalize(cgw08_14, CGW08_CENTS_PER_POINT)

def write_games():
    for ix,g in enumerate([cn_cgw08_1, cn_cgw08_2, cn_cgw08_3, cn_cgw08_4, cn_cgw08_5, cn_cgw08_6, cn_cgw08_7, cn_cgw08_8, cn_cgw08_9, cn_cgw08_10,  cn_cgw08_11,  cn_cgw08_12,  cn_cgw08_13,  cn_cgw08_14]):
        fname = "cn_cgw08_%d.nfg" % (ix+1)
        print fname
        with open(fname, 'wt') as f:
            g.title = "bogota.data.cn_costagomes2008stated.cn_cgw08_%d" % (ix+1)
            f.write(repr(g))

def read_data(fname, treatments = [0.012, 0.102, 0.10101]):
    """
    Read in data from the supplementary datafile from
    [Costa-Gomes & Weizsacker 2008].
    """
    GAMES = [cn_cgw08_8, cn_cgw08_3, cn_cgw08_10, cn_cgw08_6, cn_cgw08_14, cn_cgw08_1, cn_cgw08_12, cn_cgw08_4, cn_cgw08_7, cn_cgw08_13, cn_cgw08_5, cn_cgw08_2, cn_cgw08_9, cn_cgw08_11]
    GAMES_STRS = ['cn_cgw08_8', 'cn_cgw08_3', 'cn_cgw08_10', 'cn_cgw08_6', 'cn_cgw08_14', 'cn_cgw08_1', 'cn_cgw08_12', 'cn_cgw08_4', 'cn_cgw08_7', 'cn_cgw08_13', 'cn_cgw08_5', 'cn_cgw08_2', 'cn_cgw08_9', 'cn_cgw08_11']
    AIXS = [4 + 4*x for x in xrange(14)]
    ROLE_IX = 3
    TREATMENT_IX = 1
    h = dict([(gstr, zero_profile(g)) for (g, gstr) in zip(GAMES, GAMES_STRS)])
    with open(fname, 'rt') as f:
        for line in f:
            cols = map(float, line.split())
            if cols[TREATMENT_IX] not in treatments:
                continue
            print "[",
            for g, gstr, acn_ix in zip(GAMES, GAMES_STRS, AIXS):
                aix = cols[acn_ix]-1 if cols[ROLE_IX] == 1 else 3 + cols[acn_ix]-1
                print "%s.strategies[%d]," % (gstr, aix),
                h[gstr][int(aix)] += 1
            print "],"
    print "\n["
    for gstr in sorted(h):
        p = h[gstr]
        print "WeightedUncorrelatedProfile(None,make_profile(%s,%s))," % (gstr, map(int, p))
    print "]"
