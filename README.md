# Table of Contents

1.  [SuperNest](#orgf827d34)
2.  [installation](#org5c67b97)
3.  [How to](#orgf74ac45)
	1.  [Motivation](#org2d127d6)
	2.  [Proposals](#org77cac4d)
	3.  [Stochastic mixing](#orge7c404c)
	4.  [The framework](#orge3fe113)
4.  [Contributing](#org9b33408)
5.  [License.](#orgcef4d1e)


<a id="orgf827d34"></a>

# SuperNest

A package to perform stochastic superpositional mixing of proposal
priors for nested sampling engines such as
[PolyChord](https://pypi.org/project/pypolychord/) and
[Dynesty.](https://pypi.org/project/dynesty/)


<a id="org5c67b97"></a>

# installation

```bash
pip install supernest
```

<a id="orgf74ac45"></a>

# How to

If you are already using a considerable amount of nested sampling
code, then you might want to use the package `supernest` as is. This
provides you the bare minimum you need to get started.

The following assumes that you are familiar with the terminology
used in Bayesian inference, i.e. you know different methods of
specifying probability distributions, know what a prior, likelihood,
evidence and posterior represent, and have used nested sampling a
little bit.


<a id="org2d127d6"></a>

## Motivation

Say you have a model that you want to investigate. In order to do
that with PolyChord, you need to provide the model in the form of a
prior quantile function (also the point-percent function) and a
corresponding likelihood probability density function.

If you want to make it go faster, the prior should more closely
resemble posterior distribution, i.e. if it's a Gaussian posterior
you expect in the middle of the hard boundaries, then it's a
Gaussian quantile that you need to use.

The problem is that unlike e.g. Metropolis-Hastings or other
methods of Bayesian inference (that do not evaluate evidence),
nested sampling cannot distinguish between a prior quantile that is
physically based, or a prior quantile that is just a "hunch". Thus,
if you want to get useful data out of each nested sampling run, you
actually almost always have to use a uniform prior, which is also
the slowest.

Stochastic superpositional mixing allows you to use the intuitive
proposals but without them actually ruining your sampling run, by
not sampling in the areas where the proposal predicts no prior
density (and there is) or computing the wrong evidence.


<a id="org77cac4d"></a>

## Proposals

For Stochastic superpositional posterior repartitioning to work,
one needs to have well-tuned proposals.

A thorough overview of how to do that is available in the main
article (TODO), but as a baseline, you should do the following.

First you need a prior quantile that represents where you expect to
find the answer, e.g. if you expect to sample over the
gravitational acceleration on earth, then you should get a quantile
of a Gaussian for that parameter that is centered around 9.8 and
has reasonable breadth (but not too wide).

Then as described [here](https://arxiv.org/pdf/1908.04655.pdf), you
should make sure that the product of the prior probability density
function times the likelihood function is the same as of the original
model everywhere in the domain.

To avoid tedious calculations a function that computes a Gaussian
quantile and a proposal log-likelihood is provided:
```python
from supernest import gaussian_proposal

proposal_prior, proposal_loglike = gaussian_proposal(
	bounds=bounds_of_uniform_prior,
	mean=means_of_proposal_distribution,
   	stdev=diagonal_elements_of_covariance_matrix,
   	bounded=False,
   	loglike=original_log_like)
```

<a id="orge7c404c"></a>

## Stochastic mixing

Using the proposals directly if you aren't sure that they exactly
coincide with the posteriors is dangerous (and defeats the purpose
of doing nested sampling, as you would get the right answer only if
the proposal was also exactly correct).

Instead, you should use `supernest` to produce a stochastic
superposition of the models that you have.

The best way to do it, is to use the `supernest.superimpose`
function.

```python
from supernest import superimpose

super_n_dims, super_prior, super_like = superimpose(
    [(original_prior, original_log_like), (proposal_prior, proposal_loglike)],
    original_n_dims)
```

After which you can use the functions in any of the samplers of
your choosing. For example, `pymultinest`

```python
from pymultinest import solve

solve(LogLikelihood=super_like, Prior=super_prior, n_dims=super_n_dims,
   	  outputfiles=outputfiles)
```
# Contributing

Please read [Contributing.md](./CONTRIBUTING.md).  TL; DR: do not
worry and ask if in doubt.


# License

LGPLv3
