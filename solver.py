"""
Define the [Solver] class and the [solver] convenience decorator.
"""
from logging import debug
from warnings import warn
import numpy as np
from numpy.random import RandomState
import scipy.optimize
import cmaes

# ================================= decorator =================================

def solver(fittable_parameters,
           parameter_bounds=None, simplex_parameters=None, parameter_scales=None,
           **kwArgs):
    """
    Convenience decorator; will add a `Solver` member to `fn` which creates a
    Solver with `fn` as the function and the provided parameters.
    """
    def decorator(fn):
        def makeSolver(**kwArgs2):
            args = dict(kwArgs)
            args.update(kwArgs2)
            return Solver(fn, fittable_parameters, parameter_bounds, simplex_parameters,
                          parameter_scales, **args)
        fn.Solver = makeSolver
        return fn
    return decorator

# ================================== classes ==================================

class Solver(object):
    DEFAULT_PENALTY_COEFFICIENT = 5.0
    DEFAULT_CONSTRAINT_ITER = 5
    DEFAULT_SIGMA0 = 0.25

    def __init__(self, fn, fittable_parameters,
                 parameter_bounds=None,
                 simplex_parameters=None,
                 parameter_scales=None,
                 **kwArgs):
        # Copy solver args
        self.fn = fn
        self.fittable_parameters = list(fittable_parameters)
        assert 'prediction_cache' not in self.fittable_parameters, "'prediction_cache' is a reserved parameter name" 

        self.parameter_bounds = dict(parameter_bounds or [])
        for p in fittable_parameters:
            if p not in self.parameter_bounds:
                self.parameter_bounds[p] = (None, None)

        self.parameter_scales = dict(parameter_scales or [])
        for p in fittable_parameters:
            if p not in self.parameter_scales:
                self.parameter_scales[p] = 1.0

        self.simplex_parameters = list(simplex_parameters or [])
        for cell in self.simplex_parameters:
            for p in cell:
                if p not in parameter_bounds:
                    self.parameter_bounds[p] = (0.0, 1.0)

        # Set function arguments
        first_default = self.fn.func_code.co_argcount
        if self.fn.func_defaults is not None:
            first_default -= len(self.fn.func_defaults)
        for (i, name) in enumerate(self.fittable_parameters):
            # Plus one to skip the first arg, which is not a parameter
            if (i+1) < first_default:
                setattr(self, name, 0.0)
            else:
                setattr(self, name, self.fn.func_defaults[i+1 - first_default])

        self.kwArgs = dict(kwArgs)
        for arg in kwArgs:
            if arg in self.fittable_parameters:
                setattr(self, arg, self.kwArgs.pop(arg))

        self.fit_args = {}
        if 'fit_args' in self.kwArgs:
            self.fit_args.update(self.kwArgs['fit_args'])
            del self.kwArgs['fit_args']

        self.penalty_coefficient = self.DEFAULT_PENALTY_COEFFICIENT
        self.constraint_iter = self.DEFAULT_CONSTRAINT_ITER

        self.parameters = ParametersWrapper(self)

    def __call__(self, game):
        return self.predict(game)

    def fit(self, objective, **kwargs):
        # TODO - default kwargs for different kinds of function
        try:
            debug("Fitting '%s'", self.fn.name)
        except:
            pass
        
        kw = {}
        kwargs = dict(kwargs)
        def scalar_target(x):
            self.parameters[0] = x
            return self.penalized_objective(objective)

        def mv_target(xs):
            for (i, x) in enumerate(xs):
                self.parameters[i] = x
            return self.penalized_objective(objective)

        if 'full_output' in kwargs and kwargs['full_output']:
            warn("%s.fit: ignoring 'full_output' argument" % self.__class__.__name__)

        if 'no_cmaes' in kwargs:
            no_cmaes = kwargs.pop('no_cmaes')
        else:
            no_cmaes = False

        penalty_coefficient = self.penalty_coefficient
        for retry_count in xrange(self.constraint_iter):
            if len(self.fittable_parameters) == 1:

                # Brack extraction
                (a,b) = self.parameter_bounds.values()[0]
                if a is not None and b is not None:
                    kw['brack'] = (a,b)
                    x = self.parameters[0]
                    fx = scalar_target(x)
                    if a<x<b and scalar_target(a) > fx and scalar_target(b) > fx:
                        kw['brack'] = (a,x,b)
                    self.parameters[0] = x
                kw.update(kwargs)
                kw['full_output'] = False
                result = [scipy.optimize.brent(scalar_target, **kw)]
            elif no_cmaes:
                kw = {}
                kw.update(kwargs)
                kw['full_output'] = False
                result = scipy.optimize.fmin(mv_target, np.array(self.parameters), **kw)
            else:
                # scales = []
                # for p in self.fittable_parameters:
                #     scales.append(self.parameter_scales()[p])
                # kw = {'scaling_of_variables':np.array(scales)}
                kw = {'verb_log':0}
                kw.update(kwargs)
                res = cmaes.fmin(mv_target,
                                 np.array(self.parameters),
                                 self.DEFAULT_SIGMA0,
                                 **kw)
                print "res=%s" % (res,) #TEST
                result = res[0]

            # Extract and check results
            for (i, y) in enumerate(result):
                self.parameters[i] = y
            if self.penalty() == 0.0:
                break

            # Constraint check failed, try again from current starting point
            # with higher penalty_coefficient
            self.clamp()
            penalty_coefficient *= penalty_coefficient

        return list(self.parameters)

    def predict(self, game, prediction_cache=None):
        args = dict(self.kwArgs)
        if prediction_cache is not None:
            args['prediction_cache'] = prediction_cache
        for p in self.fittable_parameters:
            args[p] = getattr(self, p)
        profile = self.fn(game, **args)
        return profile

    def penalized_objective(self, objective):
        """
        Return a minimization objective value that includes a penalty term for
        violated constraints.
        """
        try:
            # Need to compute the penalty before we clamp, obviously
            penalty = self.penalty()
            self.clamp()
            fval = -objective(self.predict)
            return fval + self.penalty_coefficient * penalty
        except:
            print "*** %s: Rogue exception with parameters %s" % (str(self), list(self.parameters))
            raise

    def clamp(self):
        """
        Clamp `self.parameters` to constraint-satisfying values.
        """
        # Box constraints
        for (k, (a,b)) in self.parameter_bounds.items():
            v = getattr(self, k)
            if a is not None and v < a:
                setattr(self, k, a)
            elif b is not None and v > b:
                setattr(self, k, b)

        # Simplex constraints - clamp by normalizing, sorry omitted var
        for vars in self.simplex_parameters:
            total = sum(getattr(self, v) for v in vars)
            if total <= 1.0:
                continue
            for v in vars:
                val = getattr(self, v)
                setattr(self, v, val/total)


    def penalty(self):
        """
        Return 0.0 if all constraints are satisfied, or a quadratic penalty for
        each violated constraint.
        """
        ret = 0.0

        # Simplex constraints
        for vars in self.simplex_parameters:
            total = sum(getattr(self, v) for v in vars)
            if total > 1.0:
                ret += (1.0 - total)**2

        # Box constraints
        for (k, (a,b)) in self.parameter_bounds.items():
            v = getattr(self, k)
            if a is not None and v < a:
                ret += (a-v)**2
            if b is not None and v > b:
                ret += (v-b)**2

        return ret

    def random_start(self, rng=RandomState()):
        """
        Set parameters to randomized starting values where possible.
        """
        randomized = dict(zip(self.fittable_parameters, [False]*len(self.fittable_parameters)))

        # Simplex parameters
        for names in self.simplex_parameters:
            alpha = [1.0] * (len(names) + 1)
            vals = rng.dirichlet(alpha)
            for (i, name) in enumerate(names):
                randomized[name] = True
                self.parameters[name] = vals[i+1]

        # Bounded parameters
        for (name, (a, b)) in self.parameter_bounds.items():
            if randomized[name]:
                # Skip already-randomized parameters (i.e., simplex params)
                continue
            if a is not None and b is not None:
                self.parameters[name] = rng.uniform(low=a, high=b)
                randomized[name] = True
            elif a is not None:
                self.parameters[name] = a + abs(rng.normal(0.0, self.parameter_sigma(name)))
                randomized[name] = True
            elif b is not None:
                self.parameters[name] = b - abs(rng.normal(0.0, self.parameter_sigma(name)))
                randomized[name] = True

        # Warn for uninitialized fittable parameters
        for name in self.fittable_parameters:
            if not randomized[name]:
                warn("%s.random_start: fittable parameter '%s' not initialized" % \
                     (self.__class__.__name__, name))


class ParametersWrapper(object):
    """
    Provides position-based access to named parameters.
    The target object should have a `fittable_parameters` field.
    """
    def __init__(self, target):
        self.target = target
    def __getitem__(self, idx):
        if isinstance(idx, str):
            name = idx
        else:
            name = self.target.fittable_parameters[idx]
        return getattr(self.target, name)
    def __setitem__(self, idx, val):
        if isinstance(idx, str):
            name = idx
        else:
            name = self.target.fittable_parameters[idx]
        return setattr(self.target, name, val)
    def __len__(self):
        return len(self.target.fittable_parameters)
    def __repr__(self):
        return str(list(self))
