import nltk

# short term debt signifiers.  See reference:
# http://www.xbrlsite.com/2014/Protototype/Classes/
# currentLiabilities_Tree.html

SHORT_TERM_GAAP = [
    "LoansPayableToBankCurrent",
    "OtherLoansPayableCurrent",
    "MediumtermNotesCurrent",
    "ConvertibleNotesPayableCurrent",
    "NotesPayableToBankCurrent",
    "SeniorNotesCurrent",
    "JuniorSubordinatedNotesCurrent",
    "OtherNotesPayableCurrent",
    "LoansPayableCurrent",
    "NotesPayableCurrent",
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
    "NotesAndLoansPayableCurrent",
    "LongTermDebtCurrent",
    "CapitalLeaseObligationsCurrent",
    "BankOverdrafts",
    "CommercialPaper",
    "BridgeLoan",
    "ConstructionLoan",
    "ShortTermBankLoansAndNotesPayable",
    "ShortTermNonBankLoansAndNotesPayable",
    "SecuritiesSoldUnderAgreementsToRepurchase",
    "WarehouseAgreementBorrowings",
    "OtherShortTermBorrowings",
    "DebtCurrent",
    "LongTermDebtAndCapitalLeaseObligationsCurrent",
    "ShortTermBorrowings",
    "LiabilitiesCurrent",
    "AccountsPayableAndAccruedLiabilitiesCurrent",
    "AccountsPayableCurrent",
    "AccountsPayableTradeCurrent",
    "AccountsPayableOtherCurrent",
    "AccruedLiabilitiesCurrent",
    "OtherAccruedLiabilitiesCurrent",
    "AccountsPayableRelatedPartiesCurrent"
]

# Long term debt signifiers.  See reference:
# http://www.xbrlsite.com/2014/Protototype/Classes/
# currentLiabilities_Tree.html

LONG_TERM_GAAP = [
    "LongTermNotesPayable",
    "OtherLongTermNotesPayable",
    "NotesPayableToBankNoncurrent",
    "ConvertibleLongTermNotesPayable",
    "SeniorLongTermNotes",
    "JuniorSubordinatedLongTermNotes",
    "OtherLoansPayableLongTerm",
    "LongTermLoansFromBank"
    "LongTermNotesAndLoans",
    "LongTermLoansPayable",
    "LongTermDebtNoncurrent",
    "OtherLongTermDebtNoncurrent",
    "LongTermPollutionControlBond",
    "LongTermTransitionBond",
    "ConvertibleSubordinatedDebtNoncurrent",
    "ConvertibleDebtNoncurrent",
    "UnsecuredLongTermDebt",
    "SubordinatedLongTermDebt",
    "SecuredLongTermDebt",
    "ConstructionLoanNoncurrent",
    "CommercialPaperNoncurrent",
    "LongTermLineOfCredit",
    "CapitalLeaseObligationsNoncurrent",
    "LongTermDebtAndCapitalLeaseObligations",
    "LiabilitiesOtherThanLongtermDebtNoncurrent",
    "LiabilitiesNoncurrent"
]

# mapping between common phrase extracted during HTML / Text processing
# and gaap standard terminology

RAW_TO_GAAP = {
    "ACCOUNTS PAYABLE": "AccountsPayableCurrent",

    "ACCOUNTS PAYABLE AND ACCRUED EXPENSES":
    "AccountsPayableAndAccruedLiabilitiesCurrent",

    "ACCOUNTS PAYABLE AND ACCRUED LIABILITIES":
    "AccountsPayableAndAccruedLiabilitiesCurrent",

    "ACCOUNTS PAYABLE AND OTHER ACCRUED LIABILITIES":
    "AccountsPayableAndAccruedLiabilitiesCurrent",

    "ACCOUNTS PAYABLE AND OTHER LIABILITIES":
    "AccountsPayableAndAccruedLiabilitiesCurrent",

    "ACCOUNTS PAYABLE RELATED PARTIES":
    "AccountsPayableRelatedPartiesCurrent",

    "ACCOUNTS PAYABLE TRADE": "AccountsPayableTradeCurrent",

    "ACCRUED AND OTHER CURRENT LIABILITIES": "LiabilitiesCurrent",

    "ACCRUED EXPENSES AND OTHER CURRENT LIABILITIES":
    "OtherAccruedLiabilitiesCurrent",

    "CURRENT INSTALLMENTS OF LONG TERM DEBT": "LongTermDebtCurrent",

    "CURRENT LIABILITIES": "LiabilitiesCurrent",

    "CURRENT LIABILITIES OF DISCONTINUED OPERATIONS":
    "OtherAccruedLiabilitiesCurrent",

    "CURRENT MATURITIES OF LONG TERM DEBT": "LongTermDebtCurrent",

    "CURRENT PORTION OF LONG TERM DEBT": "LongTermDebtCurrent",

    "LONG TERM DEBT": "LongTermDebtNoncurrent",

    "LONG TERM DEBT LESS CURRENT INSTALLMENTS": "LongTermDebtNoncurrent",

    "LONG TERM DEBT LESS CURRENT MATURITIES": "LongTermDebtNoncurrent",

    "LONG TERM DEBT LESS CURRENT PORTION": "LongTermDebtNoncurrent",

    "LONG TERM DEBT NET OF CURRENT PORTION": "LongTermDebtNoncurrent",

    "LONG TERM LIABILITIES": "LiabilitiesNoncurrent",

    "OTHER CURRENT LIABILITIES": "OtherAccruedLiabilitiesCurrent",

    "OTHER LONG TERM LIABILITIES":
    "LiabilitiesOtherThanLongtermDebtNoncurrent",

    "OTHER NON CURRENT LIABILITIES":
    "LiabilitiesOtherThanLongtermDebtNoncurrent",

    "OTHER NONCURRENT LIABILITIES":
    "LiabilitiesOtherThanLongtermDebtNoncurrent",

    "OTHER SHORT TERM BORROWINGS": "OtherShortTermBorrowings",

    "SHORT TERM BORROWINGS": "ShortTermBorrowings",

    "SHORT TERM DEBT": "ShortTermBorrowings",

    "TOTAL CURRENT LIABILITIES": "LiabilitiesCurrent",

    "TOTAL LIABILITIES": "LiabilitiesNoncurrent",

    "TOTAL LIABILITIES ASSUMED": "LiabilitiesNoncurrent",

    "TOTAL LIABILITIES AT FAIR VALUE": "LiabilitiesNoncurrent",

    "TOTAL LIABILITIES MEASURED AT FAIR VALUE": "LiabilitiesNoncurrent",

    "TOTAL LONG TERM LIABILITIES": "LiabilitiesNoncurrent",

    "TOTAL NON CURRENT LIABILITIES": "LiabilitiesNoncurrent",

    "TRADE ACCOUNTS PAYABLE": "AccountsPayableTradeCurrent",
}


RAW_PHRASES = list(RAW_TO_GAAP.keys())

# compute trigram sets for phrases
RAW_PHRASE_GRAMS = [set(nltk.ngrams(w, n=3)) for w in RAW_PHRASES]
