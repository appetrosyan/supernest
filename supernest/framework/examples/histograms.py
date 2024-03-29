import matplotlib.pyplot as plt
import tikzplotlib
from matplotlib import rc
# from mpi4py import MPI
from numpy import array, sqrt, exp, pi, linspace

from supernest.framework.gaussian_models import (
    PowerPosteriorPrior, BoxUniformPrior, GaussianPeakedPrior, ResizeablePrior)
from supernest.framework.mixtures import StochasticMixtureModel

rc('font', **{'family': 'serif', 'serif': ['Times']})
rc('text', usetex=True)
plt.rcParams["font.size"] = 14

a = 6 * 10 ** 8
arr_bounds = (array([-a, -a, -a]), array([a, a, a]))
bounds = (-a, a)
mu = array([1, 2, 3])
cov = array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

args = [bounds, mu, cov]
kwargs = {
    'resume': False,
    'live_points': 50,
}

ppr_arr_bounds = PowerPosteriorPrior(arr_bounds, mu, cov, file_root='ppr_arr_bounds')
ppr = PowerPosteriorPrior(*args, file_root='ppr')
tgd = GaussianPeakedPrior(*args, file_root='tgd')
bun = BoxUniformPrior(*args, file_root='bun')
run = ResizeablePrior(*args, file_root='run')

mix = StochasticMixtureModel([bun, tgd], file_root='mix')

q0, reference = bun.nested_sample(**kwargs)
qg, gaussian = tgd.nested_sample(**kwargs)
qp, power = ppr.nested_sample(**kwargs)
qpp, power_arr_bounds = ppr_arr_bounds.nested_sample(**kwargs)
qm, samples = mix.nested_sample(**kwargs)

hist_samples = 1000

z_lower = min([x.logZ - x.logZerr for x in [ q0, qg, qp, qpp, qm]]) - 1
z_upper = max([x.logZ + x.logZerr for x in [ q0, qg, qp, qpp, qm]]) + 1


def overlay_gaussian(mean, sigma, **fill_kwargs):
    x = linspace(z_lower, z_upper, hist_samples)
    plt.fill_between(x, 0, hist_samples / 50 / (sigma * sqrt(2 * pi)) *
                     exp(- (x - mean) ** 2 / (2 * sigma ** 2)), **fill_kwargs)




# plt.hist(samples.logZ(hist_samples), label=r'mix\((U, G)\)', alpha=1)
overlay_gaussian(qm.logZ, qm.logZerr, label=r'SSIM\((U, G)\)', hatch='//', color='gold')
# This would contain the right histogram, except polychord
# terminates before generating any usable runs.
plt.hist(power.logZ(hist_samples), label='PPR', alpha=0.3, color='red')
# plt.hist(gaussian.logZ(hist_samples), label='\(G\) - true posterior', alpha=0.3, )
overlay_gaussian(qg.logZ, qg.logZerr,
                 label=r'$G$ - iPPR', alpha=0.3, color='black')
plt.hist(reference.logZ(hist_samples), label=r'\(U\) - reference',
         alpha=0.3, fill=True, color='blue')
plt.xlim(z_lower, z_upper)
plt.xlabel(r'\(\ln {\cal Z}\)')
plt.legend()
tikzplotlib.save('../illustrations/histograms.tex')
plt.show()
