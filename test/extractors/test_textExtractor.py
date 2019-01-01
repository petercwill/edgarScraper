from textExtractor import TextExtractor
from fileHandler import FileHandler
import unittest
from resultSet import DebtLineItem


class FileUrlIteratorTest(unittest.TestCase):

    def setUp(self):
        self.baseUrl = 'https://www.sec.gov/Archives/edgar/'
        self.fh = FileHandler()
        self.te = TextExtractor()

    def test_textWithTables(self):
        url = self.baseUrl + 'data/84129/0000893220-94-000311.txt'
        text, code = self.fh._getFile(url)
        result = self.te.processText(text)
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], DebtLineItem)

    def test_textWOTables(self):
        url = self.baseUrl + 'data/41289/0000041289-94-000003.txt'
        text, code = self.fh._getFile(url)
        result = self.te.processText(text)
        self.assertIsNotNone(result)
        self.assertIsInstance(result[0], DebtLineItem)


if __name__ == '__main__':
    unittest.main()
