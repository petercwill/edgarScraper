import unittest
from edgarScraper.pipelineIO.fileUrlGenerator import FileUrlGenerator


class FileUrlIteratorTest(unittest.TestCase):

    def test_iteration(self):
        fUrl = FileUrlGenerator().getUrlGenerator()
        baseUrl = 'https://www.sec.gov/Archives/edgar/'

        first10Q = baseUrl + 'data/40638/0000950124-94-001209.txt'
        second10Q = baseUrl + 'data/41289/0000041289-94-000003.txt'
        third10Q = baseUrl + 'data/801898/0000801898-94-000010.txt'

        self.assertEqual(next(fUrl).url, first10Q)
        self.assertEqual(next(fUrl).url, second10Q)
        self.assertEqual(next(fUrl).url, third10Q)

    def test_yearFilter(self):
        fUrl = FileUrlGenerator(years=[2010]).getUrlGenerator()
        baseUrl = 'https://www.sec.gov/Archives/edgar/'

        first10Q = baseUrl + 'data/16160/0001144204-10-000249.txt'
        second10Q = baseUrl + 'data/23217/0000950123-10-000408.txt'
        third10Q = baseUrl + 'data/1367617/0001224280-10-000002.txt'

        self.assertEqual(next(fUrl).url, first10Q)
        self.assertEqual(next(fUrl).url, second10Q)
        self.assertEqual(next(fUrl).url, third10Q)

    def test_cikFilter(self):

        # cik is for walgreens co.
        fUrl = FileUrlGenerator(years=[2010], ciks=[104207]).getUrlGenerator()
        baseUrl = 'https://www.sec.gov/Archives/edgar/'

        # first 10-Q found in 2010-01-05
        first10Q = baseUrl + 'data/104207/0000104207-10-000005.txt'

        # second 10-Q found in 2010-3-29
        second10Q = baseUrl + 'data/104207/0000104207-10-000039.txt'

        # third 10-Q found in 2010-6-28
        third10Q = baseUrl + 'data/104207/0000104207-10-000059.txt'

        urlList = [first10Q, second10Q, third10Q]

        genList = [item.url for item in fUrl]

        self.assertCountEqual(genList, urlList)


if __name__ == '__main__':
    unittest.main()
