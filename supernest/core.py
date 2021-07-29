r"""Module containing superimpose and a gaussian proposal.

The usage is as follows. Normally the proposal is approximated by a
correlated Gaussian distribution. We (for now) approximate that
further to a spherically symmetric gaussian and use that as the guide
for nested sampling.

Afterwards, the important step is to put the Gaussian proposal into a
superpositional mixture.  This is done via a functional interface for
ease and portability.

"""
from random import random, seed
from numpy import concatenate, sqrt, log, pi, array, ndarray, zeros, isclose
from scipy.special import erf, erfinv
from scipy.stats import truncnorm
from collections import namedtuple

Proposal = namedtuple("Proposal", ['prior', 'likelihood'])
NDProposal = namedtuple("NDProposal", ['nDims', 'prior', 'likelihood'])


def superimpose(models: list, nDims: int = None):
    r"""Superimpose functions for use in nested sampling packages.

    Parameters
    ----------
    models: list(tuples(callable, callable))

    This is a list of pairs of functions. The first functions
    (quantile-like) will be interpreted as prior quantiles. They will
    be made to accept extra arguments from the hypercube, and produce
    extra parameters as output.

    The secondary function will be made to accept extra parameters,
    and ignore all but the last parameter. The functions need to be a
    consistent partitioning of the model, as described in the
    stochastic superpositional mixing paper in mnras.

    In short, if the prior spaces to which the two functions coorepond
    is the same, for all functions, you only need to make sure that
    the product of the prior pdf and the likelihood pdf is the same
    acroos different elemtns of the tuple. If they are not the same,
    you must make sure that the integral of their product over each
    prior space is the same, and that the points which correspond to
    the same locations in the hypercube align.

    nDims=None: int
    Optionally, if you want to have `superimpose`
    produce a number of dimensions for use with e.g. PolyChord, and to
    guard againt changes in the calling conventions and API, just pass
    the nDims that you would pass to PolyChord.Settings, and the
    run_polychord function.

    validate_quantiles=False: bool
    if nDims is passed, makes sure that the prior
    quantiles accept points in the entire hypercube.

    validate_likelihood=False: bool
    if nDims is passed, makes sure that the likelihood
    functions are well-bevahed in the hypercube.
    Don't use with slow likelihood functions.


    Returns
    -------
    (prior_quantile: callable, likelihood: callable) : tuple
    if nDims is None,
    returns a tuple of functions: the superposition of the prior
    quantiles and the likelihoods (in that order).

    (nDims: int, prior_quantile: callable, likelihood: callable): tuple
    if the optional argument nDims is not None, the output also
    contains an nDims: the number of dimensions that you should ask
    your dimesnional sampler to pass.

    """
    priors, likes = [p for p, _ in models], [l for _, l in models]

    def prior_quantile(cube):
        physical_params = cube[:-len(models)]
        choice_params = cube[-len(models):-1]
        index = 0
        norm = choice_params.sum()
        norm = 1 if norm == 0 or len(choice_params) == 1 else norm
        probs = choice_params / norm
        h = hash(tuple(physical_params))
        seed(h)
        rand = random()
        for p in probs:
            if rand > p:
                break
            index += 1
        theta = priors[index](physical_params)
        ret = array(concatenate([theta, probs, [index]]))
        return ret

    def likelihood(theta):
        try:
            physical_params = theta[:-len(models)]
        except SystemError:
            print(f'{theta = } {len(models) =} {theta[:-len(models)]}')
            physical_params = theta[:-len(models)]
        index = int(theta[-1:].item())
        ret = likes[index](physical_params)
        return ret

    if nDims is not None:
        return NDProposal(nDims + len(models), prior_quantile, likelihood)
    else:
        return Proposal(prior_quantile, likelihood)


def _eitheriter(ab):
    a, b = ab
    return hasattr(a, '__iter__') or hasattr(b, '__iterb__')


def __snap_to_edges(cube, theta, a, b):
    # TODO use cython for efficient indexing.
    ret = theta
    for i in range(len(cube)):
        if isclose(cube[i], 0):
            ret[i] = a[i]
        elif isclose(cube[i], 1):
            ret[i] = b[i]
        else:
            pass
    return ret


def gaussian_proposal(bounds: ndarray,
                      mean: ndarray,
                      stdev: ndarray,
                      loglike: callable = None):
    r"""Produce Gaussian proposal.

    Given a uniform prior defined by bounds, it produces a gaussian
    prior quantile and a correction to the log-likelihood.

    If the loglike parameter is passed the returned is already a
    wrapped function (you don't need to wrap it in a callable yourself).

    This should be your first, and perhaps last point of call,

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
    stdev, a, b = _process_stdev(stdev, mean, bounds)
    RT2, RTG = sqrt(2), sqrt(1 / 2) / stdev
    da = erf((a - mean) * RTG)
    db = erf((b - mean) * RTG)
    log_box = log(b - a).sum() if _eitheriter(
        (a, b)) else len(mean) * log(b - a)
    log_box = -log_box

    def __quantile(cube):
        theta = erfinv((1 - cube) * da + cube * db)
        theta = mean + RT2 * stdev * theta
        theta = __snap_to_edges(cube, theta, a, b)
        return theta

    def __correction(theta):
        if loglike is None:
            ll, phi = 0, []
        else:
            ll, phi = loglike(theta)
        corr = -((theta - mean)**2) / (2 * stdev**2)
        corr -= log(2 * pi * stdev**2) / 2
        corr -= log((db - da) / 2)
        corr = corr.sum()
        return (ll - corr + log_box), phi

    return Proposal(__quantile, __correction)


def _process_stdev(stdev, mean, bounds):
    if isinstance(stdev, float):
        stdev = zeros(len(mean)) + stdev
    elif len(mean) != len(stdev):
        raise ValueError(
            'mean and covariance are of incompatible lengths. {} {}'.format(
                len(mean), len(stdev)))
    else:
        try:
            if len(stdev[0]) != len(mean):
                raise ValueError(
                    'Dimensions of stdev and mean don\'t match'
                    + f'{len(stdev)=} vs {len(mean)=}'
                )
        except TypeError:
            pass

    try:
        a, b = bounds
    except ValueError:
        a, b = bounds.T
    try:
        stdev = stdev.diagonal()
    except ValueError:
        pass
    return stdev, a, b
