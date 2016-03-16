"""
Solver support for external solvers (QRE and Nash equilibrium).
"""
from __future__ import absolute_import
from numpy import inf, linspace
from gambit.qre import ExternalStrategicQREPathTracer
from gambit.nash import ExternalEnumPureSolver, ExternalLCPSolver, ExternalGlobalNewtonSolver
from bogota.solver import solver, GridSolver
from bogota.utils import proportionally_mix_profiles
from bogota.cache import get_eqa, put_eqa, find_eqm_key, find_qre_key, get_qre, put_qres
import bogota.data # HACK to force the module to load for fitting

import logging
error = logging.getLogger(__name__).error

@solver(fittable_parameters=['lam'],
        parameter_bounds={'lam':(0.0, None)})
def qre(game, lam, tol=0.0005):
    """
    Return a quantal response equilibrium with precision `lam` for `game`.  If
    `tol` is greater than 0.0, then a cached QRE with precision within `tol` of
    `lam` may be returned instead.
    """
    try:
        if lam == 0.0:
            return game.mixed_strategy_profile()
        elif find_qre_key(game, lam, tol):
            return get_qre(game, lam, tol)
        else:
            s = ExternalStrategicQREPathTracer()
            q = s.compute_at_lambda(game, lam)[0]
            put_qres(game, {lam:q})
            return q
    except:
        error("Exception during qre(%s,%f)", game.title, lam)
        raise

class _QRE_GridSolver(GridSolver):
    def __init__(self):
        LAM = list(linspace(0.0, 1.0, 1001)) + list(linspace(1.1, 10.0, 90))
        super(_QRE_GridSolver, self).__init__(qre, 'lam', LAM)
qre.GridSolver = _QRE_GridSolver


@solver(fittable_parameters= ['eps'],
        parameter_bounds={'eps':(0.0, 1.0)})
def pure_nash(game, eps):
    """
    Return a Nash equilibrium mixed with uniform noise.
    """
    s = ExternalEnumPureSolver()
    eqa = s.solve(game)
    assert len(eqa) == 1, "%d eqa found" % len(eqa)
    return proportionally_mix_profiles([eps, 1.0-eps],
                                       [game.mixed_strategy_profile(), eqa[0]])

@solver(fittable_parameters= ['eps'],
        parameter_bounds={'eps':(0.0, 1.0)})
def nee(game, eps):
    """
    Return a set of Nash equilibria, each mixed with uniform noise.
    """
    if find_eqm_key(game):
        eqa = get_eqa(game)
    elif len(game.players) == 2:
        s = ExternalLCPSolver()
        eqa = s.solve(game)
        put_eqa(game, eqa)
    else:
        s = ExternalGlobalNewtonSolver()
        eqa = s.solve(game)
        put_eqa(game, eqa)
    assert len(eqa) > 0
    return [proportionally_mix_profiles([eps, 1.0-eps], [game.mixed_strategy_profile(), eqm]) for eqm in eqa]

@solver(fittable_parameters= ['eps'],
        parameter_bounds={'eps':(0.0, 1.0)})
def bnee(game, eps, prediction_cache=None):
    """
    For each `eps`-noised equilibrium of `game`, find the one that performs best
    on the `peek_data` entry of `prediction_cache` and return it.
    """
    eqa = nee(game, eps)
    if len(eqa) == 1:
        return eqa[0]

    wp = prediction_cache['peek_data']
    best_ll = -inf
    best_eqm = None
    for eqm in eqa:
        ll = wp.log_likelihood(eqm)
        if ll > best_ll or best_eqm is None:
            best_eqm = eqm
            best_ll = ll
    return best_eqm

@solver(fittable_parameters= ['eps'],
        parameter_bounds={'eps':(0.0, 1.0)})
def wnee(game, eps, prediction_cache=None):
    """
    For each `eps`-noised equilibrium of `game`, find the one that performs worst
    on the `peek_data` entry of `prediction_cache` and return it.
    """
    eqa = nee(game, eps)
    if len(eqa) == 1:
        return eqa[0]
    elif len(eqa) == 0:
        raise RuntimeError("OH NOE WHERE IS EQM")

    wp = prediction_cache['peek_data']
    assert wp.game == game
    worst_ll = inf
    worst_eqm = None
    for eqm in eqa:
        ll = wp.log_likelihood(eqm)
        if ll < worst_ll or worst_eqm is None:
            worst_eqm = eqm
            worst_ll = ll
    return worst_eqm

