"""
Example specific predictors.
"""


from bogota.solver import Solver
from bogota.cognitive_hierarchy import poisson_qch, spike_poisson_qch, poisson_ch, lk, qlk
from bogota.level0 import weighted_linear_l0_prediction, logit_l0_prediction
from bogota.level0 import \
    minimax_regret, maxmax, maxmin, maxmax_efficiency,\
    minmin_unfairness, max_symmetric, constant_binary

# ============================ Specific predictors ============================

def linear4(game, weights, eps, tau, lam):
    global linear4_internal
    try:
        if linear4_internal is None:
            pass
    except NameError:
        linear4_internal = gen_linear_spike_poisson(LINEAR4_FEATURES, True, False)

    return linear4_internal(game, eps, tau, lam,
                            w_maxmax=weights[0],
                            w_maxmin=weights[1],
                            w_minmin_unfairness=weights[2],
                            w_max_symmetric=weights[3])

def linear8(game, weights, eps, tau, lam):
    try:
        if linear8_internal is None:
            pass
    except NameError:
        linear8_internal = gen_linear_spike_poisson(LINEAR8_FEATURES, True, True)

    return linear8_internal(game, eps, tau, lam,
                            w_max_payoff=weights[0],
                            w_min_payoff=weights[1],
                            w_min_unfairness=weights[2],
                            w_symmetric_payoffs=weights[3],
                            w_maxmax=weights[4],
                            w_maxmin=weights[5],
                            w_minmin_unfairness=weights[6],
                            w_max_symmetric=weights[7])


# ======================= Support for generic predictors ======================

def LinearPoissonSolver(features, applicable_only=True, normalize_activations=True):
    """
    Construct a `Solver` that uses `features` for its level-0 model
    and `poisson_qch` for its higher-level predictions.

    Args:
      features: list of feature functions; will be passed to
                `weighted_linear_l0_prediction` to construct the level-0
                prediction.
      applicable_only: whether to omit "inapplicable" features.
                       (default: True)
      normalize_activations: whether to normalize feature values to sum to 1
                             before mixing according to the learned feature
                             weights.
                             (default: True)
    """
    weight_names = ["w_%s" %(f.__name__) for f in features]
    pbounds = {'tau':(0.0, None), 'lam':(0.0, None)}
    psimplex = [tuple(weight_names)]
    return Solver(gen_linear_poisson(features, applicable_only, normalize_activations),
                  ['tau', 'lam'] + weight_names,
                  parameter_bounds=pbounds,
                  simplex_parameters=psimplex)

def gen_linear_poisson(features, applicable_only=True, normalize_activations=True):
    """
    Construct a prediction function that uses `features` for its level-0 model
    and `poisson_qch` for its higher-level predictions.  The resulting function
    is suitable for passing to the `fn` argument of `Solver`.

    Args:
      features: list of feature functions; will be passed to
                `weighted_linear_l0_prediction` to construct the level-0
                prediction.
      applicable_only: whether to omit "inapplicable" features.
                       (default: True)
    """
    weight_names = ["w_%s" %(f.__name__) for f in features]

    def linear_poisson(game, tau, lam, **kw):
        weights = [kw[n] for n in weight_names]
        w0 = max(0.0, 1.0 - sum(weights))
        l0 = weighted_linear_l0_prediction([constant_binary] + features,
                                           [w0] + weights,
                                           game, applicable_only, normalize_activations)
        return poisson_qch(game, tau, lam, l0)

    return linear_poisson

def LinearSpikePoissonSolver(features, applicable_only=True, normalize_activations=True):
    """
    Construct a `Solver` that uses `features` for its level-0 model and
    `spike_poisson_qch` for its higher-level predictions, with features mixed
    according to `weighted_linear_l0_prediction`.

    Args:
      features: list of feature functions; will be passed to
                `weighted_linear_l0_prediction` to construct the level-0
                prediction.
      applicable_only: whether to omit "inapplicable" features.
                       (default: True)
      normalize_activations: whether to normalize feature values to sum to 1
                             before mixing according to the learned feature
                             weights.
                             (default: True)
    """
    weight_names = ["w_%s" %(f.__name__) for f in features]
    pbounds = {'eps':(0.0, 1.0), 'tau':(0.0, None), 'lam':(0.0, None)}
    psimplex = [tuple(weight_names)]
    return Solver(gen_linear_spike_poisson(features, applicable_only, normalize_activations),
                  ['eps', 'tau', 'lam'] + weight_names,
                  parameter_bounds=pbounds,
                  simplex_parameters=psimplex)

def gen_linear_spike_poisson(features, applicable_only=True, normalize_activations=True):
    """
    Construct a prediction function that uses `features` for its level-0 model
    and `spike_poisson_qch` for its higher-level predictions.  The resulting
    function is suitable for passing to the `fn` argument of `Solver`.

    Args:
      features: list of feature functions; will be passed to
                `weighted_linear_l0_prediction` to construct the level-0
                prediction.
      applicable_only: whether to omit "inapplicable" features.
                       (default: True)
      normalize_activations: whether to normalize feature values to sum to 1
                             before mixing according to the learned feature
                             weights.
                             (default: True)
    """
    weight_names = ["w_%s" %(f.__name__) for f in features]

    def linear_spike_poisson(game, eps, tau, lam, **kw):
        weights = [kw[n] for n in weight_names]
        w0 = max(0.0, 1.0 - sum(weights))
        l0 = weighted_linear_l0_prediction([constant_binary] + features,
                                           [w0] + weights,
                                           game, applicable_only, normalize_activations)
        return spike_poisson_qch(game, eps, tau, lam, l0)

    return linear_spike_poisson

def LinearLkSolver(features, applicable_only=True, normalize_activations=True):
    """
    Construct a `Solver` that uses `features` for its level-0 model and
    `lk` for its higher-level predictions, with features mixed
    according to `weighted_linear_l0_prediction`.

    Args:
      features: list of feature functions; will be passed to
                `weighted_linear_l0_prediction` to construct the level-0
                prediction.
      applicable_only: whether to omit "inapplicable" features.
                       (default: True)
      normalize_activations: whether to normalize feature values to sum to 1
                             before mixing according to the learned feature
                             weights.
                             (default: True)
    """
    weight_names = ["w_%s" %(f.__name__) for f in features]
    pbounds = {'eps1':(0.0, 1.0), 'eps2':(0.0, 1.0)}
    psimplex = [tuple(['a1', 'a2']), tuple(weight_names)]
    return Solver(gen_linear_lk(features, applicable_only, normalize_activations),
                  ['a1', 'a2', 'eps1', 'eps2'] + weight_names,
                  parameter_bounds=pbounds,
                  simplex_parameters=psimplex)

def gen_linear_lk(features, applicable_only=True, normalize_activations=True):
    """
    Construct a prediction function that uses `features` for its level-0 model
    and `poisson_ch` for its higher-level predictions.  The resulting
    function is suitable for passing to the `fn` argument of `Solver`.

    Args:
      features: list of feature functions; will be passed to
                `weighted_linear_l0_prediction` to construct the level-0
                prediction.
      applicable_only: whether to omit "inapplicable" features.
                       (default: True)
      normalize_activations: whether to normalize feature values to sum to 1
                             before mixing according to the learned feature
                             weights.
                             (default: True)
    """
    weight_names = ["w_%s" %(f.__name__) for f in features]

    def linear_lk(game, a1, a2, eps1, eps2, **kw):
        weights = [kw[n] for n in weight_names]
        w0 = max(0.0, 1.0 - sum(weights))
        l0 = weighted_linear_l0_prediction([constant_binary] + features,
                                           [w0] + weights,
                                           game, applicable_only, normalize_activations)
        return lk(game, a1, a2, eps1, eps2, l0_prediction=l0)

    return linear_lk

def LinearPoissonCHSolver(features, applicable_only=True, normalize_activations=True):
    """
    Construct a `Solver` that uses `features` for its level-0 model and
    `poisson_ch` for its higher-level predictions, with features mixed
    according to `weighted_linear_l0_prediction`.

    Args:
      features: list of feature functions; will be passed to
                `weighted_linear_l0_prediction` to construct the level-0
                prediction.
      applicable_only: whether to omit "inapplicable" features.
                       (default: True)
      normalize_activations: whether to normalize feature values to sum to 1
                             before mixing according to the learned feature
                             weights.
                             (default: True)
    """
    weight_names = ["w_%s" %(f.__name__) for f in features]
    pbounds = {'tau':(0.0, None)}
    psimplex = [tuple(weight_names)]
    return Solver(gen_linear_poisson_ch(features, applicable_only, normalize_activations),
                  ['tau'] + weight_names,
                  parameter_bounds=pbounds,
                  simplex_parameters=psimplex)

def gen_linear_poisson_ch(features, applicable_only=True, normalize_activations=True):
    """
    Construct a prediction function that uses `features` for its level-0 model
    and `poisson_ch` for its higher-level predictions.  The resulting
    function is suitable for passing to the `fn` argument of `Solver`.

    Args:
      features: list of feature functions; will be passed to
                `weighted_linear_l0_prediction` to construct the level-0
                prediction.
      applicable_only: whether to omit "inapplicable" features.
                       (default: True)
      normalize_activations: whether to normalize feature values to sum to 1
                             before mixing according to the learned feature
                             weights.
                             (default: True)
    """
    weight_names = ["w_%s" %(f.__name__) for f in features]

    def linear_poisson_ch(game, tau, **kw):
        weights = [kw[n] for n in weight_names]
        w0 = max(0.0, 1.0 - sum(weights))
        l0 = weighted_linear_l0_prediction([constant_binary] + features,
                                           [w0] + weights,
                                           game, applicable_only, normalize_activations)
        return poisson_ch(game, tau, l0)

    return linear_poisson_ch

def LinearQLkSolver(features, applicable_only=True, normalize_activations=True):
    """
    Construct a `Solver` that uses `features` for its level-0 model and
    `qlk` for its higher-level predictions, with features mixed
    according to `weighted_linear_l0_prediction`.

    Args:
      features: list of feature functions; will be passed to
                `weighted_linear_l0_prediction` to construct the level-0
                prediction.
      applicable_only: whether to omit "inapplicable" features.
                       (default: True)
      normalize_activations: whether to normalize feature values to sum to 1
                             before mixing according to the learned feature
                             weights.
                             (default: True)
    """
    weight_names = ["w_%s" %(f.__name__) for f in features]
    pbounds = {'lam1':(0.0,None), 'lam2':(0.0,None), 'lam1_2':(0.0,None)}
    psimplex = [('a1', 'a2'), tuple(weight_names)]
    return Solver(gen_linear_qlk(features, applicable_only, normalize_activations),
                  ['a1', 'a2', 'lam1', 'lam2', 'lam1_2'] + weight_names,
                  parameter_bounds=pbounds,
                  simplex_parameters=psimplex)

def gen_linear_qlk(features, applicable_only=True, normalize_activations=True):
    """
    Construct a prediction function that uses `features` for its level-0 model
    and `qlk` for its higher-level predictions.  The resulting
    function is suitable for passing to the `fn` argument of `Solver`.

    Args:
      features: list of feature functions; will be passed to
                `weighted_linear_l0_prediction` to construct the level-0
                prediction.
      applicable_only: whether to omit "inapplicable" features.
                       (default: True)
      normalize_activations: whether to normalize feature values to sum to 1
                             before mixing according to the learned feature
                             weights.
                             (default: True)
    """
    weight_names = ["w_%s" %(f.__name__) for f in features]

    def linear_qlk(game, a1, a2, lam1, lam2, lam1_2, **kw):
        weights = [kw[n] for n in weight_names]
        w0 = max(0.0, 1.0 - sum(weights))
        l0 = weighted_linear_l0_prediction([constant_binary] + features,
                                           [w0] + weights,
                                           game, applicable_only, normalize_activations)
        return qlk(game, a1, a2, lam1, lam2, lam1_2, l0_prediction=l0)

    return linear_qlk


def LogitSpikePoissonSolver(features, normalize_activations):
    """
    Construct a `Solver` that uses `features` for its level-0 model and
    `spike_poisson_qch` for its higher-level predictions, with features mixed
    according to `logit_l0_prediction`.

    Args:
      features: list of feature functions; will be passed to
                `logit_l0_prediction` to construct the level-0
                prediction.
      normalize_activations: whether to normalize feature values to sum to 1
                             before mixing according to the learned feature
                             weights.
                             (default: True)
    """
    weight_names = ["w_%s" %(f.__name__) for f in features]
    pbounds = {'eps':(0.0, 1.0), 'tau':(0.0, None), 'lam':(0.0, None), 'link_lam':(0.0, None)}
    psimplex = [tuple(weight_names)]
    return Solver(gen_logit_spike_poisson(features, normalize_activations),
                  ['eps', 'tau', 'lam', 'link_lam'] + weight_names,
                  parameter_bounds=pbounds,
                  simplex_parameters=psimplex)

def gen_logit_spike_poisson(features, normalize_activations):
    """
    Construct a prediction function that uses `features` for its level-0 model
    and `spike_poisson_qch` for its higher-level predictions.  The resulting
    function is suitable for passing to the `fn` argument of `Solver`.

    Args:
      features: list of feature functions; will be passed to
                `logit_l0_prediction` to construct the level-0
                prediction.
      normalize_activations: whether to normalize feature values to sum to 1
                             before mixing according to the learned feature
                             weights.
                             (default: True)
    """
    weight_names = ["w_%s" %(f.__name__) for f in features]

    def logit_spike_poisson(game, eps, tau, lam, link_lam, **kw):
        weights = [kw[n] for n in weight_names]
        w0 = max(0.0, 1.0 - sum(weights))
        l0 = logit_l0_prediction([constant_binary] + features,
                                 [w0] + weights,
                                 link_lam,
                                 game, normalize_activations)
        return spike_poisson_qch(game, eps, tau, lam, l0)

    return logit_spike_poisson

def LogitPoissonSolver(features, normalize_activations):
    """
    Construct a `Solver` that uses `features` for its level-0 model and
    `poisson_qch` for its higher-level predictions, with features mixed
    according to `logit_l0_prediction`.

    Args:
      features: list of feature functions; will be passed to
                `logit_l0_prediction` to construct the level-0
                prediction.
      normalize_activations: whether to normalize feature values to sum to 1
                             before mixing according to the learned feature
                             weights.
                             (default: True)
    """
    weight_names = ["w_%s" %(f.__name__) for f in features]
    pbounds = {'tau':(0.0, None), 'lam':(0.0, None), 'link_lam':(0.0, None)}
    psimplex = [tuple(weight_names)]
    return Solver(gen_logit_poisson(features, normalize_activations),
                  ['tau', 'lam', 'link_lam'] + weight_names,
                  parameter_bounds=pbounds,
                  simplex_parameters=psimplex)

def gen_logit_poisson(features, normalize_activations):
    """
    Construct a prediction function that uses `features` for its level-0 model
    and `poisson_qch` for its higher-level predictions.  The resulting
    function is suitable for passing to the `fn` argument of `Solver`.

    Args:
      features: list of feature functions; will be passed to
                `logit_l0_prediction` to construct the level-0
                prediction.
      normalize_activations: whether to normalize feature values to sum to 1
                             before mixing according to the learned feature
                             weights.
                             (default: True)
    """
    weight_names = ["w_%s" %(f.__name__) for f in features]

    def logit_poisson(game, tau, lam, link_lam, **kw):
        weights = [kw[n] for n in weight_names]
        w0 = max(0.0, 1.0 - sum(weights))
        l0 = logit_l0_prediction([constant_binary] + features,
                                 [w0] + weights,
                                 link_lam,
                                 game, normalize_activations)
        return poisson_qch(game, tau, lam, l0)

    return logit_poisson

