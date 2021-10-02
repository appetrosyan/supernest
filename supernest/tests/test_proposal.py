import unittest
import supernest as sn
import numpy as np
import hypothesis


class TestProposal(unittest.TestCase):
    def setUp(self):
        bounds = (-1, 1)
        means = np.array([-1, 0, 1])
        covs = np.diag(np.array([1,2,3]))
        self.proposal = sn.gaussian_proposal(bounds, means, covs)

    def test_proposal_prior_type(self):
        self.assertIsInstance(self.proposal.prior(np.zeros(3)), np.ndarray)

    @hypothesis.given(hypothesis.strategies.integers(1, 100))
    def test_proposal_prior_dims(self, num):
        bounds = (-1, 1)
        means = np.zeros(num)
        covs = np.diag(np.zeros(num) + 1)
        proposal = sn.gaussian_proposal(bounds, means, covs)
        self.assertEqual(len(proposal.prior(np.zeros(num))), num)

    try:
        @hypothesis.given(hypothesis.extra.numpy.arrays(np.float64, (2)))
        def test_constructing_proposal(self, arr):
            sn.truncated_gaussian_proposal(arr, arr, np.diag(np.zeros(len(arr)) + 1))
            sn.gaussian_proposal(arr, arr, np.diag(np.zeros(len(arr))+1))
    except AttributeError as e:
        print(e)



if __name__ == '__main__':
    unittest.main()
