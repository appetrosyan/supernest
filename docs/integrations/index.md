---
outline: deep
---
# Nested Samplers

## PolyChord

Supernest was historically designed around PolyChord and provided an
OOP-like interface to take care of most of your housekeeping.

However it later became apparent that with a minimal modification to
the API, one can extend `supernest` to work with other samplers.  The
issue is that for this to work, some of the housekeeping is delegated
onto the user.

As per usual, you start by wrapping the prior functions:
```python
from supernest import superimpose

super_n_dims, super_prior, super_like = superimpose(
	[(original_prior, original_log_like), (proposal_prior, proposal_loglike)],
	original_n_dims)
```

If any of this is confusing refer to the API documentation.

::: warning
This exact API is subject to change.
:::

## MultiNest

`PyMultiNest` has a very similar API to PolyChord, owing to it being a Python library.

```python
from pymultinest import solve

solve(LogLikelihood=super_like, Prior=super_prior, n_dims=super_n_dims,
	  outputfiles=outputfiles)
```

::: warning

Integration with the FORTRAN framework MultiNest is planned.

:::

::: warning

This doesn't exactly mean that everything shall work out of the box,
`PyMultiNest` wasn't tested as extensively as PolyChord.
:::

## DyNesty

::: danger

DyNesty is not integrated.

:::

## DyPolyChord

::: danger

DyPolyChord is not integrated.

:::


## NestorFlow

::: danger

NestorFlow is not integrated.

:::

# Cosmological Inference Software

## Cobaya

Historically the cobaya sampler framework has been integrated into the
original supernest.

Unfortunately, that work was never upstreamed and now the work has to
be done from scratch.

::: danger

Cobaya is not integrated.

:::

## CosmoChord

CosmoChord is a fork of CosmoMC that uses the PolyChord sampler in
FORTRAN. As this is similar in scope to the integration with
MultiNest, one should expect both to be handled at a similar time.


::: danger

CosmoChord is not integrated.

:::
