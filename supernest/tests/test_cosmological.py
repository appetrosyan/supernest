import os
from mpi4py import MPI
import numpy as np
from anesthetic import read_chains
import matplotlib.pyplot as plt
import pypolychord as pp
import supernest as sn
from pypolychord.settings import PolyChordSettings as Settings

if not os.path.isdir('base'):
    chains = 'https://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_CosmoParams_base-plikHM-TTTEEE-lowl-lowE_R3.00.zip'

    import urllib.request
    urllib.request.urlretrieve(chains, "chains.zip")

    import zipfile
    with zipfile.ZipFile("chains.zip", 'r') as zip_ref:
        zip_ref.extractall(".")

    os.remove("chains.zip")



# Load the planck samples into MCMCSamples object
root = 'base/plikHM_TTTEEE_lowl_lowE_lensing/base_plikHM_TTTEEE_lowl_lowE_lensing'
planck_samples = read_chains(root)

# Define the parameters we're working with the first 27 (real) parameters
nDims = 27
nDerived = 0
paramnames = planck_samples.columns[:nDims]

mu = planck_samples[paramnames].mean().values
Sig = planck_samples[paramnames].cov().values
invSig = np.linalg.inv(Sig)
# This is not strictly necessary, but makes the loglikelihood look slightly
# more planck-like. See https://arxiv.org/abs/1903.06682
d = planck_samples.logL.var()*2
logLmax = planck_samples.logL.mean() + d/2


bounds = np.array(
    [
        [planck_samples[p].min(), planck_samples[p].max()]
        for p in paramnames
    ],
    dtype=float)


def loglikelihood(theta):
    return logLmax-(theta-mu) @ invSig @ (theta-mu)/2, []

def prior(cube):
    theta = bounds[:, 0]*(1-cube) + bounds[:, 1]*cube
    return theta



nDerived = 0
nlive = 500

# PolyChord
settings = Settings(nDims, nDerived, file_root="default", nlive=nlive)
pp.run_polychord(loglikelihood, nDims, nDerived, settings, prior=prior)
poly_samples = read_chains("chains/default", columns=paramnames)

# SuperNest
gauss = sn.gaussian_proposal(bounds.T, mu, Sig*2, loglike=loglikelihood)
proposal = sn.superimpose([(prior, loglikelihood), gauss], nDims=nDims)
settings = Settings(proposal.nDims, nDerived, file_root="supernest", nlive=nlive)
pp.run_polychord(proposal.likelihood, proposal.nDims, 0, settings, prior=proposal.prior)
super_samples = read_chains("chains/supernest", columns=paramnames.tolist() + ['prob', 'choice'])
super_samples.tex = planck_samples.tex
super_samples.tex['prob'] = '$p$'
super_samples.tex['choice'] = '$x$'

# SuperNest with bad proposal
mu += np.sqrt(np.diag(Sig))*1
gauss = sn.gaussian_proposal(bounds.T, mu, Sig*2, loglike=loglikelihood)
proposal = sn.superimpose([(prior, loglikelihood), gauss], nDims=nDims)
settings = Settings(proposal.nDims, nDerived, file_root="supernest_bad_proposal", nlive=nlive)
pp.run_polychord(proposal.likelihood, proposal.nDims, 0, settings, prior=proposal.prior)
superbad_samples = read_chains("chains/supernest_bad_proposal", columns=paramnames.tolist() + ['prob', 'choice'])
superbad_samples.tex = planck_samples.tex
superbad_samples.tex['prob'] = '$p$'
superbad_samples.tex['choice'] = '$x$'


plt.hist(poly_samples.logZ(1000), bins=30,  label='PC')
plt.hist(super_samples.logZ(1000), bins=30, alpha=0.8, label='SN')
plt.hist(superbad_samples.logZ(1000), bins=30, alpha=0.8, label='SN bad proposal')

logV = np.log(np.diff(bounds)).sum()
logZ = logLmax + np.linalg.slogdet(2*np.pi*Sig)[1]/2 - logV
plt.axvline(logZ, color='k')
plt.xlabel(r'$\log\mathcal{Z}$')
plt.legend()


fig, ax = planck_samples.plot_2d(paramnames[:6])
poly_samples.plot_2d(ax)
super_samples.plot_2d(ax)
superbad_samples.plot_2d(ax)
