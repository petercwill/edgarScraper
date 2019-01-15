import unittest
import pandas as pd
from edgarScraper.edgarDebtScraper import EdgarDebtScraper


class EdgarDebtScraperTest(unittest.TestCase):

    def setUp(self):
        self.eds = EdgarDebtScraper()

    def test_spToDF(self):
        lineItems, disclosures = self.eds.runJob(
            maxFiles=25,
            nScraperProcesses=1
        )
        self.assertIsInstance(lineItems, pd.DataFrame)
        self.assertEqual(lineItems.shape[0], 25)
        self.assertIsInstance(lineItems, pd.DataFrame)
        self.assertEqual(lineItems.shape[0], 25)

    def test_mpToDf(self):
        lineItems, disclosures = self.eds.runJob(
            years=[2011],
            maxFiles=100,
            nScraperProcesses=4
        )
        self.assertIsInstance(lineItems, pd.DataFrame)
        self.assertEqual(lineItems.shape[0], 100)
        self.assertIsInstance(disclosures, pd.DataFrame)
        self.assertEqual(disclosures.shape[0], 100)


if __name__ == '__main__':
    unittest.main()
