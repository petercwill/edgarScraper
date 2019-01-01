from xbrlExtractor import XBRLExtractor
from fileHandler import FileHandler
import unittest
from resultSet import DebtLineItem


class HTMLExtractorTest(unittest.TestCase):

    def setUp(self):
        self.baseUrl = 'https://www.sec.gov/Archives/edgar/'
        self.fh = FileHandler()
        self.xe = XBRLExtractor()

    def test_htmlWithTables(self):
        url = self.baseUrl + 'data/1005286/0001437749-15-017917.txt'
        text, code = self.fh._getFile(url)
        result = self.xe.processText(text)
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], DebtLineItem)
        print(result)


if __name__ == '__main__':
    unittest.main()
