from math import log
from numpy import inf
import gambit
import bogota.datapool as datapool
from bogota.test_utils import profile, constantly, near, nfg

def test_averaging():
    d = profile([1,0,0,1])
    wp = datapool.WeightedUncorrelatedProfile(None, d)
    opool = datapool.DataPool([wp])
    pool = datapool.AveragingPool(opool)

    def opred0(game):
        return profile([0.75, 0.25, 0.75, 0.25])
    def pred0(game):
        return [opred0(game)]
    assert near(pool.log_likelihood(pred0), opool.log_likelihood(opred0))

    def pred1(game):
        return [profile([1,0,1,0]), profile([0,1,0,1])]
    assert pool.log_likelihood(pred1) == -inf

    def pred2(game):
        return [profile([1,0,0,1]), profile([0.5, 0.5, 0.5, 0.5])]
    assert near(pool.log_likelihood(pred2), log(0.5))

def test_peekaboo():
    d1 = profile([25.0, 75.0, 25.0, 75.0])
    d2 = profile([25.0, 75.0, 0.0, 0.0])
    wp1 = datapool.WeightedUncorrelatedProfile(None, d1)
    wp2 = datapool.WeightedUncorrelatedProfile(None, d2)
    opool = datapool.PeekabooPool([wp1, wp2])
    pool = datapool.PeekabooPool(opool)

    trn, tst = pool.train_fold_gamewise(10, 2, 0, True)

    def pred(game, prediction_cache):
        r = repr(prediction_cache['peek_data']._profile)
        assert r ==  repr(wp1._profile) or r ==  repr(wp2._profile), (r, repr(wp1._profile), repr(wp2._profile))
        return prediction_cache['peek_data']._profile

    pool.log_likelihood(pred)
    trn.log_likelihood(pred)
    tst.log_likelihood(pred)

def test_asymmetric():
    d1 = profile([0.25, 0.75, 0.25, 0.75])
    d2 = profile([0.25, 0.75, 0.0, 0.0])
    wp1 = datapool.WeightedUncorrelatedProfile(200, d1)
    wp2 = datapool.WeightedUncorrelatedProfile(200, d2)
    print(wp1.n, wp2.n)
    assert wp1.n == wp2.n

    p1 = profile([0.8, 0.2, 0.0, 0.0])
    p2 = profile([0.8, 0.2, 0.8, 0.2])
    print(wp1.log_likelihood(p1), wp2.log_likelihood(p2))
    assert wp1.log_likelihood(p2) == wp2.log_likelihood(p2)

def test_certainty():
    p = profile([1.0, 0.0, 0.0, 0.0])
    wp = datapool.WeightedUncorrelatedProfile(1, p)
    pool = datapool.DataPool([wp])
    assert wp.log_likelihood(p) == 0.0
    assert pool.log_likelihood(constantly(p)) == 0.0

    wp = datapool.WeightedUncorrelatedProfile(1000, p)
    pool = datapool.DataPool([wp])
    assert wp.log_likelihood(p) == 0.0
    assert pool.log_likelihood(constantly(p)) == 0.0

    p[0] = 0.0
    p[1] = 1.0
    assert wp.log_likelihood(p) == -inf
    assert pool.log_likelihood(constantly(p)) == -inf

def test_unbalanced():
    wp = datapool.WeightedUncorrelatedProfile(None, profile([1.0, 2.0, 3.0, 6.0]))
    pool = datapool.DataPool([wp])
    predict = profile([0.75, 0.25, 0.25, 0.75])
    ll = 7.0*log(0.75) + 5.0*log(0.25)
    assert abs(pool.log_likelihood(constantly(predict)) - ll) < 1e-6

def test_denormalization():
    from bogota.data import cn_some9
    wp1 = datapool.WeightedUncorrelatedProfile(None, profile([1.0, 2.0, 3.0, 6.0]))
    wp2 = datapool.WeightedUncorrelatedProfile(8, profile([0.25, 0.75, 0.5, 0.5]))
    wp3 = cn_some9.weighted_profiles[15]
    assert list(wp1.denormalized_profile()) == [1.0, 2.0, 3.0, 6.0]
    assert list(wp2.denormalized_profile()) == [1.0, 3.0, 2.0, 2.0]
    for p in wp3.denormalized_profile():
        assert p % 1 == 0.0

def test_test_train():
    wp1 = datapool.WeightedUncorrelatedProfile(None, profile([1.0, 2.0, 3.0, 6.0]))
    wp2 = datapool.WeightedUncorrelatedProfile(8, profile([0.25, 0.75, 0.5, 0.5]))
    pool = datapool.DataPool([wp1, wp2])
    (test,train) = pool.test_and_train(1, 0.25)
    assert test.n == 5
    assert train.n == 15

    # We happen to know that picking the first fold is the same as selecting an
    # appropriately-sized test set from the original pool
    test2 = pool.test_fold(1, 4, 0)
    assert test.n == test2.n
    for (wp, wp2) in zip(test.weighted_profiles, test2.weighted_profiles):
        dnp = wp.denormalized_profile()
        dnp2 = wp2.denormalized_profile()
        for i in range(len(dnp)):
            assert dnp[i] == dnp2[i]


def test_divide_folds():
    wp1 = datapool.WeightedUncorrelatedProfile(None, profile([100, 102, 10, 192]))
    wp2 = datapool.WeightedUncorrelatedProfile(8, profile([0.25, 0.75, 0.5, 0.5]))
    pool1 = datapool.DataPool([wp1])
    pool2 = datapool.DataPool([wp2])

    # Check that data points are distributed properly across the folds
    for i in range(10):
        fold1 = pool1.test_fold(1, 10, i)
        if i < 4:
            assert fold1.n == 41
        else:
            assert fold1.n == 40

        fold2 = pool2.test_fold(1, 10, i)
        if i < 8:
            assert fold2.n == 1
        else:
            assert fold2.n == 0

    # Check that our subtraction method for extracting the test fold works properly
    (test,train) = pool1.test_and_train(1, 0.25)
    train1 = pool1.train_fold(1, 4, 0)
    assert train.n == train1.n
    for (wp, wp1) in zip(train.weighted_profiles, train1.weighted_profiles):
        dnp = wp.denormalized_profile()
        dnp1 = wp1.denormalized_profile()
        for i in range(len(dnp)):
            assert dnp[i] == dnp1[i]

def test_divide_folds_gamewise_stratified(noassert=False):
    def new_game(s,n,d=0):
        g = gambit.Game.new_table([2,2])
        g[0,0][0] = n
        g[0,0][1] = d
        g.title = "bogota.datapool_test.stratum_%d.g_%d" % (s,n)
        return g

    wps = [datapool.WeightedUncorrelatedProfile(8, new_game(i,j).mixed_strategy_profile()) for i in range(3) for j in range(20-i)]
    pool = datapool.DataPool(wps)
    folds = pool._divide_folds_gamewise(5, 12345, True)
    assert noassert or sum(map(len, folds)) == len(wps)

    wps = [datapool.WeightedUncorrelatedProfile(8, new_game(i,j,i).mixed_strategy_profile()) for i in range(3) for j in range(20-i)]
    pool = datapool.DataPool(wps)
    folds = pool._divide_folds_gamewise(5, 12345, True)
    assert noassert or sum(map(len, folds)) == len(wps)

    return folds

def test_ppd_profile():
    wp = datapool.WeightedUncorrelatedProfile(None, profile([1.0, 0.0, 0.0, 0.0]))
    ppd = wp.ppd_profile()
    assert near(ppd, [2.0/3.0, 1.0/3.0, 0.0, 0.0]), ppd

def test_neg_ppd_cross_entropy():
    wp1 = datapool.WeightedUncorrelatedProfile(None, profile([1.0, 0.0, 0.0, 0.0]))
    wp2 = datapool.WeightedUncorrelatedProfile(None, profile([100.0, 0.0, 0.0, 0.0]))
    predictor = lambda x: profile([0.75, 0.25, 0.75, 0.25])

    assert near(wp1.neg_ppd_cross_entropy(predictor(0.0)), log(0.75) * (2.0/3.0) + log(0.25) * (1.0/3.0))
    assert near(wp2.neg_ppd_cross_entropy(predictor(0.0)), log(0.75) * (101.0/102.0) + log(0.25) * (1.0/102.0))

    pool = datapool.DataPool([wp1, wp2])
    assert near(pool.neg_ppd_cross_entropy(predictor),
                wp1.neg_ppd_cross_entropy(predictor(0.0)) + wp2.neg_ppd_cross_entropy(predictor(0.0)))

def test_kl_divergence():
    wp1 = datapool.WeightedUncorrelatedProfile(None, profile([1.0, 0.0, 0.0, 0.0]))
    wp2 = datapool.WeightedUncorrelatedProfile(None, profile([100.0, 0.0, 0.0, 0.0]))

    d1 = datapool.DataPool([wp1])
    d2 = datapool.DataPool([wp2])

    q0 = lambda x: profile([1.0, 0.0, 1.0, 0.0])
    predictor = lambda x: profile([0.75, 0.25, 0.75, 0.25])

    assert near(0.0, d1.kl_divergence(q0))
    assert near(0.0, d2.kl_divergence(q0))

    assert near(d1.kl_divergence(q0), d2.kl_divergence(q0))

    pool = datapool.DataPool([wp1, wp2])
    assert near(0.0, pool.kl_divergence(q0))
    assert near(d1.kl_divergence(predictor) + d2.kl_divergence(predictor),
                pool.kl_divergence(predictor))

    assert pool.kl_divergence(predictor) > 0.0
    
