import sys
sys.path.append('../../')

import unittest
from edgarScraper.extractors.xbrlExtractor import XBRLExtractor
from edgarScraper.pipelineIO.resultGenerator import ResultGenerator
from edgarScraper.pipelineIO.resultSet import DebtLineItem
import cProfile
from pstats import Stats


class XBRLExtractorTest(unittest.TestCase):

    def setUp(self):
        self.baseUrl = 'https://www.sec.gov/Archives/edgar/'
        self.rGen = ResultGenerator()
        self.xe = XBRLExtractor()
    #     self.pr = cProfile.Profile()
    #     self.pr.enable()
    #     print("\n<<<---")

    # def tearDown(self):
    #     """finish any test"""
    #     p = Stats(self.pr)
    #     p.strip_dirs()
    #     p.sort_stats('cumtime')
    #     p.print_stats(200)
    #     print("\n--->>>")

    def test_xbrl1(self):
        url = self.baseUrl + 'data/1005286/0001437749-15-017917.txt'
        text, code = self.rGen._getFile(url)
        result, debtDisclosure = self.xe.processText(text)
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], DebtLineItem)

    def test_xbrl2(self):
        url = self.baseUrl + 'data/815097/0000815097-16-000040.txt'
        text, code = self.rGen._getFile(url)
        result, debtDisclosure = self.xe.processText(text)
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], DebtLineItem)

    def test_xbrl3(self):
        url = self.baseUrl + 'data/63754/0000063754-16-000089.txt'
        text, code = self.rGen._getFile(url)
        result, debtDisclosure = self.xe.processText(text)
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], DebtLineItem)

    def test_longXbrl(self):
        url = self.baseUrl + 'data/1393612/0001193125-11-091525.txt'
        text, code = self.rGen._getFile(url)
        result, debtDisclosure = self.xe.processText(text)
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], DebtLineItem)

if __name__ == '__main__':
    unittest.main()
