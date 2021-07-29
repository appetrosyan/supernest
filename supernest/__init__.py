r"""Superpositional model repartitiong for accelerated nested sampling.

model repartitioning also known as posterior or more accurrately
conclusion re-partitioning is a technique that allows reshaping the
input functions: prior and likelihood and achieving faster Bayesian
inference by way of Nested Sampling.

IMPORTANT: This is an early version of the software, which does not
yet have the links to the proper publication, nor indeed is guaranteed
to function. If you use this for your research, please consider
waiting until the full release.

"""
from .core import superimpose as __superimpose
from .core import gaussian_proposal as __gaussian_proposal
from .core import Proposal, NDProposal

import numpy as np

def superimpose(models: list, nDims: int = None):
    return __superimpose(models, nDims)


superimpose.__doc__ = __superimpose.__doc__


def gaussian_proposal(bounds: np.ndarray,
                      mean: np.ndarray,
                      stdev: np.ndarray,
                      loglike: callable = None):
    return __gaussian_proposal(bounds, mean, stdev, loglike)


gaussian_proposal.__doc__ = __gaussian_proposal.__doc__
