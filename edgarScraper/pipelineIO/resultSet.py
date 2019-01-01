from collections import namedtuple
import nltk
import numpy as np
from config.constants import (
    LONG_TERM_GAAP, SHORT_TERM_GAAP, RAW_PHRASES, RAW_PHRASE_GRAMS, RAW_TO_GAAP
)

DebtLineItem = namedtuple(
    'DebtLineItem', 'elementType name value date context')


class ResultSet(object):

    def __init__(self, url, jacThreshold=.3):

        # final results
        self.finalLongTerm = None
        self.finalShortTerm = None
        self.url = url
        self.jacThreshold = jacThreshold

        for item in SHORT_TERM_GAAP + LONG_TERM_GAAP:
            setattr(self, item, None)

    def addXRBLLineItem(self, lineItem):

        if not hasattr(self, lineItem.name):
            raise ValueError('Bad Item')

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

    def addHTMLLineItem(self, lineItem):

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
            print('Rejecting {} due to bad match similarity'.format(lineItem))

        else:
            curr = getattr(self, attrName)
            if curr is None:
                setattr(self, attrName, lineItem)

            else:

                # heuristic 1 shorter names are better / more germain
                if len(curr.name) > len(lineItem.name):
                    setattr(self, attrName, lineItem)

    def processLineItems(self, lineItems):

        for li in lineItems:
            if li.elementType == "XBRL":
                self.addXRBLLineItem(li)

            elif li.elementType == 'HTML':
                self.addHTMLLineItem(li)

    def rollUp(self, resultAttr, childAttrs):
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

            rollUpResult = DebtLineItem("Roll Up", resultAttr, val, None, None)
            setattr(self, resultAttr, rollUpResult)

    def formIntermediateResults(self):
        if not self.LongTermNotesPayable:

            self.rollUp(
                "LongTermNotesPayable",
                [
                    "OtherLongTermNotesPayable",
                    "NotesPayableToBankNoncurrent",
                    "ConvertibleLongTermNotesPayable",
                    "SeniorLongTermNotes",
                    "JuniorSubordinatedLongTermNotes"
                ]
            )

        if not self.LongTermLoansPayable:

            self.rollUp(
                "LongTermLoansPayable",
                [
                    "OtherLoansPayableLongTerm",
                    "LongTermLoansFromBank"
                ]
            )

        if not self.LongTermNotesAndLoans:

            self.rollUp(
                "LongTermNotesAndLoans",
                [
                    "LongTermNotesPayable",
                    "LongTermLoansPayable"
                ]
            )

        if not self.LongTermDebtNoncurrent:

            self.rollUp(
                "LongTermDebtNoncurrent",
                [
                    "OtherLongTermDebtNoncurrent"
                    "LongTermNotesAndLoans",
                    "LongTermPollutionControlBond",
                    "LongTermTransitionBond",
                    "ConvertibleSubordinatedDebtNoncurrent",
                    "ConvertibleDebtNoncurrent",
                    "UnsecuredLongTermDebt",
                    "SubordinatedLongTermDebt",
                    "SecuredLongTermDebt",
                    "ConstructionLoanNoncurrent",
                    "CommercialPaperNoncurrent",
                    "LongTermLineOfCredit"

                ]
            )

        if not self.LoansPayableCurrent:

            self.rollUp(
                "LoansPayableCurrent",
                [
                    "LoansPayableToBankCurrent",
                    "OtherLoansPayableCurrent"
                ]
            )

        if not self.NotesPayableCurrent:

            self.rollUp(
                "NotesPayableCurrent",
                [
                    "MediumtermNotesCurrent",
                    "ConvertibleNotesPayableCurrent",
                    "NotesPayableToBankCurrent",
                    "SeniorNotesCurrent",
                    "JuniorSubordinatedNotesCurrent",
                    "OtherNotesPayableCurrent"
                ]
            )

        if not self.NotesAndLoansPayableCurrent:

            self.rollUp(
                "NotesAndLoansPayableCurrent",
                [
                    "LoansPayableCurrent",
                    "NotesPayableCurrent"
                ]
            )

        if not self.LongTermDebtCurrent:

            self.rollUp(
                "LongTermDebtCurrent",
                [
                    "SecuredDebtCurrent",
                    "ConvertibleDebtCurrent",
                    "UnsecuredDebtCurrent",
                    "SubordinatedDebtCurrent",
                    "ConvertibleSubordinatedDebtCurrent",
                    "LongTermCommercialPaperCurrent",
                    "LongTermConstructionLoanCurrent",
                    "LongtermTransitionBondCurrent",
                    "LongtermPollutionControlBondCurrent",
                    "OtherLongTermDebtCurrent",
                    "LinesOfCreditCurrent",
                    "NotesAndLoansPayableCurrent"
                ]
            )

        if not self.LongTermDebtAndCapitalLeaseObligationsCurrent:

            self.rollUp(
                "LongTermDebtAndCapitalLeaseObligationsCurrent",
                [
                    "LongTermDebtCurrent",
                    "CapitalLeaseObligationsCurrent"
                ]
            )

        if not self.ShortTermBorrowings:

            self.rollUp(
                "ShortTermBorrowings",
                [
                    "BankOverdrafts",
                    "CommercialPaper",
                    "BridgeLoan",
                    "ConstructionLoan",
                    "ShortTermBankLoansAndNotesPayable",
                    "ShortTermNonBankLoansAndNotesPayable",
                    "SecuritiesSoldUnderAgreementsToRepurchase",
                    "WarehouseAgreementBorrowings",
                    "OtherShortTermBorrowings",
                ]
            )

        if not self.DebtCurrent:

            self.rollUp(
                "DebtCurrent",
                [
                    "LongTermDebtAndCapitalLeaseObligationsCurrent",
                    "ShortTermBorrowings"
                ]
            )

        if not self.AccountsPayableAndAccruedLiabilitiesCurrent:

            self.rollup(
                "AccountsPayableAndAccruedLiabilitiesCurrent",
                [
                    "AccountsPayableCurrent",
                    "AccountsPayableTradeCurrent",
                    "AccountsPayableOtherCurrent",
                    "AccruedLiabilitiesCurrent",
                    "OtherAccruedLiabilitiesCurrent",
                    "AccountsPayableRelatedPartiesCurrent"
                ]
            )

    def formFinalLongTermResult(self):

        # reference http://www.xbrlsite.com/US-GAAP/Templates/2010-09-30/
        # BalanceSheet/abc-20101231_MeasureRelations.html

        if self.LongTermDebtNoncurrent:
            self.finalLongTerm = self.LongTermDebtNoncurrent.value

        elif self.CapitalLeaseObligationsNoncurrent:

            self.finalLongTerm = (
                self.LongTermDebtAndCapitalLeaseObligations.value
            )

            if self.CapitalLeaseObligationsNoncurrent:
                self.finalLongTerm -= (
                    self.CapitalLeaseObligationsNoncurrent.value
                )

        elif self.LiabilitiesNoncurrent:
            self.finalLongTerm = self.LiabilitiesNoncurrent.value

            if self.LiabilitiesOtherThanLongtermDebtNoncurrent:
                self.finalLongTerm -= (
                    self.LiabilitiesOtherThanLongtermDebtNoncurrent.value
                )

    def formFinalShortTermResult(self):

        if self.ShortTermBorrowings:
            self.finalShortTerm = self.ShortTermBorrowings.value

        elif self.DebtCurrent:
            self.finalShortTerm = self.DebtCurrent.value

            if self.LongTermDebtAndCapitalLeaseObligationsCurrent:
                self.finalShortTerm -= (
                    self.LongTermDebtAndCapitalLeaseObligationsCurrent.value
                )

        elif self.LiabilitiesCurrent:
            self.finalShortTerm = self.LiabilitiesCurrent.value

        elif self.AccountsPayableAndAccruedLiabilitiesCurrent:
            self.finalShortTerm = (
                self.AccountsPayableAndAccruedLiabilitiesCurrent.value
            )

    def __str__(self):

        returnStrings = ["RESULT_SET"]

        for term in SHORT_TERM_GAAP + LONG_TERM_GAAP:
            res = getattr(self, term)
            if res:
                returnStrings.append("{}".format(res))

        return "\t\n".join(returnStrings)

