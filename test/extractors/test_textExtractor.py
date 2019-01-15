import unittest
from edgarScraper.extractors.textExtractor import TextExtractor
from edgarScraper.pipelineIO.fileParser import FileParser
from edgarScraper.pipelineIO.resultSet import DebtLineItem


class FileUrlIteratorTest(unittest.TestCase):

    def setUp(self):
        self.baseUrl = 'https://www.sec.gov/Archives/edgar/'
        self.parser = FileParser()
        self.te = TextExtractor()

    def test_textWithTables(self):
        url = self.baseUrl + 'data/84129/0000893220-94-000311.txt'
        text, code = self.parser._getFile(url)
        result = self.te.processText(text)
        self.assertTrue(result)
        self.assertIsInstance(result[0], DebtLineItem)

    def test_textWOTables(self):
        url = self.baseUrl + 'data/41289/0000041289-94-000003.txt'
        text, code = self.parser._getFile(url)
        result = self.te.processText(text)
        self.assertTrue(result)
        self.assertIsInstance(result[0], DebtLineItem)

    def test_HTMLasText(self):
        url = self.baseUrl + 'data/1175501/0001175501-11-000006.txt'
        text, code = self.parser._getFile(url)
        result = self.te.processText(text)
        self.assertTrue(result)
        self.assertIsInstance(result[0], DebtLineItem)
