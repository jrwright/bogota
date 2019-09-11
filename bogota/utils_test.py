import gambit
from bogota.utils import game_array, normalize, near, zero_profile

def test_game_array():
    nfg = gambit.Game.new_table([3,3])
    nfg[0,0][0] = 1
    nfg[0,0][1] = 2
    nfg[1,1][0] = 5
    nfg[1,1][1] = 8
    nfg[2,2][0] = 6
    nfg[2,2][1] = 7

    print(nfg)
    A = game_array(nfg)
    print(A)

    assert A[0,0][0] == 1
    assert A[0,0][1] == 2
    assert A[1,1][0] == 5
    assert A[1,1][1] == 8
    assert A[2,2][0] == 6
    assert A[2,2][1] == 7

def test_normalize():
    assert near(normalize([1,2,3]),
                [1./6, 2./6, 3./6])

    assert near(normalize([-1,-2,-3]),
                [2./3, 1./3, 0./3]), normalize([-1,-2,-3])

    nfg = gambit.Game.new_table([3,3])
    p = nfg.mixed_strategy_profile()
    p[0] = 1
    p[1] = 2
    p[2] = 3
    p[3] = -1
    p[4] = -2
    p[5] = -3

    assert near(normalize(p),
                [1./6, 2./6, 3./6,
                 2./3, 1./3, 0./3]), (
                     normalize(p),
                     [1./6, 2./6, 3./6,
                      2./3, 1./3, 0./3])

    
    assert near(normalize([0.0, 0.0, 0.0, 0.0]),
                [0.25, 0.25, 0.25, 0.25])

    p = zero_profile(nfg)
    assert near(normalize(p),
                [1./3, 1./3, 1./3, 1./3, 1./3, 1./3])

    
