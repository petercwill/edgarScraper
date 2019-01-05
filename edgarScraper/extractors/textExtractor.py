import re
import edgarScraper.config.regexExp as regexExp
from edgarScraper.extractors.baseExtractor import BaseExtractor


class TextExtractor(BaseExtractor):

    def __init__(self):
        pass

    def _getRelevantTables(self, text):
        for table in re.findall(regexExp.TABLE_SECTION, text):
            if (
                re.search(regexExp.BALANCE_SHEET, table) and
                re.search(regexExp.LIABILITIES, table)
            ):
                yield table
                break

            elif re.search(regexExp.LIABILITIES, table):
                yield table

    def _getRelevantFreeText(self, text, chunkSize=100):
        textLines = text.split('\n')
        regex = re.compile('BALANCE SHEET', re.IGNORECASE)
        lineNum = 0
        while lineNum < len(textLines):
            line = textLines[lineNum]
            if re.search(regex, line):
                yield "\n".join(textLines[lineNum:lineNum + chunkSize])
            lineNum += 1

    def _getColumnPos(self, lines):
        for line in lines:
            m = re.match(regexExp.TEXT_TABLE_COLUMNS, line)
            if m:

                startInd = m.start()
                endInd = m.end() - 1
                midInd = re.search(
                    re.compile(r'<c>', re.I), m.group(0)
                ).start()

                return(startInd, midInd, endInd)

    def _parseTableByPosition(self, lines):
        inds = self._getColumnPos(lines)
        if inds:
            startInd, midInd, endInd = inds
            lineNo = 0
            while lineNo < len(lines):
                line = lines[lineNo]
                name = line[startInd:midInd]
                val = line[midInd:endInd]

                if (line[midInd:].isspace()) or line[midInd:] == '':

                    # read next line
                    lineNo += 1
                    if lineNo >= len(lines):
                        continue

                    line = lines[lineNo]

                    if (
                        line[midInd:].isspace() or
                        line[midInd:] == ''
                    ):

                        # two line breaks, revert
                        lineNo -= 1

                    else:
                        name += line[startInd:midInd]
                        val = line[midInd:endInd]

                lineNo += 1
                yield name + "   " + val

    def _getSections(self, text):
        textSection = "\n".join(
            [result for result in re.findall(regexExp.TEXT_SECTION, text)]
        )
        return self._cleanString(textSection)

    def _freeSearchText(self, text):
        results = []
        for chunk in self._getRelevantFreeText(text):

            for m in re.finditer(regexExp.FREE_TEXT_SHORT_TERM, chunk):
                name = re.sub(r'\n', ' ', m.group('name'))
                name = re.sub(r'\s{3,}', '   ', name)
                value = m.group('value')
                row_string = name + "   " + value
                result = self._string2LineItem(row_string, 'TEXT')
                results.append(result)

        return(list(filter(None, results)))

    def _lookForTables(self, text):
        results = []
        for table in self._getRelevantTables(text):
            lines = table.split("\n")
            for row_string in self._parseTableByPosition(lines):
                result = self._string2LineItem(row_string, 'TEXT')
                results.append(result)

        return(list(filter(None, results)))

    def _processSection(self, text):
        results = self._lookForTables(text)
        if not results:
            results = self._freeSearchText(text)

        return results

    def processText(self, text):
        textSections = self._getSections(text)
        textLineItems = self._processSection(textSections)
        return textLineItems

