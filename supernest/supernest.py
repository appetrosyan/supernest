"""This package contains the only important function superimpose. The
submodule `super_nest.framework` is included for more complex tasks
that involve complicated models and custom code, and offer a much
better user experience, compared to base `super_nest`.

The usage is as follows.

Let models be denoted by a tuple (pi, lgL), where pi is the
prior_quantile function (or prior point-percent function) and the
likelihood, is represented by its logarithm.

Normally you\'d run a nested sampler like

sampler.sample(pi, nDims, lgL, nDerived).

Using `super_nest`, you can accelerate the inference, by providing it
extra information in terms of an extra prior and an extra lilelihood
pair (pi_p, lgL_p), which are normalied such that:

pi.pdf(x) * L.pdf(x) = pi_p.pdf(x) * L_p.pdf(x)

Then yuou can put them into a stochastic mixture, by using superimpose, e.g.

pi_m, lgL_m = super_nest.superimpose([(pi, lgL), (pi_p, lgL_p)])

and then use it as you would pi and lgL. The result is a sampling run
that is roughly 30 times faster and 100 times more precise. I could
speculate about the accuracy, i.e. that within the confines of testing
of a masters\' thesis project, I haven\' found anything that would not
work and bias the output, but that\'s hardly a high standard of
testing.
"""
from random import random, seed
from numpy import concatenate, sqrt, log, pi
from scipy.special import erf, erfinv


def superimpose(models: list, nDims: int = None):
    """Superimpose functions for use in nested sampling packages such
    as PolyChord, PyMultiNest and dynesty.

    Parameters
    ----------
    models :list(tuples(callable, callable))

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
    Don\'t use with slow likelihood functions.


    Returns
    -------
    (prior_quantile: callable, likelihood: callable) : tuple
    if nDims is None,
    returns a tuple of functions: the superposition of the prior
    quantiles and the likelihoods (in that order).

    (nDims :int, prior_quantile: callable, likelihood: callable) : tuple
    if the optional argument nDims is not None, the output also
    contains an nDims: the number of dimensions that you should ask
    your dimesnional sampler to pass.

    """
    priors, likes = [prior for prior, _ in models], [
        like for _, like in models]

    def prior_quantile(cube):
        physical_params = cube[:-len(models)]
        choice_params = cube[-len(models):-1]
        index = 0
        norm = choice_params.sum()
        norm = 1 if norm == 0 else norm
        ps = choice_params / norm
        h = hash(tuple(physical_params))
        seed(h)
        r = random()
        for p in ps:
            if r > p:
                break
            index += 1
        theta = priors[index](physical_params)
        return concatenate([theta, ps, [index]])

    def likelihood(theta):
        physical_params = theta[:-len(models)]
        index = int(theta[-1:].item())
        return likes[index](physical_params)

    if nDims is not None:
        return nDims+len(models), prior_quantile, likelihood
    else:
        return prior_quantile, likelihood


def _eitheriter(ab):
    a, b = ab
    return hasattr(a, '__iter__') or hasattr(b, '__iter__')


def gaussian_proposal(bounds, mean, stdev, bounded=False, loglike=None):
    """This function provides the most common type of proposal that\'s
    acceptable into Stochastic mixtures. Given a uniform prior defined
    by bounds, it produces a gaussian prior quantile and a correction
    to the log-likelihood.

    If the loglike parameter is passed the returned is already a
    wrapped function (you don\'t need to wrap it in a callable yourself).

    This should be your first, and perhaps last point of call,

    Parameters
    ----------
    bounds : array-like
    A tuple that represents the original uniform prior.


    mean : array-like
    The vector \\mu at which the proposal is to be centered.

    stdev : array-like
    The vector of standard deviations. Currently only
    uncorrelated Gaussians are supported.

    bounded : bool, optional
    Currently the algorithm produces
    untruncated Gaussians. In the future, once the boundary effects
    have been thoroughly examined, this will be supported.

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
    if bounded:
        raise NotImplementedError(
            'Truncated gaussian proprosals are not yet implemented.')
    if len(mean) != len(stdev):
        raise ValueError(
            'mean and covariance are of incompatible lengths. {} {}'
            .format(len(mean), len(stdev)))
    try:
        if len(stdev[0]) != len(mean):
            raise NotImplementedError('Covariance matrices are not supported.')
    except TypeError:
        pass

    a, b = bounds
    RT2, RTG = sqrt(2), sqrt(1/2)/stdev
    da = erf((a-mean)*RTG)
    db = erf((b-mean)*RTG)
    log_box = log(b-a).sum() if _eitheriter((a, b)) else len(mean)*log(b-a)

    def quantile_(cube):
        theta_ = erfinv((1-cube)*da + cube*db)
        return mean + RT2*stdev*theta_

    def correction_(theta):
        if loglike is None:
            ll, phi_ = 0, []
        else:
            ll, phi_ = loglike(theta)
            corr = -((theta-mean)**2) / (2*stdev**2)
            corr -= log((pi*stdev**2)/2)/2
            corr -= log(db-da)
            return ll+corr-log_box, phi_

    return quantile_, correction_
