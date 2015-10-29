"""
Solver support for external solvers (QRE and Nash equilibrium).
"""
from __future__ import absolute_import
from numpy import inf
from gambit.qre import ExternalStrategicQREPathTracer
from gambit.nash import ExternalEnumPureSolver, ExternalLCPSolver, ExternalGlobalNewtonSolver
from bogota.solver import solver
from bogota.utils import proportionally_mix_profiles
import bogota.data #HACK

from bogota.cache import NASH_CACHE

import logging
error = logging.getLogger(__name__).error

@solver(fittable_parameters=['lam'],
        parameter_bounds={'lam':(0.0, None)})
def qre(game, lam):
    """
    Return a quantal response equilibrium with precision 'lam' for 'game'.
    """
    try:
        if lam == 0.0:
            return game.mixed_strategy_profile()
        s = ExternalStrategicQREPathTracer()
        return s.compute_at_lambda(game, lam)[0]
    except:
        error("Exception during qre(%s,%f)", game.title, lam)
        raise

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
    global NASH_CACHE
    if game in NASH_CACHE:
        eqa = NASH_CACHE[game]
    elif len(game.players) == 2:
        s = ExternalLCPSolver()
        eqa = s.solve(game)
        NASH_CACHE[game] = eqa
    else:
        s = ExternalGlobalNewtonSolver()
        eqa = s.solve(game)
        NASH_CACHE[game] = eqa
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

