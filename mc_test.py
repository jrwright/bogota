from bogota.mc import stochastic_slices
import pymc as pm

def test_stochastic_slices():
    rvs = [pm.Uniform('a', size=(5,6,7), lower=0, upper=1), pm.Exponential('b', beta=1.0, value=[0.1, 0.2])]
    slices = stochastic_slices(rvs)
    assert slices[rvs[0]].start == 0
    assert slices[rvs[1]].start == 210

    assert slices[rvs[0]].stop == 210
    assert slices[rvs[1]].stop == 212

    assert len(rvs) == 2
