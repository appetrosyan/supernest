---
outline: deep
---
# Introduction

## Dependencies

In this example we shall be using the stack that had historically been
used to develop supernest.

### Sampler
One should firstly install `pypolychord`.

This project has historically been difficult to install, owing to
FORTRAN being an old lanugage with difficult to track dependencies,
and poor compiler support from modern GCC or LLVM.

We recommend following the official instructions (yours truly
contributed to the install process being tenable on Mac OS X).


### Plotting
We would then need a post-processing library.  One is welcome to do
kernel density estimations by hand, but it would be tiresome to do
with something like _e.g._ `gnuplot` so, we recommend using eitehr
`anesthetic` or `getdist`.

::: tip

While historically `anesthetic` has been used to develop `supernest`,
`getdist` is a more standard tool with a friendlier user interface,
and better architectural design decisions.

:::


::: details `nestcheck`
For additional insight, Edward Higson's `nestcheck` package is useful,
but not required.  It can, to some extent diagnose issues within the
nested sampling pipeline itself and warn about misbehaviour.

However, all work done with `nestcheck` is highly technical in nature
and only useful to those that want to grasp the concepts more
thoroughly, and not required for a quickstart.
:::

## Basic theory

In order to perform Bayesian inference, one needs to define two
probability functions: the _prior_ and the _likelihood_.  The precise
meanings of these terms are better described in specific books, but
for the time being, I would recommend one think of them as two
functions: `pi` and `logl`.

In mathematical terms the prior quantile probability function, `pi`
maps a point in the unit hypercube into the prior coordinate space.
We are mainly concerned with computationally simple models, so in this
guide we shall never cover anything more complicated than, _e.g._
mapping to a hyperrectangle and a Gaussian (more on that later).

The log-likelihood function `logl` is a much more straightforward
mapping.  It accepts points in the hyperrectangle generated by `pi`
and transforms them into a single number.  We conventionally operate
in logarithmic space, as almost all realistic distributions are going
to contain an exponential element to them, (including the so-called
banana distribution).

### Example model

Our example model is a single two-dimensional spherical Gaussian peak
with a uniform prior located in the hyperrectangle whose
2<sup>nd</sup> component is scaled by a factor of two.

This translates to the following prior quantile:

```python
def pi(cube):
	return np.array([cube[0], 2*cube[1]])
```

::: tip
The usage of an explicit list and conversion is done for the
readability's benefit, the next examples shall be better optimised, to
use `numpy` operations.
:::

The Gaussian is equally straightforward, but a tad more involved. 

::: danger
TODO
:::