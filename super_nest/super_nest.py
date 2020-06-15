from random import random, seed
from numpy import concatenate


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
    Don't use with slow likelihood functions.


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


