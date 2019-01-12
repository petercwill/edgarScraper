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
        testIndexResult = IndexResult(0, 'test', 'test', 'test', url)
        rGen = ResultGenerator()
        result, dd = rGen.fileUrl2Result(testIndexResult)

        self.assertIsNotNone(result.lineItems)
        self.assertIsInstance(result, ResultSet)
        #self.assertIsNotNone(dd.text)

    def test_html(self):
        url = self.baseUrl + 'data/1144215/0001193125-10-001623.txt'
        testIndexResult = IndexResult(1, 'test', 'test', 'test', url)
        rGen = ResultGenerator()
        result, dd = rGen.fileUrl2Result(testIndexResult)

        self.assertIsNotNone(result.lineItems)
        self.assertIsInstance(result, ResultSet)
        self.assertIsNone(dd.text)

    def test_text(self):
        url = self.baseUrl + 'data/1005406/0000898430-96-001816.txt'
        testIndexResult = IndexResult(2, 'test', 'test', 'test', url)
        rGen = ResultGenerator()
        result, dd = rGen.fileUrl2Result(testIndexResult)

        self.assertIsNotNone(result.lineItems)
        self.assertIsInstance(result, ResultSet)
        self.assertIsNone(dd.text)

    def test_failures(self):
        url = self.baseUrl + 'data/1468679/0001271008-11-000006.txt'
        testIndexResult = IndexResult(2, 'test', 'test', 'test', url)
        rGen = ResultGenerator()        



if __name__ == '__main__':
    unittest.main()
