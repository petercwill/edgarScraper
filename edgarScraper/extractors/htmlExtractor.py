import re
import regexExp
from baseExtractor import BaseExtractor
from bs4 import BeautifulSoup


class HTMLExtractor(BaseExtractor):

    def __init__(self):
        pass

    def _row2Text(self, row):
        string = self._cleanString(row)
        string = re.sub(r'\n', ' ', string)
        string = re.sub(r'\s{3,}', r'   ', string)
        string = re.sub(r'[\'\"]', '', string).strip()
        return string

    def _getRelevantTables(self, soup):
        for table in soup.findAll(regexExp.TABLE):
            text = table.text

            if (
                re.search(regexExp.BALANCE_SHEET, text) and
                re.search(regexExp.LIABILITIES, text)
            ):
                yield table
                break

            elif re.search(regexExp.LIABILITIES, text):
                yield table

    def _getReleventElms(self, soup):

        for navString in soup.findAll(text=regexExp.TAGS_WO_NUMS):

            elm = navString.parent.findNext()
            value = elm.text

            while re.match(regexExp.EMPTY_OR_DOLLAR, value):
                elm = elm.findNext()
                value = elm.text

            if re.match(regexExp.NUMBER, value):
                elmString = navString.parent.text + "   " + value
                yield elmString

    def _lookForTables(self, soup):

        results = []
        for table in self._getRelevantTables(soup):
            for row in table.findAll(re.compile("tr", re.I)):
                row_string = self._row2Text(row.text)
                result = self._string2Result(row_string, 'HTML')
                results.append(result)

        return(list(filter(None, results)))

    def _genericElements(self, soup):
        results = []
        for elmString in self._getReleventElms(soup):
            row_string = self._row2Text(elmString)
            result = self._string2Result(row_string, 'HTML')
            results.append(result)

        return(list(filter(None, results)))

    def _getSections(self, text):
        return "\n".join(
            [result for result in re.findall(regexExp.HTML_SECTION, text)]
        )

    def _processSection(self, soup):
        results = self._lookForTables(soup)
        if not results:
            print('HTML Table Search Failed')
            results = self._genericElements(soup)

        return results

    def processText(self, text):
        htmlSections = self._getSections(text)
        soup = BeautifulSoup(htmlSections, features="lxml")
        htmlResults = self._processSection(soup)
        return htmlResults
