from abc import ABC, abstractmethod
import regexExp
from resultSet import DebtLineItem
import unicodedata
import locale
import re


class BaseExtractor(ABC):

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    @abstractmethod
    def processText(self, url):
        pass

    @abstractmethod
    def _getSections(self):
        pass

    @abstractmethod
    def _processSection(self):
        pass

    def _cleanString(self, string):
        string = unicodedata.normalize("NFKD", string)
        string = re.sub(regexExp.NOTES, '', string)
        return string

    def _tryToAtoF(self, value):
        try:
            value = locale.atof(value)
            return value
        except ValueError:
            print('Skipping Match, unable to convert to numeric')
            return

    def _cleanAndFilterLineItem(self, lineItem):


        name = re.sub(r'[^0-9a-zA-Z]+', ' ', lineItem.name).strip()
        if re.search(regexExp.FILTER, name):
            print('filtering {}'.format(name))
            return

        else:
            val = re.sub('(blank)|-+', '0.0', lineItem.value)
            val = re.sub(r'[\(\)]', '', val).strip()
            if val == '':
                val = '0.0'
            val = self._tryToAtoF(val)

        return DebtLineItem(
            lineItem.elementType,
            name,
            val,
            lineItem.date,
            lineItem.context
        )

    def _matchRows(self, regexExp, row_string, kind):
        m = re.match(regexExp, row_string)
        if m:
            rawLineItem = DebtLineItem(
                kind,
                m.group('name'),
                m.group('value'),
                None,
                None
            )
            cleanLineItem = self._cleanAndFilterLineItem(rawLineItem)
            return cleanLineItem

    def _string2Result(self, string, kind):

        result = self._matchRows(
            regexExp.SHORT_TERM,
            string,
            kind
        )
        if result:
            return result

        result = self._matchRows(
            regexExp.SHORT_TERM,
            string,
            kind
        )
        return result
