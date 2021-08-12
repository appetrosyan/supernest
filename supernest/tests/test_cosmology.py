import supernest
from pypolychord.settings import PolyChordSettings
from pypolychord import run_polychord
import matplotlib.pyplot as plt
import numpy as np
import mpi4py


def uniform_with_gaussian_like(nDims, mu, sigma, bounds):
    thetamin = bounds[0]
    thetamax = bounds[1]
    invCov = np.linalg.inv(sigma)

    def ll(theta):
        return -(theta - mu) @ invCov @ (theta - mu) / 2, []

    def up(cube):
        return thetamin + cube * (thetamax - thetamin)

    return up, ll


def normal_run_settings(nDims,
                        nlive,
                        file_root='control_uniform_gaussian_like'):
    settings = PolyChordSettings(nDims, 0)
    settings.read_resume = False
    settings.feedback = 0
    settings.nlive = nlive
    settings.file_root = file_root

    return settings


def test_uniform(nDims, mu, sigma, bounds, nlive):
    prior, like = uniform_with_gaussian_like(nDims, mu, sigma, bounds)

    settings = normal_run_settings(nDims, nlive)
    output = run_polychord(like, nDims, 0, settings, prior)
    return output, prior, like


def test_proposal(nDims, mu, sigma, bounds, nlive):
    prior, like = uniform_with_gaussian_like(nDims, mu, sigma, bounds)

    pp, ll = supernest.truncated_gaussian_proposal(bounds,
                                                   mu,
                                                   sigma,
                                                   loglike=like)
    settings = normal_run_settings(nDims,
                                   nlive,
                                   file_root="supernest_proposal")
    output = run_polychord(ll, nDims, 0, settings, pp)
    return output, pp, ll


def test_supernest(nDims, mu, sigma, bounds, nlive):
    prior, like = uniform_with_gaussian_like(nDims, mu, sigma, bounds)

    pp, ll = supernest.truncated_gaussian_proposal(bounds,
                                                   mu,
                                                   sigma,
                                                   loglike=like)
    dims, ppp, lll = supernest.superimpose([(prior, like), (pp, ll)], nDims)

    settings = normal_run_settings(dims,
                                   nlive,
                                   file_root="supernest_superimposed")

    output = run_polychord(lll, dims, 0, settings, ppp)
    return output, ppp, lll


def deltas(boundaries, nDims, mu, sigma, nlive):
    retZ = []
    retZerr = []
    for b in boundaries:
        bounds = (-b, b)
        uni = test_uniform(nDims, mu, sigma, bounds, nlive)[0]
        # pro = test_supernest(nDims, mu, sigma, bounds, nlive)[0]
        pro = test_proposal(nDims, mu, sigma, bounds, nlive)[0]
        retZ.append(uni.logZ - pro.logZ)
        retZerr.append(max(uni.logZerr, pro.logZerr))
    return retZ, retZerr


def main(nlive=30):
    global uniform, proposal, x, y
    mu = np.loadtxt(
        '/home/app/Git/sspr/supernest/tests/cosmology_data/means.npy')
    sigma = np.loadtxt(
        '/home/app/Git/sspr/supernest/tests/cosmology_data/covmat.npy')
    bounds = np.loadtxt(
        '/home/app/Git/sspr/supernest/tests/cosmology_data/bounds.npy')
    bounds = bounds.T
    x = test_uniform(len(mu), mu, sigma, bounds, nlive)
    y = test_proposal(len(mu), mu, sigma, bounds, nlive)


if __name__ == '__main__':
    main()
