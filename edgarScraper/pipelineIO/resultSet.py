from collections import namedtuple
import nltk
import numpy as np
from edgarScraper.config.constants import (
    LONG_TERM_GAAP, SHORT_TERM_GAAP, RAW_PHRASES, RAW_PHRASE_GRAMS, RAW_TO_GAAP
)
from edgarScraper.config.log import (
    urlLogger, rejectedMatchLogger, matchLogger, edgarScraperLog
)

DebtLineItem = namedtuple(
    'DebtLineItem', 'elementType name value date context'
)

DebtDisclosure = namedtuple(
    'DebtDisclosure', 'DATE CIK ELEMENTYPE TEXT'
)


class ResultSet(object):

    def __init__(
        self,
        lineItems,
        cik=None,
        name=None,
        date=None,
        extractCode=None,
        jacThreshold=.4
    ):
        self.lineItems = lineItems
        self.CIK = cik
        self.NAME = name
        self.DATE = date
        self.EXTRACTCODE = extractCode
        self.jacThreshold = jacThreshold
        self.FINALLONGTERM = None
        self.FINALSHORTTERM = None
        self.urlLog = urlLogger
        self.rejectLog = rejectedMatchLogger
        self.matchLog = matchLogger
        self.writeAttrs = (
            [
                "CIK", "NAME", "DATE", "FINALSHORTTERM", "FINALLONGTERM",
                "EXTRACTCODE"
            ]
        )

        for item in SHORT_TERM_GAAP + LONG_TERM_GAAP:
            setattr(self, item, None)

    def addXRBLLineItem(self, lineItem):

        if not hasattr(self, lineItem.name):
            edgarScraperLog.error(
                'bad xbrl match found for {}'.format(lineItem.name)
            )
            print(lineItem)
            return

        curr = getattr(self, lineItem.name)
        if curr is None:
            setattr(self, lineItem.name, lineItem)

        else:

            # heuristic 1 shorter contexts are better / more germain
            if len(curr.context) > len(lineItem.context):
                setattr(self, lineItem.name, lineItem)

            # heuristic 2 more recent information is better
            elif (
                len(curr.context) == len(lineItem.context)
            ) and (curr.date < lineItem.date):
                setattr(self, lineItem.name, lineItem)

    def addAndMatchLineItem(self, lineItem):

        nameGrams = set(nltk.ngrams(lineItem.name.upper(), n=3))
        simScores = [
            nltk.jaccard_distance(nameGrams, wGram)
            for wGram in RAW_PHRASE_GRAMS
        ]
        matchInd = np.argmin(simScores)
        jacScore = simScores[matchInd]
        matchWord = RAW_PHRASES[matchInd]
        attrName = RAW_TO_GAAP[matchWord]

        if jacScore > self.jacThreshold:
            self.rejectLog.debug('{}'.format(lineItem.name))

        else:
            self.matchLog.debug('{}||{}'.format(lineItem.name, matchWord))
            curr = getattr(self, attrName)
            if curr is None:
                setattr(self, attrName, lineItem)

            else:

                # heuristic 1 shorter names are better / more germain
                if len(curr.name) > len(lineItem.name):
                    setattr(self, attrName, lineItem)

    def processLineItems(self):
        if not self.lineItems:
            return

        for li in self.lineItems:
            if li.elementType == "XBRL":
                self.addXRBLLineItem(li)

            else:
                self.addAndMatchLineItem(li)

        self.formIntermediateResults()
        self.formFinalLongTermResult()
        self.formFinalShortTermResult()

    def _rollUp(self, resultAttr, childAttrs):
        if all(getattr(self, c) is None for c in childAttrs):
            setattr(self, resultAttr, None)

        else:
            totalVal = 0
            for c in childAttrs:
                if getattr(self, c) is None:
                    val = 0
                else:
                    val = getattr(self, c).value
                totalVal += val

            rollUpResult = DebtLineItem(
                "Roll Up",
                resultAttr,
                totalVal,
                None,
                None
            )
            setattr(self, resultAttr, rollUpResult)

    def formIntermediateResults(self):
        if not self.LONGTERMNOTESPAYABLE:

            self._rollUp(
                "LONGTERMNOTESPAYABLE",
                [
                    "OTHERLONGTERMNOTESPAYABLE",
                    "NOTESPAYABLETOBANKNONCURRENT",
                    "CONVERTIBLELONGTERMNOTESPAYABLE",
                    "SENIORLONGTERMNOTES",
                    "JUNIORSUBORDINATEDLONGTERMNOTES"
                ]
            )

        if not self.LONGTERMLOANSPAYABLE:

            self._rollUp(
                "LONGTERMLOANSPAYABLE",
                [
                    "OTHERLOANSPAYABLELONGTERM",
                    "LONGTERMLOANSFROMBANK"
                ]
            )

        if not self.LONGTERMNOTESANDLOANS:

            self._rollUp(
                "LONGTERMNOTESANDLOANS",
                [
                    "LONGTERMNOTESPAYABLE",
                    "LONGTERMLOANSPAYABLE"
                ]
            )

        if not self.LONGTERMDEBTNONCURRENT:

            self._rollUp(
                "LONGTERMDEBTNONCURRENT",
                [
                    "OTHERLONGTERMDEBTNONCURRENT",
                    "LONGTERMNOTESANDLOANS",
                    "LONGTERMTRANSITIONBOND",
                    "CONVERTIBLESUBORDINATEDDEBTNONCURRENT",
                    "CONVERTIBLEDEBTNONCURRENT",
                    "UNSECUREDLONGTERMDEBT",
                    "SUBORDINATEDLONGTERMDEBT",
                    "SECUREDLONGTERMDEBT",
                    "CONSTRUCTIONLOANNONCURRENT",
                    "COMMERCIALPAPERNONCURRENT",
                    "LONGTERMLINEOFCREDIT"

                ]
            )

        if not self.LOANSPAYABLECURRENT:

            self._rollUp(
                "LOANSPAYABLECURRENT",
                [
                    "LOANSPAYABLETOBANKCURRENT",
                    "OTHERLOANSPAYABLECURRENT"
                ]
            )

        if not self.NOTESPAYABLECURRENT:

            self._rollUp(
                "NOTESPAYABLECURRENT",
                [
                    "MEDIUMTERMNOTESCURRENT",
                    "CONVERTIBLENOTESPAYABLECURRENT",
                    "NOTESPAYABLETOBANKCURRENT",
                    "SENIORNOTESCURRENT",
                    "JUNIORSUBORDINATEDNOTESCURRENT",
                    "OTHERNOTESPAYABLECURRENT"
                ]
            )

        if not self.NOTESANDLOANSPAYABLECURRENT:

            self._rollUp(
                "NOTESANDLOANSPAYABLECURRENT",
                [
                    "LOANSPAYABLECURRENT",
                    "NOTESPAYABLECURRENT"
                ]
            )

        if not self.LONGTERMDEBTCURRENT:

            self._rollUp(
                "LONGTERMDEBTCURRENT",
                [
                    "SECUREDDEBTCURRENT",
                    "CONVERTIBLEDEBTCURRENT",
                    "UNSECUREDDEBTCURRENT",
                    "SUBORDINATEDDEBTCURRENT",
                    "CONVERTIBLESUBORDINATEDDEBTCURRENT",
                    "LONGTERMCOMMERCIALPAPERCURRENT",
                    "LONGTERMCONSTRUCTIONLOANCURRENT",
                    "LONGTERMTRANSITIONBONDCURRENT",
                    "LONGTERMPOLLUTIONCONTROLBONDCURRENT",
                    "OTHERLONGTERMDEBTCURRENT",
                    "LINESOFCREDITCURRENT",
                    "NOTESANDLOANSPAYABLECURRENT"
                ]
            )

        if not self.LONGTERMDEBTANDCAPITALLEASEOBLIGATIONSCURRENT:

            self._rollUp(
                "LONGTERMDEBTANDCAPITALLEASEOBLIGATIONSCURRENT",
                [
                    "LONGTERMDEBTCURRENT",
                    "CAPITALLEASEOBLIGATIONSCURRENT"
                ]
            )

        if not self.SHORTTERMBORROWINGS:

            self._rollUp(
                "SHORTTERMBORROWINGS",
                [
                    "BANKOVERDRAFTS",
                    "COMMERCIALPAPER",
                    "BRIDGELOAN",
                    "CONSTRUCTIONLOAN",
                    "SHORTTERMBANKLOANSANDNOTESPAYABLE",
                    "SHORTTERMNONBANKLOANSANDNOTESPAYABLE",
                    "SECURITIESSOLDUNDERAGREEMENTSTOREPURCHASE",
                    "WAREHOUSEAGREEMENTBORROWINGS",
                    "OTHERSHORTTERMBORROWINGS",
                ]
            )

        if not self.DEBTCURRENT:

            self._rollUp(
                "DEBTCURRENT",
                [
                    "LONGTERMDEBTANDCAPITALLEASEOBLIGATIONSCURRENT",
                    "SHORTTERMBORROWINGS"
                ]
            )

        if not self.ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT:

            self._rollUp(
                "ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT",
                [
                    "ACCOUNTSPAYABLECURRENT",
                    "ACCOUNTSPAYABLETRADECURRENT",
                    "ACCOUNTSPAYABLEOTHERCURRENT",
                    "ACCRUEDLIABILITIESCURRENT",
                    "OTHERACCRUEDLIABILITIESCURRENT",
                    "ACCOUNTSPAYABLERELATEDPARTIESCURRENT"
                ]
            )

        if not self.LIABILITIESCURRENT:

            self._rollUp(
                "LIABILITIESCURRENT",
                [
                    "ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT",
                    "DEBTCURRENT",
                    "OTHERLIABILITIESCURRENT"
                ]
            )

    def formFinalLongTermResult(self):

        # reference http://www.xbrlsite.com/2014/Protototype/Classes/
        # currentLiabilities_Tree.html

        if (
            self.LONGTERMDEBTNONCURRENT and
            self.LONGTERMDEBTNONCURRENT.value != 0
        ):
            self.FINALLONGTERM = self.LONGTERMDEBTNONCURRENT.value

        elif (
            self.LONGTERMDEBTANDCAPITALLEASEOBLIGATIONS and
            self.LONGTERMDEBTANDCAPITALLEASEOBLIGATIONS.value != 0
        ):

            self.FINALLONGTERM = (
                self.LONGTERMDEBTANDCAPITALLEASEOBLIGATIONS.value
            )

            if self.CAPITALLEASEOBLIGATIONSNONCURRENT:
                self.FINALLONGTERM -= (
                    self.CAPITALLEASEOBLIGATIONSNONCURRENT.value
                )

        elif self.LIABILITIESNONCURRENT:
            self.FINALLONGTERM = self.LIABILITIESNONCURRENT.value

            if self.LIABILITIESOTHERTHANLONGTERMDEBTNONCURRENT:
                self.FINALLONGTERM -= (
                    self.LIABILITIESOTHERTHANLONGTERMDEBTNONCURRENT.value
                )

    def formFinalShortTermResult(self):

        if self.SHORTTERMBORROWINGS and self.SHORTTERMBORROWINGS != 0:
            self.FINALSHORTTERM = self.SHORTTERMBORROWINGS.value

        elif self.DEBTCURRENT and self.DEBTCURRENT != 0:
            self.FINALSHORTTERM = self.DEBTCURRENT.value

        elif (
            self.ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT
            and self.ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT != 0
        ):
            self.FINALSHORTTERM = (
                self.ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT.value
            )

        elif self.LIABILITIESCURRENT:
            self.FINALSHORTTERM = self.LIABILITIESCURRENT.value

    def __str__(self):

        returnStrings = []

        for term in SHORT_TERM_GAAP + LONG_TERM_GAAP:
            res = getattr(self, term)
            if res:
                returnStrings.append(str(res.value))
            else:
                returnStrings.append("")

        for term in self.writeAttrs:
            res = getattr(self, term)
            if res:
                returnStrings.append(str(res))
            else:
                returnStrings.append("")

        finalString = "||".join(returnStrings) + "\n"
        return finalString

    def _toDict(self):
        d = {
            term: getattr(self, term).value if getattr(self, term) else np.NaN
            for term in SHORT_TERM_GAAP + LONG_TERM_GAAP
        }

        for term in self.writeAttrs:
            d[term] = getattr(self, term)

        return d
