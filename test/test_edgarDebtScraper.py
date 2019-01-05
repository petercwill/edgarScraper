import unittest
import sys
import cProfile
from pstats import Stats

sys.path.append('../')
from edgarScraper.edgarDebtScraper1 import EdgarDebtScraper


class EdgarDebtScraperTest(unittest.TestCase):

    def setUp(self):
        """init each test"""
        self.eds = EdgarDebtScraper()
        self.pr = cProfile.Profile()
        self.pr.enable()
        print("\n<<<---")

    def tearDown(self):
        """finish any test"""
        p = Stats(self.pr)
        p.strip_dirs()
        p.sort_stats('cumtime')
        p.print_stats(20)
        print("\n--->>>")

    # def test_spToDF(self):
    #     df = self.eds.runJob(
    #         outputType='pandas',
    #         maxFiles=25,
    #         nScraperProcesses=1
    #     )
    #     print(df)

    # def test_spToFile(self):
    #     f = self.eds.runJob(
    #         outputType='file',
    #         outputFile='test123',
    #         years=[2012],
    #         maxFiles=25,
    #         nScraperProcesses=1
    #     )
        
    #     print(f)

    # def test_mpToDF(self):
    #     df = self.eds.runJob(
    #         outputType='pandas',
    #         maxFiles=1000,
    #         nScraperProcesses=8
    #     )
    #     print(df)

    def test_mpToDf(self):
        df = self.eds.runJob(
            outputType='pandas',
            outputFile='text.csv',
            maxFiles=100000,
            nScraperProcesses=4
        )
        #print(df)


if __name__ == '__main__':
    unittest.main()
