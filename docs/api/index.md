---
outline: deep
---

# Introduction

Supernest is a package for accelerating Bayesian inference for
algorithms that are sensitive to the boundary between prior and likelihood.

::: warning
If this sounds like gibberish to you, perhaps you should start with McKay, and readon on about Bayesian inference.
:::

This means Nested Sampling (todo: cite Skilling), and to a greater
extent newer algorithms some of which are based on nested sampling and
some of which were designed as a consequence of `supernest`.

# How to use this

The simple answer is that you should view this as an interactive
guided tour of what you can and should do in particular situations
with Bayseian Inference.

The `supernest` package is integrated with particular tools, such as
e.g. the Cobaya sampler, which shall be covered in a separate section
both here and in the `cobaya` tutorial.

While  there is  planned integration  with  other tools,  if it's  not
stated here, then the tool is not ready for production.

# Licensing and Attribution

The main code for the `supernest` package is licensed under **LGPLv3**.

::: info
This means that you **can** use it at no extra cost in your commercial project.
:::


::: warning
This also means that you would need to make any code improvements
available upstream (that is, here).
:::

::: warning
However, you **must** respect the attribution rights, that is you must
cite the `supernest` paper, (once that is finalised, it will be linked
here), if you used it.
:::

Generally speaking if what you're doing is open source, just linking
to this documentation, or mentioning me as the author should be
sufficient.  If you're writing an academic publication, citing me
would greatly help justifying spedning more time on it.
