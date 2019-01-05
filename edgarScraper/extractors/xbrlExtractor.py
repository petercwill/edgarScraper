import re
import dateutil.parser
from bs4 import BeautifulSoup
from edgarScraper.extractors.baseExtractor import BaseExtractor
import edgarScraper.config.regexExp as regexExp
from edgarScraper.pipelineIO.resultSet import DebtLineItem


class XBRLExtractor(BaseExtractor):

    def __init__(self):
        pass

    def _findDate(self, context, soup):

        contextElm = soup.find(regexExp.XBRL_CONTEXT, {"id": context})
        dateElm = contextElm.find(regexExp.XBRL_DATE)
        return dateutil.parser.parse(dateElm.text)

    def _getSections(self, text):
        xbrlSection = "\n".join(
            [result for result in re.findall(regexExp.XBRL_SECTION, text)]
        )
        xbrlContextSection = "\n".join(
            [result for result in re.findall(
                regexExp.XBRL_CONTEXT_SECTION, text
            )]
        )

        return (xbrlSection, xbrlContextSection or xbrlSection)

    def _processSection(self, xbrlSection, xbrlContext):
        xbrlLineItems = []
        soup = BeautifulSoup(xbrlSection, 'lxml')
        contextSoup = BeautifulSoup(xbrlContext, 'lxml')

        for r in soup.find_all(regexExp.GAAP_RE):
            name = re.sub('us-gaap:', '', r.name).strip().upper()
            context = r.get('contextref')
            date = self._findDate(context, contextSoup)
            rawLineItem = DebtLineItem(
                'XBRL', name, r.text, date, context
            )
            cleanLineItem = self._cleanAndFilterLineItem(rawLineItem)
            xbrlLineItems.append(cleanLineItem)

        return xbrlLineItems

    def processText(self, text):

        xbrlSection, xbrlContextSection = self._getSections(text)
        xbrlLineItems = self._processSection(xbrlSection, xbrlContextSection)
        return xbrlLineItems
