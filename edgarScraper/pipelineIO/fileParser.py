import requests
from edgarScraper.extractors.xbrlExtractor import XBRLExtractor
from edgarScraper.extractors.htmlExtractor import HTMLExtractor
from edgarScraper.extractors.textExtractor import TextExtractor
from edgarScraper.config.log import urlLogger
from edgarScraper.pipelineIO.resultSet import ResultSet, DebtDisclosure


class FileParser(object):

    def __init__(self):
        self.log = urlLogger
        self.xbrlExtractor = XBRLExtractor()
        self.htmlExtractor = HTMLExtractor()
        self.textExtractor = TextExtractor()

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

        debtDisclosure = None
       
        if not text:
            return ([], 'BAD_URL', None)

        lineItems, debtDisclosure = self.xbrlExtractor.processText(text)
        if lineItems:
            # self.xbrlCount += 1
            return (lineItems, 'XBRL', debtDisclosure)

        lineItems = self.htmlExtractor.processText(text)
        if lineItems:
            # self.htmlCount += 1
            return (lineItems, 'HTML', debtDisclosure)

        lineItems = self.textExtractor.processText(text)
        if lineItems:
            # self.textCount += 1
            return (lineItems, 'TEXT', debtDisclosure)

        # self.failCount += 1
        return ([], 'FAILED', debtDisclosure)

    def fileUrl2Result(self, indexResult):
        text, code = self._getFile(indexResult.url)

        lineItems, extractCode, debtDisclosure = self._parseWatefall(text)
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

        dd = DebtDisclosure(
            indexResult.date,
            indexResult.cik,
            extractCode,
            debtDisclosure
        )

        rs.processLineItems()
        return (rs, dd)
