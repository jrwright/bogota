"""
Test cognitive_hierarchy module
"""
from bogota.test_utils import nfg
import bogota.cognitive_hierarchy as cognitive_hierarchy

def test_zeros():
    alphas = cognitive_hierarchy.poisson_alphas(0.0, 1)
    assert alphas == [1.0, 0.0]

    p = cognitive_hierarchy.poisson_qch(nfg, 0.0, 1.0)
    assert list(p) == [0.5, 0.5, 0.5, 0.5]

    p = cognitive_hierarchy.poisson_qch(nfg, 1.0, 0.0)
    for pi in p:
        assert abs(pi - 0.5) < 1e-6

    alphas = cognitive_hierarchy.spike_poisson_alphas(1.0, 1.0, 3)
    assert alphas == [1.0, 0.0, 0.0, 0.0]

    alphas = cognitive_hierarchy.spike_poisson_alphas(0.5, 0.0, 3)
    print alphas
    assert alphas == [1.0, 0.0, 0.0, 0.0]

    p = cognitive_hierarchy.spike_poisson_qch(nfg, 0.5, 0.0, 0.5)
    print p
    for pi in p:
        assert abs(pi - 0.5) < 1e-6

def test_qlk_compare():
    #TODO compare Lisp QLk predictions to Python QLk
    pass

def main():
    test_zeros()
    test_qlk_compare()

if __name__ == '__main__':
    main()
