import unittest
from pipelineIO.fileHandler import FileHandler
from pipelineIO.resultSet import DebtLineItem


class FileHandlerTest(unittest.TestCase):

    def setUp(self):
        self.baseUrl = 'https://www.sec.gov/Archives/edgar/'
        self.fh = FileHandler()

    def test_html(self):
        url = self.baseUrl + 'data/1144215/0001193125-10-001623.txt'
        results = self.fh.extractDebt(url)
        self.assertIsNotNone(results)
        self.assertIsInstance(results[0], DebtLineItem)
        self.assertEqual(self.fh.statusCode, "HTML")

    def test_xbrl(self):
        url = self.baseUrl + 'data/730255/0001206774-15-003149.txt'
        results = self.fh.extractDebt(url)
        self.assertIsNotNone(results)
        self.assertIsInstance(results[0], DebtLineItem)
        self.assertEqual(self.fh.statusCode, "XBRL")

    def test_text(self):
        url = self.baseUrl + 'data/1005406/0000898430-96-001816.txt'
        results = self.fh.extractDebt(url)
        self.assertIsNotNone(results)
        self.assertIsInstance(results[0], DebtLineItem)
        self.assertEqual(self.fh.statusCode, "TEXT")


if __name__ == '__main__':
    unittest.main()
