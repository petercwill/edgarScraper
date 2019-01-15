import unittest
from edgarScraper.pipelineIO.fileParser import FileParser
from edgarScraper.pipelineIO.resultSet import ResultSet
from edgarScraper.pipelineIO.fileUrlGenerator import IndexResult


class FileParserTest(unittest.TestCase):

    def setUp(self):
        self.baseUrl = 'https://www.sec.gov/Archives/edgar/'

    def test_xbrl(self):
        url = self.baseUrl + 'data/730255/0001206774-15-003149.txt'
        testIndexResult = IndexResult(0, 'test', 'test', 'test', url)
        parser = FileParser()
        result, dd = parser.fileUrl2Result(testIndexResult)

        self.assertIsNotNone(result.lineItems)
        self.assertIsInstance(result, ResultSet)

    def test_html(self):
        url = self.baseUrl + 'data/1144215/0001193125-10-001623.txt'
        testIndexResult = IndexResult(1, 'test', 'test', 'test', url)
        parser = FileParser()
        result, dd = parser.fileUrl2Result(testIndexResult)

        self.assertIsNotNone(result.lineItems)
        self.assertIsInstance(result, ResultSet)
        self.assertIsNone(dd.TEXT)

    def test_text(self):
        url = self.baseUrl + 'data/1005406/0000898430-96-001816.txt'
        testIndexResult = IndexResult(2, 'test', 'test', 'test', url)
        parser = FileParser()
        result, dd = parser.fileUrl2Result(testIndexResult)

        self.assertIsNotNone(result.lineItems)
        self.assertIsInstance(result, ResultSet)
        self.assertIsNone(dd.TEXT)
