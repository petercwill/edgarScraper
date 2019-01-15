import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
from collections import namedtuple
from edgarScraper.config.log import dailyIndLogger
from edgarScraper.config.constants import (
    NAME_POS, CIK_POS, DATE_POS, PATH_POS
)
from edgarScraper.config.regexExp import EDGAR_SUB
from edgarScraper.pipelineIO.utils import iteratorSlice
import multiprocessing

IndexResult = namedtuple('IndexResult', 'seqNo date name cik url')


def processIndex(masterIndexUrls, ciks):

    results = []
    for url in masterIndexUrls:

        response = requests.get(url)
        lines = response.text.split('\n')

        exitFlag = False
        for i, line in enumerate(lines):

            if not line.startswith("10-Q "):
                if exitFlag:
                    break
                else:
                    continue

            name = line[NAME_POS[0]:NAME_POS[1]].strip()
            cik = line[CIK_POS[0]:CIK_POS[1]].strip()
            date = line[DATE_POS[0]:DATE_POS[1]].strip()
            pathSuffix = line[PATH_POS[0]:].strip()

            if cik in ciks:

                # check for duplicate 'edgar' directory - changes over time
                pathSuffix = re.sub(EDGAR_SUB, '', pathSuffix)
                filePath = (
                    "https://www.sec.gov/Archives/edgar/" + pathSuffix
                )

                result = IndexResult(
                    None,
                    date,
                    name,
                    cik,
                    filePath,
                )
                dailyIndLogger.info("found {} in {}".format(cik, url))
                results.append(result)

            exitFlag = True

    return results


class FileUrlGenerator(object):
    '''
    Yield urls for 10Qs found in the daily index files for all
    relevent years and quarter.
    '''

    def __init__(self, years=None, ciks=None, maxFiles=100, nProcesses=8):

        self.log = dailyIndLogger
        self.baseUrl = 'https://www.sec.gov/Archives/edgar/daily-index/'
        self.years = years
        self.ciks = ciks
        self.maxFiles = maxFiles
        self.nProcesses = nProcesses
        self.qtrRe = re.compile(r'QTR[1-4]')
        self.fileRe = re.compile(r'form')
        self._makeYearRe()
        self._makeCikSet()

    def _makeYearRe(self):
        if self.years:
            yearString = ['(' + str(y) + ')' for y in self.years]
            self.yearRe = re.compile("|".join(yearString))

        else:
            self.yearRe = re.compile(r'\d{4}')

    def _makeCikSet(self):
        if self.ciks:
            self.cikSet = set(str(c) for c in self.ciks)

    def _getChildUrl(self, parentUrl, linkRegex, divId='main-content'):

        response = requests.get(parentUrl)
        soup = BeautifulSoup(response.text, features="lxml")
        table = soup.find("div", {"id": divId})
        for link in table.find_all('a'):

            if linkRegex.match(link.text):
                childUrl = urljoin(parentUrl, link.get('href'))
                yield childUrl

    def _yieldMasterIndexUrl(self):

        for year in self._getChildUrl(self.baseUrl, self.yearRe):
            for quarter in self._getChildUrl(year, self.qtrRe):
                self.quarterCount = 0
                self.log.info(
                    'Searching for 10Qs in {}'.format(
                        quarter
                    )
                )
                for filing in self._getChildUrl(quarter, self.fileRe):
                    yield filing

    def _getUrlGenerator(self):

        totalCount = 0

        for url in self._yieldMasterIndexUrl():

            if url[-3:] == '.gz':
                self.log.info(
                    'Skipping compressed index file {}'.format(url)
                )
                continue

            dayCount = 0
            response = requests.get(url)
            lines = response.text.split('\n')

            exitFlag = False
            for i, line in enumerate(lines):

                if not line.startswith("10-Q "):
                    if exitFlag:
                        break
                    else:
                        continue

                dayCount += 1
                totalCount += 1

                if totalCount % 25 == 0:
                    self.log.info('Generated {} 10-Qs '.format(totalCount))

                name = line[NAME_POS[0]:NAME_POS[1]].strip()
                cik = line[CIK_POS[0]:CIK_POS[1]].strip()
                date = line[DATE_POS[0]:DATE_POS[1]].strip()
                pathSuffix = line[PATH_POS[0]:].strip()

                # check for duplicate 'edgar' directory - changes over time
                pathSuffix = re.sub(EDGAR_SUB, '', pathSuffix)
                filePath = (
                    "https://www.sec.gov/Archives/edgar/" + pathSuffix
                )

                result = IndexResult(
                    totalCount,
                    date,
                    name,
                    cik,
                    filePath
                )

                yield result
                exitFlag = True

                if totalCount >= self.maxFiles:
                    break

            self.log.debug(
                'Found {} 10-Qs in index file {}'.format(
                    dayCount,
                    url
                )
            )

            if totalCount >= self.maxFiles:
                break

    def _getCikSpecificFilingsDistr(self, nProcesses, ciks):
        '''
        Change 10-Q search behavior if a list of ciks is passed.
        No longer lazily iterating through daily files,
        eagerly get all matching 10-Qs, use multiprocessing.
        '''
        results = []
        pool = multiprocessing.Pool(processes=nProcesses)
        masterIndexGen = self._yieldMasterIndexUrl()
        miIterator = iteratorSlice(masterIndexGen, 100)

        queue = []

        while miIterator or queue:
            try:
                queue.append(
                    pool.apply_async(
                        processIndex, [next(miIterator), self.cikSet]
                    )
                )

            except (StopIteration, TypeError):
                miIterator = None

            while queue and (
                len(queue) >= pool._processes or not miIterator
            ):
                process = queue.pop(0)
                process.wait(0.01)
                if not process.ready():
                    queue.append(process)
                else:
                    results += process.get()
        pool.close()
        return results

    def getUrlGenerator(self):

        if self.ciks:
            self.log.info(
                'CIKS specified, calling distributed search routine,'
                'ignoring maxFiles limit'
            )
            results = self._getCikSpecificFilingsDistr(
                self.nProcesses, self.ciks
            )
            self.log.info('Found {} filings for selected ciks'.format(
                len(results))
            )
            return iter(results)

        else:
            return self._getUrlGenerator()
