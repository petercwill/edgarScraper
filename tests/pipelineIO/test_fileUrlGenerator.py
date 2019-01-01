import unittest
from fileUrlGenerator import FileUrlGenerator


class FileUrlIteratorTest(unittest.TestCase):

    def test_iteration(self):
        fUrl = FileUrlGenerator().getUrlGenerator()
        baseUrl = 'https://www.sec.gov/Archives/edgar/'

        first10Q = baseUrl + 'data/40638/0000950124-94-001209.txt'
        second10Q = baseUrl + 'data/41289/0000041289-94-000003.txt'
        third10Q = baseUrl + 'data/101929/0000101929-94-000016.txt'

        self.assertEqual(next(fUrl), first10Q)
        self.assertEqual(next(fUrl), second10Q)
        self.assertEqual(next(fUrl), third10Q)

    def test_yearFilter(self):
        fUrl = FileUrlGenerator(years=[2010]).getUrlGenerator()
        baseUrl = 'https://www.sec.gov/Archives/edgar/'

        first10Q = baseUrl + 'data/104207/0000104207-10-000005.txt'
        second10Q = baseUrl + 'data/1050825/0000950123-10-000336.txt'
        third10Q = baseUrl + 'data/1256540/0001295345-10-000002.txt'

        self.assertEqual(next(fUrl), first10Q)
        self.assertEqual(next(fUrl), second10Q)
        self.assertEqual(next(fUrl), third10Q)

    def test_cikFilter(self):

        # cik is for walgreens co.
        fUrl = FileUrlGenerator(years=[2010], ciks=[104207]).getUrlGenerator()
        baseUrl = 'https://www.sec.gov/Archives/edgar/'

        # first 10-Q found in 2010-01-05
        first10Q = baseUrl + 'data/104207/0000104207-10-000005.txt'

        # second 10-Q found in 2010-3-29
        second10Q = baseUrl + 'data/104207/0000104207-10-000039.txt'

        # hird 10-Q found in 2010-6-28
        third10Q = baseUrl + 'data/104207/0000104207-10-000059.txt'

        self.assertEqual(next(fUrl), first10Q)
        self.assertEqual(next(fUrl), second10Q)
        self.assertEqual(next(fUrl), third10Q)

    def test_nFiles(self):
        fUrl = FileUrlGenerator(maxFiles=10).getUrlGenerator()
        self.assertEqual(len(list(fUrl)), 10)


if __name__ == '__main__':
    unittest.main()
