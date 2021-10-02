import unittest
import supernest as sn
import numpy as np


class TestTyping(unittest.TestCase):

    def setUp(self):
        bounds = (0, 1)
        mean = np.array([0])
        stdev = np.array([[1]])
        self.proposal = sn.gaussian_proposal(bounds, mean, stdev)
        self.t_proposal = sn.truncated_gaussian_proposal(bounds, mean, stdev)


    def test_proposal_as_return_type(self):
        self.assertIsInstance(self.proposal, sn.Proposal)
        self.assertIsInstance(self.t_proposal, sn.Proposal)
        self.assertIsInstance(sn.superimpose([self.proposal, self.proposal]),
                              sn.Proposal)
        self.assertIsInstance(sn.superimpose([self.proposal, self.proposal], nDims=1).nDims, int)
        # self.assertIsInstance(sn.superimpose([proposal, proposal], nDims=1), sn.NDProposal)

    def test_prior_type(self):
        self.assertIsInstance(self.proposal.prior, sn.proposals.Prior)
        self.assertIsInstance(self.t_proposal.prior, sn.proposals.Prior)


if __name__ == '__main__':
    unittest.main()
