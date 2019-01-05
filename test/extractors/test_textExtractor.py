import unittest
from edgarScraper.extractors.textExtractor import TextExtractor
from edgarScraper.pipelineIO.resultGenerator import ResultGenerator
from edgarScraper.pipelineIO.resultSet import DebtLineItem


class FileUrlIteratorTest(unittest.TestCase):

    def setUp(self):
        self.baseUrl = 'https://www.sec.gov/Archives/edgar/'
        self.rGen = ResultGenerator()
        self.te = TextExtractor()

    def test_textWithTables(self):
        url = self.baseUrl + 'data/84129/0000893220-94-000311.txt'
        text, code = self.rGen._getFile(url)
        result = self.te.processText(text)
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], DebtLineItem)

    def test_textWOTables(self):
        url = self.baseUrl + 'data/41289/0000041289-94-000003.txt'
        text, code = self.rGen._getFile(url)
        result = self.te.processText(text)
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], DebtLineItem)


if __name__ == '__main__':
    unittest.main()
