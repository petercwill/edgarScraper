import unittest
from edgarScraper.extractors.xbrlExtractor import XBRLExtractor
from edgarScraper.pipelineIO.resultGenerator import ResultGenerator
from edgarScraper.pipelineIO.resultSet import DebtLineItem


class HTMLExtractorTest(unittest.TestCase):

    def setUp(self):
        self.baseUrl = 'https://www.sec.gov/Archives/edgar/'
        self.rGen = ResultGenerator()
        self.xe = XBRLExtractor()

    def test_htmlWithTables(self):
        url = self.baseUrl + 'data/1005286/0001437749-15-017917.txt'
        text, code = self.rGen._getFile(url)
        result = self.xe.processText(text)
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], DebtLineItem)


if __name__ == '__main__':
    unittest.main()
