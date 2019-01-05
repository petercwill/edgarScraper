import unittest
from edgarScraper.extractors.htmlExtractor import HTMLExtractor
from edgarScraper.pipelineIO.resultGenerator import ResultGenerator
from edgarScraper.pipelineIO.resultSet import DebtLineItem


class HTMLExtractorTest(unittest.TestCase):

    def setUp(self):
        self.baseUrl = 'https://www.sec.gov/Archives/edgar/'
        self.rGen = ResultGenerator()
        self.he = HTMLExtractor()

    def test_htmlWithTables(self):
        url = self.baseUrl + 'data/1012956/0001193125-03-015316.txt'
        text, code = self.rGen._getFile(url)
        result = self.he.processText(text)
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], DebtLineItem)

    def test_htmlWithTables2(self):
        url = self.baseUrl + 'data/225261/0001047469-03-023135.txt'
        text, code = self.rGen._getFile(url)
        result = self.he.processText(text)
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], DebtLineItem)

    def test_htmlWithTables3(self):
        url = self.baseUrl + 'data/1368055/0001140361-10-002064.txt'
        text, code = self.rGen._getFile(url)
        result = self.he.processText(text)
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], DebtLineItem)

    def test_htmlWOTables(self):
        url = self.baseUrl + 'data/915337/0001002334-10-000006.txt'
        text, code = self.rGen._getFile(url)
        result = self.he.processText(text)
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], DebtLineItem)

    def test_htmlWOTables2(self):
        url = self.baseUrl + 'data/1439981/0001137050-10-000003.txt'
        text, code = self.rGen._getFile(url)
        result = self.he.processText(text)
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], DebtLineItem)
