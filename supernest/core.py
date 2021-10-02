r"""Module containing `superimpose` and `gaussian_proposal`s.

Normally the proposal is approximated by a correlated Gaussian
distribution. We (for now) approximate that further to a spherically
symmetric gaussian and use that as the guide for nested sampling.

Afterwards, the important step is to put the Gaussian proposal into a
superpositional mixture.  This is done via a functional interface for
ease and portability.

"""
import random
import numpy as np
import numpy.linalg
import warnings
from supernest.utils import snap_to_edges, process_stdev
import supernest.proposals as prop

debug = False


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


    Returns
    -------
    (prior_quantile: callable, likelihood: callable) : tuple
    returns a tuple of functions: the superposition of the prior
    quantiles and the likelihoods (in that order).

    """
    proposals = [prop.Proposal(*m) for m in models]
    priors = [p.prior for p in proposals]
    likes = [p.likelihood for p in proposals]

    def prior_quantile(cube):
        physical_params = cube[:-len(models)]
        choice_params = cube[-len(models):-1]
        index = 0
        norm = choice_params.sum()
        norm = 1 if norm == 0 or len(choice_params) == 1 else norm
        probs = choice_params / norm
        h = hash(tuple(physical_params))
        random.seed(h)
        rand = random.random()
        for p in probs:
            if rand > p:
                break
            index += 1
        theta = priors[index](physical_params)
        ret = np.array(np.concatenate([theta, probs, [index]]))
        return ret

    def likelihood(theta):
        try:
            physical_params = theta[:-len(models)]
        except SystemError:
            warnings.warn(f'theta = {theta} {theta[:-len(models)]}')
            physical_params = theta[:-len(models)]
        index = int(theta[-1:].item())
        ret = likes[index](physical_params)
        return ret

    return prop.Proposal(prior_quantile, likelihood, nDims if nDims is None else nDims + len(models))
