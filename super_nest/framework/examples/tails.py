from numpy import array, diag

from super_nest.framework.gaussian_models import PowerPosteriorPrior, BoxUniformPrior

mu = array([1, 2, 3])
cov = diag([1, 1, 1])
a = 6 * 10 ** 8
bounds = (-array([a, a, a]), array([a, a, a]))

args = [bounds, mu, cov]
kwargs = {
    'resume': False,
    'live_points': 20
}

models = {
    'uniform': BoxUniformPrior(*args),
    'ppr': PowerPosteriorPrior(*args)
}

answers = {k: models[k].nested_sample(**kwargs) for k in models}
q = answers['uniform'][1]
