# SSPR

Stochastic superpositional posterior repartitioning used in
conjunction with Bayesian inference engines such as PolyChord and
MultiNest.

# What is Bayesian inference

Bayesian inference is a suitable framework for model fitting.  You
give it a theory and some data and it tells you how well the theory
fits the data, while also telling you what the theory's parameters
should be for the fit to be the best.

# Installation

The preferred way is to use 
```
pip install super-nest
```

though other packages will be developed as needed.

If you know what you're doing you can clone this repository and
install manually, using

```
cd super-nest && python3 setup.py
```

You also need to have either
[PolyChord](https://github.com/PolyChord/PolyChordLite) or
[MultiNest](https://github.com/farhanferoz/MultiNest) (or both)
installed.
# Usage

This is planned as a simple convenient package that you use with a sampler. 

Suppose that you had a set-up with `PolyChord` that involved a prior
quantile `prior` a log-likelihood function, `loglike` all of which
operated on an `nDims` dimensional space. 

Often you'd be using a uniform prior. You're sure that using a
different prior would cause an imprint, which is fine if that prior
was based on a previous run, but not so if you just used it as a
hunch. As hunch is used liberally here, you could have an intuition,
or you could have done a run using a different model and extrapolated
the posterior. 

Previously all such information could not be used. Nested sampling
would return all of that information to you and you wouldn't be able
to tell, if this is actually what the data suggests, or that you
simply gave it too much info out of thin air.

Well, now you can use that information and get your sampling to run
faster, but to produce the output you would have gotten had you used a
uniform prior (and a lot more live points).

## General overview.
Suppose you had a unfirom prior `pi` and likelihood `l`. To use them
in nested sampling, you need a prior quantile, and the logarithm of
the likelihood. You need to pass both to the sampler, e.g.
```
settings= PolyChordSettings(nDims, nDerived, ...)
run_polychord(log(l), functional_inverse(cumulative_dist(pi)), nDims,
nDerived ...)  
``` 
if the prior is uniform (a function that maps to a
constant), you expect the quantile to be dependent on the boundaries
of your prior space. If you have a box with corners at `a` and `b`,
then the uniform prior quantile is:
```
def quantile(cube):
	return a + (b-a)*cube
```

Let's say you have a hunch that the posterior would be a Gaussian at
`mu` with covariance matrix `Sigma`. How do you formulate it in such a
way that supernest can understand?

Well, for starters, the prior quantile would look like
```
def gaussian_quantile(cube):
	def _erf_term(d, g):
			return erf(d * sqrt(1 / 2) / g)
	sigma = diag(m.cov)
    da = _erf_term(a - mu, sigma)
    db = _erf_term(b - mu, sigma)
    ret = erfinv((1 - cube) * da + cube * db)
    return mu + sqrt(2 / beta) * sigma * ret
```
which is already quite a mouthful. If you tried to use this quantile directly, you would have a few problems:

1) Your posterior will have a Gaussian imprint at `mu` and `Sigma`,
whether or not you want it.
2) If most of your posterior is far away, it would have been picked up by the uniform prior, but not the one you
have.
3) You would get the wrong (larger) evidence than you would with a uniform prior. 

So what do you do?

## Creating a proposal. 

You create a consistent proposal. This means that you need to change the likelihood specifically, you need to make it so that the product of the prior pdf and the new likelihood is the same as the original uniform prior times the original `log(l)`. 

So what do you do for a Gaussian? Well, it's easy:

```
def logl_gaussian(theta):
	ll=0
	def ln_z(t, b):
        ret = - b * (t - mu) ** 2 / 2 / sigma ** 2
        ret -= log(pi * sigma ** 2 / 2 / b) / 2
        db = _erf_term(b - mu, sigma)
        da = _erf_term(a - mu, sigma)
        ret -= log(db - da)
        return ret
		
	ll -= log(b-a).sum()
    ll -= ln_z(theta, beta).sum()

    return ll
```

And then you pass it and it works? **Wrong**. This will help you with
the wrong evidence, but you would still get an imprint in the
posterior, and sampling far away would still be an issue.

## Using this package. 
To solve the problem you need to put both your original prior and
likelihood and the newly created gaussian proposa. into a
superposition. This what this package does, and this is what this package is. 

So to use the things that we've defined previously, we should do the
following: (I'm assuming polyChord, but this works with **any** nested
sampler).

```
from polychord import run_polychord
from polychord.settings import PolyChordSettings
from supernest import superimpose


def uniform_quantile(cube):
	...
	
	
def uniform_like(theta):
	...
	return log(l), derived
	
	
def gaussian_quantile(cube):
	...
	

# In later versions, you will have a function that generates the correctsion for you. 
def gaussian_like(theta):
    ...
	
# Note taht you can have as many proposals as you like. 
n_dims, prior, log_like = superimpose([(uniform_prior, uniform_like), (gaussian_prior, gaussian_like), ...], nDims)

...

# Be wary of using grade_dims and grade_frac. If you have n models, you should 
# grade_dims.append(n)
# grade_frac.append([1.0]*n)
# before passing them to settings. 

settings = PolyChordSettings(n_dims,nDerived, ...)

...

run_polychord(prior, n_dims, nDerived, log_like, ...)
```
## What do I get in return for my work?

A run-time reduction starting at 37x. A precision increase of about
100x. The posterior you get should contain all the usual stuff, plus
some extra parameters at the end, which tell you how good your
proposals were. These should be interpreted as probabilities that the
proposal described the posterior.

## Is this the best that superpositional mixtures have to offer. 

Not at all. We're writing a purpose built sampler that eliminates all
outward appearances of using superposition under the hood, while also
making use of some clever tricks, that you normally can't
do. Effectively we're creating a quantum computer of nested samplers.

# Does this support the X sampler. 
Yes. This is a very thin module, and while I have assumed a
`PolyChord`-like calling convention (also `dynesty`), you can use it
with other samplers that support using python functions as callbacks.

## Pymultinest
Very similar to PolyChord, (and also quite popular). Use as follows:
```
from super_nest import superimpose

n_dims, my_prior_quantile, my_likelihood = superimpose([(prior1, like1), (proposal_prior1, proposal_like1)], nDims)
solve(LogLikelihood= my_likelihood, Prior= my_prior_quantile, n_dims = n_dims)
```

## dynesty


# What is this useful for 

Suppose that you were running a complex Bayesian inference,
e.g. [Cobaya](https://cobaya.readthedocs.io/en/latest/). You have a
choice of sampler, e.g. Monte-Carlo, Metropolis Hastings or you could
choose to use Nested Sampling, among a family of other inference
methods. If you choose the former, you get a good idea of what the
model parameters should be quick, but you have no idea how good the
fit is, because MCMC and MH don't evaluate the evidence. You think to
use Nested Sampling, but that takes too long, and you can't give it
more information to run faster... At least not without this package.

This is a thin wrapper around both PolyChord and Multinest's code,
that allows you to specify a proposal distribution. For now it's
mainly a multivariate correlated Gaussian, but other distributions are
being planned.

## How much faster/more precise can this make inference? 

Our preliminary academic benchmarks showed a runtime reduction by a
factor of 20. Your mileage may vary, but if you're willing to
sacrifice some precision, you can make it go even faster.

If you really want the extra precision, you can expect an uplift by
two orders of magnitude, if you started with a uniform prior (as we
often do in nested sampling) and used the posterior chains to generate
the distribution.


# License - MIT

