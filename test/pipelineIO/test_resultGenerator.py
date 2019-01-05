import unittest
import sys
sys.path.append('../../')
from edgarScraper.pipelineIO.resultGenerator import ResultGenerator
from edgarScraper.pipelineIO.resultSet import (DebtLineItem, ResultSet)
from edgarScraper.pipelineIO.fileUrlGenerator import IndexResult

class ResultGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.baseUrl = 'https://www.sec.gov/Archives/edgar/'

    def test_xbrl(self):
        url = self.baseUrl + 'data/730255/0001206774-15-003149.txt'
        testIndexResult = IndexResult('test', 'test', 'test', url)
        rGen = ResultGenerator()
        result = rGen.fileUrl2Result(testIndexResult)

        self.assertIsNotNone(result.lineItems)
        self.assertIsInstance(result, ResultSet)
        # self.assertEqual(rGen.xbrlCount, 1)
        # self.assertEqual(rGen.htmlCount, 0)
        # self.assertEqual(rGen.textCount, 0)
        # self.assertEqual(rGen.failCount, 0)

    def test_html(self):
        url = self.baseUrl + 'data/1144215/0001193125-10-001623.txt'
        testIndexResult = IndexResult('test', 'test', 'test', url)
        rGen = ResultGenerator()
        result = rGen.fileUrl2Result(testIndexResult)

        self.assertIsNotNone(result.lineItems)
        self.assertIsInstance(result, ResultSet)
        # self.assertEqual(rGen.xbrlCount, 0)
        # self.assertEqual(rGen.htmlCount, 1)
        # self.assertEqual(rGen.textCount, 0)
        # self.assertEqual(rGen.failCount, 0)

    def test_text(self):
        url = self.baseUrl + 'data/1005406/0000898430-96-001816.txt'
        testIndexResult = IndexResult('test', 'test', 'test', url)
        rGen = ResultGenerator()
        result = rGen.fileUrl2Result(testIndexResult)

        self.assertIsNotNone(result.lineItems)
        self.assertIsInstance(result, ResultSet)
        # self.assertEqual(rGen.xbrlCount, 0)
        # self.assertEqual(rGen.htmlCount, 0)
        # self.assertEqual(rGen.textCount, 1)
        # self.assertEqual(rGen.failCount, 0)

    # def test_iteration(self):
    #     rGen = ResultGenerator(years=[2010], maxFiles=5)
    #     results = list(rGen.getResultGenerator())
    #     self.assertIsNotNone(results)
    #     self.assertIsInstance(results[0], ResultSet)
    #     self.assertEqual(
    #         rGen.xbrlCount + rGen.htmlCount + rGen.textCount + rGen.failCount,
    #         5
    #     )


if __name__ == '__main__':
    unittest.main()
