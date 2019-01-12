import sys
sys.path.append('../../')

import unittest
from edgarScraper.extractors.htmlExtractor import HTMLExtractor
from edgarScraper.pipelineIO.resultGenerator import ResultGenerator
from edgarScraper.pipelineIO.resultSet import DebtLineItem
import cProfile
from pstats import Stats


class HTMLExtractorTest(unittest.TestCase):

    def setUp(self):
        self.baseUrl = 'https://www.sec.gov/Archives/edgar/'
        self.rGen = ResultGenerator()
        self.he = HTMLExtractor()
        # self.pr = cProfile.Profile()
        # self.pr.enable()
        # print("\n<<<---")

    # def tearDown(self):
    #     """finish any test"""
    #     p = Stats(self.pr)
    #     p.strip_dirs()
    #     p.sort_stats('cumtime')
    #     p.print_stats(200)
    #     print("\n--->>>")

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

    def test_htmlWOTables3(self):
        url = self.baseUrl + 'data/1175501/0001175501-11-000006.txt'
        text, code = self.rGen._getFile(url)
        result = self.he.processText(text)
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], DebtLineItem)

    def test_htmlWithZeros(self):
        url = self.baseUrl + 'data/1468679/0001271008-11-000006.txt'
        text, code = self.rGen._getFile(url)
        result = self.he.processText(text)
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], DebtLineItem)


if __name__ == '__main__':
    unittest.main()
