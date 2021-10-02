r"""Proposals used in supernest.

These are provided for convenience, any proposal has an element called
`prior` and an element called `likelihood`, or a tuple where the first two elements
are the prior and the likelihood.
"""
import typing
import numpy as np
import scipy.special as sp
import supernest.utils as utils
import warnings


class Prior:
    """Class wrapping prior quantile."""

    def __init__(self, prior_callable):
        """Create."""
        self.prior = prior_callable

    def __call__(self, cube):
        """Call wrapped prior quantile."""
        return self.prior(cube)


class Likelihood:
    """Class for representing likelihood."""

    def __init__(self, log_like_callable):
        """Create."""
        self.loglikelihood = log_like_callable

    def __call__(self, theta):
        """Call wrapped function."""
        return self.loglikelihood(theta)

    def __repr__(self):
        """Representation."""
        return f"Likelihood wrapping {repr(self.loglikelihood)}"


class CorrectedLikelihood:
    """Class representing a likelihood with a correction."""

    def __init__(self, original, corrected):
        """Create."""
        self.original = original
        self.corrected = corrected

    def __call__(self, theta):
        """Call."""
        return self.corrected(theta)

    def __repr__(self):
        """Represent."""
        return f"""Likelihood wrapping
    {self.corrected}
which is based on
    {self.original}"""


class Proposal(typing.NamedTuple):
    """Class wrapping proposals."""

    prior: Prior
    likelihood: callable
    nDims: int = None

    def __repr__(self):
        """Representation."""
        return f"""Proposal

prior:
------
{repr(self.prior)}

likelihood:
-----------


{repr(self.likelihood)}"""
