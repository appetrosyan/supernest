import unittest
import supernest as sn
import numpy as np

class TestSuperposition(unittest.TestCase):
    def setUp(self):
        self.bounds = (0, 1)
        self.mean = np.array([0])
        self.stdev = np.array([[1]])
        self.proposal = sn.gaussian_proposal(self.bounds, self.mean, self.stdev)

    def test_proposal_calculates_nDims(self):
        self.assertEqual(sn.superimpose([self.proposal, self.proposal], nDims=1).nDims, 3)


if __name__ == '__main__':
    unittest.main()
