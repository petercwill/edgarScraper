import re
import locale
import unicodedata
from abc import ABC, abstractmethod
import edgarScraper.config.regexExp as regexExp
from edgarScraper.pipelineIO.resultSet import DebtLineItem


class BaseExtractor(ABC):
    '''
    base class for different extractors
    '''

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    @abstractmethod
    def processText(self, url):
        '''
        Child class must implement
        '''
        pass

    @abstractmethod
    def _getSections(self):
        '''
        Child class must implement
        '''
        pass

    @abstractmethod
    def _processSection(self):
        '''
        Child class must implement
        '''
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
            return

    def _converttoCaps(self, lineItem):
        if lineItem.elementType != "XBRL":

            return DebtLineItem(
                lineItem.elementType,
                lineItem.name.upper(),
                lineItem.value,
                lineItem.date,
                lineItem.context
            )
        else:
            return lineItem

    def _cleanAndFilterLineItem(self, lineItem):
        '''
        converts a raw line item into a cleaned one.  Filters out spurious
        matches, and handles string cleaning and number parsing. 
        '''

        name = re.sub(r'[^0-9a-zA-Z]+', ' ', lineItem.name).strip()
        if re.search(regexExp.FILTER, name):
            return

        else:
            val = re.sub('(blank)|-+', '0.0', lineItem.value)
            val = re.sub(r'[\(\)]', '', val).strip()
            if val == '':
                val = '0.0'
            val = self._tryToAtoF(val)
            if not (val is None):

                li = DebtLineItem(
                    lineItem.elementType,
                    name,
                    val,
                    lineItem.date,
                    lineItem.context
                )

                li = self._converttoCaps(li)
                return li

    def _matchRows(self, regexExp, row_string, kind):
        '''
        Attempts to form a raw line item from a given string, by matching
        against list of regular expressions.  Returns cleaned line item.
        '''

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

    def _string2LineItem(self, string, kind):
        '''
        First searches for presence of short term debt signifiers.  Then
        long term debt signifiers.
        '''
        result = self._matchRows(
            regexExp.SHORT_TERM,
            string,
            kind
        )
        if result:
            return result

        result = self._matchRows(
            regexExp.LONG_TERM,
            string,
            kind
        )
        return result
