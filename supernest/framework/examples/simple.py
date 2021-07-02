# from super_nest.framework.gaussian_models import GaussianPeakedPrior
from pypolychord import run_polychord
from pypolychord.settings import PolyChordSettings


def loglike(arr):
    return 1, []


def prior(arr):
    return arr


ps = PolyChordSettings(3, 0)
run_polychord(loglike, 3, 0, ps)
