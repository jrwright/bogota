import gambit
from bogota.utils import game_array

def test_game_array():
    nfg = gambit.Game.new_table([3,3])
    nfg[0,0][0] = 1
    nfg[0,0][1] = 2
    nfg[1,1][0] = 5
    nfg[1,1][1] = 8
    nfg[2,2][0] = 6
    nfg[2,2][1] = 7

    print nfg
    A = game_array(nfg)
    print A

    assert A[0][0,0] == 1
    assert A[1][0,0] == 2
    assert A[0][1,1] == 5
    assert A[1][1,1] == 8
    assert A[0][2,2] == 6
    assert A[1][2,2] == 7
