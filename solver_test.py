from bogota.solver import solver
from bogota.utils import near

@solver(['x', 'y'])
def fn(g, x, y):
    return -(x-1.5)**2 - (y+10)**2

def test_fit():
    s = fn.Solver()
    s.fit(lambda p: p(None))
    assert near(s.x, 1.5)
    assert near(s.y, -10)

def main():
    test_fit()

if __name__ == '__main__':
    main()
