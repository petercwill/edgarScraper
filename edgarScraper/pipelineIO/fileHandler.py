import logging
import requests
from xbrlExtractor import XBRLExtractor
from htmlExtractor import HTMLExtractor
from textExtractor import TextExtractor


class FileHandler(object):

    def __init__(self):
        self.log = logging.getLogger()
        self.xbrlExtractor = XBRLExtractor()
        self.htmlExtractor = HTMLExtractor()
        self.textExtractor = TextExtractor()
        self.statusCode = None

    def _getFile(self, url):
        self.log.info('Getting {}'.format(url))
        response = requests.get(url)
        code = response.status_code
        if code != 200:
            self.log.info('File {} return response code {}.'.format(url, code))
            return (None, code)
        else:
            return (response.text, code)

    def _parseWatefall(self, text):

        results = self.xbrlExtractor.processText(text)
        if results:
            self.statusCode = 'XBRL'
            return results

        results = self.htmlExtractor.processText(text)
        if results:
            self.statusCode = 'HTML'
            return results

        results = self.textExtractor.processText(text)
        if results:
            self.statusCode = 'TEXT'
            return results

        self.statusCode = 'FAILED'


    def extractDebt(self, url):
        text, code = self._getFile(url)
        if text:
            results = self._parseWatefall(text)
            return results

