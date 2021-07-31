import mpi4py
import supernest

from pypolychord.settings import PolyChordSettings
from pypolychord import run_polychord

import numpy as np
import matplotlib.pyplot as plt

nDims = 2
bounds = np.array([[-30, -10], [30, 10]])
means = np.array([0.2, 0])
covmat = np.array([[0.1, 0.05], [0.05, 0.2]])
proposal_mean = np.array([0.2, 0])
proposal_covmat = np.array([[0.3, 0], [0, 0.4]])


def uniform_with_gaussian_like(nDims, mu, sigma, bounds):
    thetamin = bounds[0]
    thetamax = bounds[1]

    def ll(theta):
        delta = theta - mu
        ll = - np.linalg.slogdet(2 * np.pi * sigma)/2
        ll -= np.linalg.multi_dot([delta, np.linalg.inv(sigma), delta])/2
        return ll, []

    def up(cube):
        return thetamin + cube * (thetamax - thetamin)

    return up, ll


def main():
    hypothesis = uniform_with_gaussian_like(2, means, covmat, bounds)
    proposal = supernest.gaussian_proposal(bounds, proposal_mean, proposal_covmat, hypothesis[1])
    superProposal = supernest.superimpose([hypothesis, proposal], nDims)
    settings = PolyChordSettings(nDims, 0)
    settings.read_resume = False
    settings.feedback = 0
    settings.file_root = "super_test"
    run_polychord(proposal.likelihood, nDims, 0, settings, prior=proposal.prior)


if __name__ == '__main__':
    main()
