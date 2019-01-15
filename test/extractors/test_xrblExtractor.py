import unittest
from edgarScraper.extractors.xbrlExtractor import XBRLExtractor
from edgarScraper.pipelineIO.fileParser import FileParser
from edgarScraper.pipelineIO.resultSet import DebtLineItem


class XBRLExtractorTest(unittest.TestCase):

    def setUp(self):
        self.baseUrl = 'https://www.sec.gov/Archives/edgar/'
        self.parser = FileParser()
        self.xe = XBRLExtractor()

    def test_xbrl1(self):
        url = self.baseUrl + 'data/1005286/0001437749-15-017917.txt'
        text, code = self.parser._getFile(url)
        result, debtDisclosure = self.xe.processText(text)
        self.assertTrue(result)
        self.assertIsInstance(result[0], DebtLineItem)

    def test_xbrl2(self):
        url = self.baseUrl + 'data/815097/0000815097-16-000040.txt'
        text, code = self.parser._getFile(url)
        result, debtDisclosure = self.xe.processText(text)
        self.assertTrue(result)
        self.assertIsInstance(result[0], DebtLineItem)

    def test_xbrl3(self):
        url = self.baseUrl + 'data/63754/0000063754-16-000089.txt'
        text, code = self.parser._getFile(url)
        result, debtDisclosure = self.xe.processText(text)
        self.assertTrue(result)
        self.assertIsInstance(result[0], DebtLineItem)

    def test_longXbrl(self):
        url = self.baseUrl + 'data/1393612/0001193125-11-091525.txt'
        text, code = self.parser._getFile(url)
        result, debtDisclosure = self.xe.processText(text)
        self.assertTrue(result)
        self.assertIsInstance(result[0], DebtLineItem)
