import numpy as np
import scipy.special as sp
import supernest.utils as utils
from supernest.proposals.types import (Prior, Proposal,
                                       Likelihood, CorrectedLikelihood)
from functools import lru_cache

macheps = np.nextafter(0, 1)


class GaussianPrior(Prior):
    """Class wrapping correlated multivariate normal distribution."""

    def __init__(self, mean, covmat, logzero=-1e30):
        """Create."""
        self.mean = mean
        self.covmat = covmat
        self.logzero = logzero

    def prior(self, cube: np.ndarray):
        """Prior quantile implementation."""
        theta = np.sqrt(2) * sp.erfinv(2 * cube - 1)
        theta = self.mean + np.linalg.cholesky(self.covmat) @ theta
        return utils.guard_against_inf_nan(cube, theta, self.logzero, 1e30)

    def __repr__(self):
        """Representation."""
        return f"""Gaussian
---------
mean:
=====
{self.mean}

covmat:
=======
{self.covmat}"""


def gaussian_proposal(bounds: np.ndarray,
                      mean: np.ndarray,
                      covmat: np.ndarray,
                      loglike: callable = None,
                      logzero: np.float64 = -1e30):
    r"""Produce a Gaussian proposal.

    Given a uniform prior defined by bounds, produces the corrected
    loglikelihood and prior.

    Parameters
    ----------
    bounds: array-like
        A tuple-like or array-like that contains the (min, max) of the
        original uniform prior.

    mean: array-like
        A vector of the means of the gaussian approximation of the proposal

    covmat: array-like
        A matrix containing the covariance of the gaussian proposal.

    loglike: callable (optional)
        The loglikelihood function of the original model to be corrected.

    Returns
    -------
    proposal: Proposal (tuple(prior, loglike))
    """
    covmat, a, b = utils.process_stdev(covmat, mean, bounds)
    log_box = np.log(b - a).sum() if utils.eitheriter(
        (a, b)) else len(mean) * np.log(b - a)
    log_box = -log_box
    invCov = np.linalg.inv(covmat)

    def correction(theta):
        ll, phi = (0, []) if loglike is None else loglike(theta)
        corr = -((theta - mean) @ invCov @ (theta - mean)) / 2.0
        corr -= np.log(
            2 * np.pi) * len(mean) / 2 + np.linalg.slogdet(covmat)[1] / 2

        return (ll - corr + log_box), phi

    return Proposal(GaussianPrior(mean, covmat),
                    Likelihood(correction) if loglike is None
                    else CorrectedLikelihood(loglike, correction),
                    nDims=len(mean))


class PowerPosteriorPrior(Prior):
    """Implementation of Chen, Ferroz and Hobson's posterior repartitioning."""

    def __init__(self, mean, covmat, **kwargs):
        """Construct."""
        self.mean = mean
        self.covmat = covmat
        self.logzero = kwargs.get('logzero')
        self.nDims = kwargs.get('nDims', len(mean))
        self.beta_max = kwargs.get('beta_max', 1)
        self.beta_min = kwargs.get('beta_min', macheps)
        self.bounds = kwargs.get('bounds')

    def power_gaussian_quantile(self, cube, beta=1):
        """Power Gaussian Quantile evaluation."""
        sigma = np.diag(self.covmat)
        da = _erf_term(self.bounds[0] - self.mean, beta, sigma)
        db = _erf_term(self.bounds[1] - self.mean, beta, sigma)
        ret = np.erfinv((1 - cube) * da + cube * db)
        return self.mean + np.sqrt(2/beta) * sigma * ret

    def prior_quantile(self, cube):
        """Calculate the prior quantile function."""
        beta = self.beta_min + (self.beta_max - self.beta_min) * cube[-1]
        theta = self.power_gaussian_quantile(cube=cube[:self.nDims], beta=beta)
        return np.concatenate([theta, [beta]])


def _erf_term(d, b, g):
    @lru_cache(maxsize=256)
    def helper(t_delta, t_beta, t_sigma):
        hd, hg = np.array(t_delta), np.array(t_sigma)
        return np.erf(hd * np.sqrt(t_beta/2) / hg)

    return helper(tuple(d), b, tuple(g))


def power_posterior_proposal(bounds: np.ndarray,
                             mean: np.ndarray,
                             covmat: np.ndarray,
                             nDims,
                             loglike: callable = None,
                             logzero: np.float64 = -1e30):
    """Produce the power posterior proposal."""
    prior = PowerPosteriorPrior(mean, covmat, logzero, nDims, bounds=bounds)

    return Proposal(prior, loglike, nDims=len(mean)+1)
