import regexExp
import re
from baseExtractor import BaseExtractor
import dateutil.parser
from bs4 import BeautifulSoup
from resultSet import DebtLineItem


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
        xbrlResults = []
        soup = BeautifulSoup(xbrlSection, 'lxml')
        contextSoup = BeautifulSoup(xbrlContext, 'lxml')

        for (tag, regex) in regexExp.GAAP_RE_DICT.items():
            res = soup.find_all(regex)
            for r in res:
                context = r.get('contextref')
                date = self._findDate(context, contextSoup)
                rawLineItem = DebtLineItem(
                    'XBRL', tag, r.text, date, context
                )
                cleanLineItem = self._cleanAndFilterLineItem(rawLineItem)
                xbrlResults.append(cleanLineItem)

        return xbrlResults

    def processText(self, text):

        xbrlSection, xbrlContextSection = self._getSections(text)
        xbrlResults = self._processSection(xbrlSection, xbrlContextSection)
        return xbrlResults
