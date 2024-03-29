"""This is the reference implementation of the superpositional
stochastic mixture, that was used to generate my entire master\'s
thesis. 

Pass any of the mixture Models a list of models, and you\'d get the
proper mixture of the type that you needed. You mostly want to use the
stochastic mixture.

"""

from abc import ABC
from random import random, seed

from numpy import concatenate

from .polychord import Model


def _are_all_elements_identical(lst):
    return not lst or lst.count(lst[0]) == len(lst)


class AbstractMixtureModel(Model, ABC):
    """This is the abstract base class that defines a general mixture. If
    you either have your own implementation of a superpositional
    mixture, or have a different idea entirely, for a mixture of
    several models, you want to subclass this one. 


    Most of the heavy lifiting is figureing out the dimesnionality for
    arbitrary model inputs, and figuring out an efficient log_like and
    prior_quantile.

    """
    default_file_root = 'MixtureModel'

    def __str__(self):
        return f'\nMixture of \n{self.models}'

    def __init__(self, models, file_root=default_file_root, **kwargs):
        self.models = models
        if not _are_all_elements_identical([x.nDims for x in models]):
            raise ValueError(
                "Models in mixture have different dimensionality.")
        self.nDims = max([x.dimensionality for x in models])
        if not _are_all_elements_identical([x.num_derived for x in models]):
            raise ValueError(
                "Models in mixture have different derived parameters.")
        self.nDerived = models[0].num_derived
        super().__init__(self.dimensionality, self.num_derived, file_root, **kwargs)

    def test_quantile(self):
        __doc__ = super().__doc__
        for m in self.models:
            m.test_quantile()
        super().test_quantile()

    def test_log_like(self):
        __doc__ = super().__doc__
        for m in self.models:
            m.test_log_like()
        super().test_log_like()

    @property
    def num_derived(self):
        __doc__ = super().__doc__
        return self.nDerived


class StochasticMixtureModel(AbstractMixtureModel):
    """This is a stochastic mixture model. As described in my Masters'
    thesis also available at https://github.com/appetrosyan/LCDM-NS/

    Initially the `super_nest.superimpose` function was a carbon copy
    of this method. However, I didn't want to impose on the user the
    requirement to keep track of dimensionality, so I decided to cut
    all of the dimensionality management and reserve it for the
    framework proper.

    """
    default_file_root = 'StochasticMixture'

    def __init__(self, models, settings=None, file_root=default_file_root):
        super().__init__(models, file_root=file_root, settings=settings)

    @property
    def dimensionality(self):
        __doc__ = super().dimensionality.__doc__
        return self.nDims + len(self.models)

    def _unpack(self, theta):
        physical_params = theta[:self.nDims]
        choice_probabilities = theta[self.nDims:-1]
        index = theta[-1:].item()
        return physical_params, choice_probabilities, index

    def log_likelihood(self, theta):
        __doc__ = super().__doc__
        t, _, m = self._unpack(theta)
        _current_model = self.models[int(m)]
        _nDims = _current_model.dimensionality
        log_l, phi = _current_model.log_likelihood(t[:_nDims])
        return log_l, phi

    def prior_quantile(self, hypercube):
        __doc__ = super().__doc__ 
        t, b, _ = self._unpack(hypercube)
        norm = b.sum() if b.sum() != 0 else 1
        ps = b / norm
        index = 0
        h = hash(tuple(t))
        seed(h)
        r = random()
        for p in ps:
            if r > p:
                break
            index += 1
        _nDims = self.models[index].dimensionality
        cube, cube_ = t[:_nDims], t[_nDims:]
        theta = self.models[index].prior_quantile(cube)
        return concatenate([theta, cube_, b, [index]])
