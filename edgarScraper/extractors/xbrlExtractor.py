import re
import dateutil.parser
from bs4 import BeautifulSoup, SoupStrainer
from edgarScraper.extractors.baseExtractor import BaseExtractor
import edgarScraper.config.regexExp as regexExp
from edgarScraper.pipelineIO.resultSet import DebtLineItem
import unicodedata
from edgarScraper.config.log import edgarScraperLog


class XBRLExtractor(BaseExtractor):

    def __init__(self):
        pass

    def _findDate(self, context, soup):

        if not context:
            return None

        contextElm = soup.find(regexExp.XBRL_CONTEXT, {"id": context})

        if contextElm:
            dateElm = contextElm.find(regexExp.XBRL_DATE)

            if dateElm:

                try:
                    date = dateutil.parser.parse(dateElm.text)
                    return date
                
                except ValueError:
                    edgarScraperLog.error(
                        "Date parse error for {}".format(dateElm.text)
                    )

    def _getSections(self, text):

        xbrlSection = "\n".join(
           [result for result in re.findall(regexExp.XBRL_SECTION, text)]
        )

        return xbrlSection

    def _getDebtDisclosure(self, soup):

        for res in soup.find_all(regexExp.DEBT_DISCLOSURE):
            contentSoup = BeautifulSoup(res.text, 'lxml')
            text = unicodedata.normalize("NFKD", contentSoup.text)
            text = re.sub(r"\r\n+", ' ', text)
            text = re.sub(r"\s\s+", " ", text)
            return text

    def _processSection(self, xbrlSection):
        xbrlLineItems = []

        strainer = SoupStrainer(regexExp.XBRL_COMPOSITE_SOUP)
        soup = BeautifulSoup(
            xbrlSection,
            'lxml',
            parse_only=strainer
        )

        debtDisclosureText = self._getDebtDisclosure(soup)

        for r in soup.find_all(regexExp.GAAP_RE):
            name = re.sub('us-gaap:', '', r.name).strip().upper()
            context = r.get('contextref')

            date = self._findDate(context, soup)

            rawLineItem = DebtLineItem(
                'XBRL', name, r.text, date, context
            )
            cleanLineItem = self._cleanAndFilterLineItem(rawLineItem)
            if cleanLineItem:
                xbrlLineItems.append(cleanLineItem)

        return xbrlLineItems, debtDisclosureText

    def processText(self, text):

        xbrlSection = self._getSections(text)
        xbrlLineItems, debtDisclosureText = self._processSection(
            xbrlSection
        )
        return (xbrlLineItems, debtDisclosureText)
