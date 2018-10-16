"""
Implement the noisy introspection model from [Goeree and Holt 2004].
"""
from __future__ import absolute_import
from numpy.linalg import norm
from .solver import solver
from .cognitive_hierarchy import logit_br_all

@solver(fittable_parameters=['lam0', 'tel'],
        parameter_bounds={'lam0':(0.0,None), 'tel':(1.05, None)})
def noisy_introspection(game, lam0, tel, thresh=1e-6, return_steps=False, max_steps=1000):
    """
    Return the play predicted by the noisy introspection model for 'game' with
    initial precision 'lam0' and telescope parameter 'tel'.

    If 'return_steps' is `True`, returns `k,p`, where `k` is the number of
    steps where the sequence converged, and `p` is the prediction.
    Otherwise returns `p`.

    Noisy introspection is defined as the limit of a sequence of noisy
    responses; this function computes sequences of increasing length and then
    stops when the sequence has converged.  The sequence is considered
    converged when the L2 distance between two elements is less than 'thresh'.

    Raises a `ValueError` if no convergence after 'max_steps' steps.
    """
    assert lam0 >= 0.0
    assert tel > 1.0

    def prediction(steps):
        p = game.mixed_strategy_profile()
        for k in xrange(steps, -1, -1):
            lam = (tel**(-k)) * lam0
            p = logit_br_all(p, lam)
        return p
    def delta(p1,p2):
        return norm([x1-x2 for (x1,x2) in zip(p1,p2)])

    K = 0
    p1 = game.mixed_strategy_profile()
    p2 = prediction(K)
    while delta(p1,p2) > thresh:
        K += 1
        p1 = p2
        p2 = prediction(K)
        if max_steps is not None and K > max_steps:
            raise ValueError("noisy_introspection: too many steps with no convergence on game %s with lam0=%s tel=%s", game.title, lam0, tel)

    if return_steps:
        return K,p2
    else:
        return p2
