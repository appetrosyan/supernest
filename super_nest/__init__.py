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
