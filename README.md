SuperNest
=========

A package to perform stochastic superpositional mixing of proposal
priors for nested sampling engines such as
[PolyChord](https://pypi.org/project/pypolychord/) and
[Dynesty.](https://pypi.org/project/dynesty/)

installation
============

```bash
pip install supernest
```

How to
======

If you are already using a considerable amount of nested sampling code,
then you might want to use the package `supernest` as is. This provides
you the bare minimum you need to get started.

The following assumes that you are familiar with the terminology used in
Bayesian inference, i.e. you know different methods of specifying
probability distributions, know what a prior, likelihood, evidence and
posterior represent, and have used nested sampling a little bit.

Motivation
----------

Say you have a model that you want to investigate. In order to do that
with PolyChord, you need to provide the model in the form of a prior
quantile function (also the point-percent function) and a corresponding
likelihood probability density function.

If you want to make it go faster, the prior should more closely resemble
posterior distribution, i.e. if it\'s a Gaussian posterior you expect in
the middle of the hard boundaries, then it\'s a Gaussian quantile that
you need to use.

The problem is that unlike e.g. Metropolis-Hastings or other methods of
Bayesian inference (that do not evaluate evidence), nested sampling
cannot distinguish between a prior quantile that is physically based, or
a prior quantile that is just a \"hunch\". Thus, if you want to get
useful data out of each nested sampling run, you actually almost always
have to use a uniform prior, which is also the slowest.

Stochastic superpositional mixing allows you to use the intuitive
proposals but without them actually ruining your sampling run, by not
sampling in the areas where the proposal predicts no prior density (and
there is) or computing the wrong evidence.

Proposals
---------

For Stochastic superpositional posterior repartitioning to work, one
needs to have well-tuned proposals.

A thorough overview of how to do that is available in the main article
(TODO), but as a baseline, you should do the following.

First you need a prior quantile that represents where you expect to find
the answer, e.g. if you expect to sample over the gravitational
acceleration on earth, then you should get a quantile of a Gaussian for
that parameter that is centered around 9.8 and has reasonable breadth
(but not too wide).

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

Stochastic mixing
-----------------

Using the proposals directly if you aren\'t sure that they exactly
coincide with the posteriors is dangerous (and defeats the purpose of
doing nested sampling, as you would get the right answer only if the
proposal was also exactly correct).

Instead, you should use `supernest` to produce a stochastic
superposition of the models that you have.

The best way to do it, is to use the `supernest.superimpose` function.

```python
from supernest import superimpose

super_n_dims, super_prior, super_like = superimpose(
    [(original_prior, original_log_like), (proposal_prior, proposal_loglike)],
    original_n_dims)
```

After which you can use the functions in any of the samplers of your
choosing. For example, `pymultinest`

``` python
from pymultinest import solve

solve(LogLikelihood=super_like, Prior=super_prior, n_dims=super_n_dims,
      outputfiles=outputfiles)
```

The framework
-------------

`supernest` comes with a convenient OOP-based wrapper for PolyChord.
It\'s feature packed and much more easy to work with as you don\'t need
to separately track the number of dimensions of your problem.

As of now it only supports PolyChord, as the features don\'t play well
with other samplers, e.g. dynamic samplers (`dyPolychord`, `dynesty`,
`nestorflow`), and samplers that depend highly on the smoothness of the
prior distribution (`multinest`).

The idea is that you do rapid prototyping using the provided parameter
covariance templates, and eventually subclass the
`supernest.framework.polychord.Model`, and run PolyChord as is. Of
course, this will extend further to a successor to PolyChord that uses
the idea of superpositional mixtures as a first-class citizen, and thus,
`supernest` will eventually become a Python front-end for that nested
sampler.

Contributing
============

I don\'t like Python, so I don\'t follow most of the best practices
(because I think that they exasperate Python\'s weaknesses). Of course
if you feel that some things can be made better (i.e. follow the
aforementioned guidelines and best practices) I will accept a Merge
request.

The project lives on Gitlab. The Github repository is a (push) mirror,
hence if you create a pull request, I would prefer if you copied the
code and pushed to Gitlab.

Why? Well, I\'m glad you asked. Gitlab is 100% FOSS, and has no ties to
an unethical company (yet). They have integrated CI, and a ratehr robust
system for managing private repositories (up until recently, GitHub
didn\'t have that).

License.
========

LGPLv3.

Without getting too technical, you this is a permissive non-viral
license that\'s GPL3 compatible.

It\'s not quite MIT or BSD, but for the non-legal speaking user they are
effectively the same.
