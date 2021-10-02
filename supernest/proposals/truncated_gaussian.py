import numpy as np
import scipy.special as sp
import supernest.utils as utils
import warnings
from supernest.proposals.types import Prior, Likelihood, Proposal


def truncated_gaussian_proposal(bounds: np.ndarray,
                                mean: np.ndarray,
                                stdev: np.ndarray,
                                loglike: callable = None):
    r"""Produce a truncated Gaussian proposal.

    Given a uniform prior defined by bounds, it produces a gaussian
    prior quantile and a correction to the log-likelihood.

    Parameters
    ----------
    bounds : array-like
        A tuple with bounds of the original uniform prior.

    mean : array-like
        The vector \mu at which the proposal is to be centered.

    stdev : array-like
        The vector of standard deviations. Currently only
        uncorrelated Gaussians are supported.

    loglike: callable: (array-like) -> (real, array-like), optional
        The callable that constitutes the model likelihood.  If provided
        will be included in the output. Otherwise assumed to be
        lambda () -> 0


    Returns
    -------
    (prior_quantile, loglike_corrected): tuple(callable, callable)
    This is the output to be used in the stochastic mixing. You can
    use it directly, if you\'re certain that this is the exact shape of
    the posterior. Any deviation, however, will be strongly imprinted
    in the posterior, so you should think carefully before doing this.

    """
    stdev, a, b = utils.process_stdev(stdev, mean, bounds)
    # truncation requires the covmat to be diagonal
    try:
        stdev = np.sqrt(stdev.diagonal())
    except ValueError:
        warnings.warn(f'stdev={stdev} couldn\'t be diagonalised')
    log_box = np.log(b - a).sum() if utils.eitheriter(
        (a, b)) else len(mean) * np.log(b - a)
    log_box = -log_box

    # Convenice variable to avoid duplicating code
    RT2, RTG = np.sqrt(2), np.sqrt(1 / 2) / stdev
    da = sp.erf((a - mean) * RTG)
    db = sp.erf((b - mean) * RTG)

    def quantile(cube):
        theta = RT2 * sp.erfinv((1 - cube) * da + cube * db)
        theta = mean + stdev * theta
        theta = utils.snap_to_edges(cube, theta, a, b)
        return theta

    def correction(theta):
        if loglike is None:
            ll, phi = 0, []
        else:
            ll, phi = loglike(theta)
        corr = -((theta - mean)**2) / (2 * stdev)
        corr -= np.log(2 * np.pi * stdev**2) / 2
        corr -= np.log((db - da) / 2)
        corr = corr.sum()
        return (ll - corr + log_box), phi

    return Proposal(Prior(quantile), Likelihood(correction), nDims=len(mean))
