import requests
from edgarScraper.extractors.xbrlExtractor import XBRLExtractor
from edgarScraper.extractors.htmlExtractor import HTMLExtractor
from edgarScraper.extractors.textExtractor import TextExtractor
from edgarScraper.config.log import urlLogger
# from edgarScraper.pipelineIO.fileUrlGenerator import FileUrlGenerator
from edgarScraper.pipelineIO.resultSet import ResultSet


class ResultGenerator(object):

    def __init__(self, years=None, ciks=None, maxFiles=1000, nProcesses=8):
        self.log = urlLogger
        self.xbrlExtractor = XBRLExtractor()
        self.htmlExtractor = HTMLExtractor()
        self.textExtractor = TextExtractor()
        # self.urlGen = FileUrlGenerator(years, ciks, nProcesses)
        # self.maxFiles = maxFiles
        # self.xbrlCount = 0
        # self.htmlCount = 0
        # self.textCount = 0
        # self.failCount = 0

    def _getFile(self, url):
        self.log.debug('Getting {}'.format(url))
        response = requests.get(url)
        code = response.status_code
        if code != 200:
            self.log.error(
                'File {} returned non 200 response code {}.'.format(
                    url, code
                )
            )
            return (None, code)
        else:
            return (response.text, code)

    def _parseWatefall(self, text):

        if not text:
            return ([], 'BAD_URL')

        lineItems = self.xbrlExtractor.processText(text)
        if lineItems:
            # self.xbrlCount += 1
            return (lineItems, 'XBRL')

        lineItems = self.htmlExtractor.processText(text)
        if lineItems:
            # self.htmlCount += 1
            return (lineItems, 'HTML')

        lineItems = self.textExtractor.processText(text)
        if lineItems:
            # self.textCount += 1
            return (lineItems, 'TEXT')

        # self.failCount += 1
        return ([], 'FAILED')

    def fileUrl2Result(self, indexResult):
        text, code = self._getFile(indexResult.url)

        lineItems, extractCode = self._parseWatefall(text)
        self.log.debug(
            'Extracted {} possible lineItems using {}'.format(
                len(lineItems),
                extractCode
                )
        )
        rs = ResultSet(
            lineItems,
            indexResult.cik,
            indexResult.name,
            indexResult.date,
            extractCode
        )

        rs.processLineItems()            
        return rs

    # def getResultGenerator(self):
    #     count = 0
    #     for indexResult in self.urlGen.getUrlGenerator():

    #         if count >= self.maxFiles:
    #             break

    #         lineItems = self.url2LineItems(indexResult.url)
    #         rs = ResultSet(
    #             lineItems,
    #             indexResult.cik,
    #             indexResult.name,
    #             indexResult.date
    #         )

    #         rs.processLineItems()
    #         count += 1

    #         if count % 100 == 0:
    #             self.log.info(
    #                 'Total {}: Xbrl: {}, Html: {}, Text: {}'
    #                 ', Failures: {}'.format(
    #                         count,
    #                         self.xbrlCount,
    #                         self.htmlCount,
    #                         self.textCount,
    #                         self.failCount
    #                     )
    #             )

    #         yield rs
