from bogota.mc import stochastic_slices, theta_to_model, model_to_theta
import pymc as pm
import numpy as np

def test_stochastic_slices():
    rvs = [pm.Uniform('a', size=(5,6,7), lower=0, upper=1),
           pm.Exponential('b', beta=1.0, value=[0.1, 0.2]),
           pm.Uniform('c', lower=0, upper=1)]
    slices = stochastic_slices(rvs)

    assert len(rvs) == 3
    assert slices[rvs[0]].stop - slices[rvs[0]].start == 210
    assert slices[rvs[1]].stop - slices[rvs[1]].start == 2
    assert slices[rvs[2]].stop - slices[rvs[2]].start == 1
    assert max(s.stop for s in slices.values()) == 213


def test_theta():
    rvs = [pm.Uniform('a', size=(2,2), lower=0, upper=1), pm.Uniform('b', size=3, lower=0, upper=1)]
    theta = np.array([1,2,3,4,5,6,7.0])
    slices = stochastic_slices(rvs)
    theta_to_model(slices, theta)
    theta2 = model_to_theta(slices)
    assert all(theta == theta2)
