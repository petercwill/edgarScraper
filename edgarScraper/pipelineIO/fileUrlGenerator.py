import logging
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re


class FileUrlGenerator(object):
    '''
    Yield urls for 10Qs found in the daily index files for all
    relevent years and quarter.
    '''

    def __init__(self, years=None, ciks=None, maxFiles=100):

        self.log = logging.getLogger()
        self.baseUrl = 'https://www.sec.gov/Archives/edgar/daily-index/'
        self.years = years
        self.ciks = ciks
        self.maxFiles = maxFiles
        self.qtrRe = re.compile(r'QTR[1-4]')
        self.fileRe = re.compile(r'master')
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
                for filing in self._getChildUrl(quarter, self.fileRe):
                    yield filing

    def getUrlGenerator(self):

        count = 0

        for masterIndexUrl in self._yieldMasterIndexUrl():

            self.log.info('Scanning index {} for 10Qs'.format(masterIndexUrl))
            response = requests.get(masterIndexUrl)

            for line in response.text.split('\n'):
                tokens = line.split('|')
                if len(tokens) != 5:
                    self.log.debug('SKIPPING MALFORMED LINE: {}'.format(line))
                    continue

                if self.ciks:
                    if tokens[0] not in self.cikSet:
                        continue

                self.log.debug(
                    'Found Filing Type {} At {}'.format(
                        tokens[2], tokens[4])
                )

                # format changes over time - duplication of '/edgar' directory
                fileSuffix = re.sub('edgar/', '', tokens[4])

                if tokens[2] == '10-Q':
                    count += 1
                    yield "https://www.sec.gov/Archives/edgar/" + fileSuffix

                if count >= self.maxFiles:
                    return

