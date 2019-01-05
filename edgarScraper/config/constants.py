import nltk

# form index files are fixed width formated.  Character positions of relevent
# fields
NAME_POS = (12, 74)
CIK_POS = (74, 86)
DATE_POS = (86, 98)
PATH_POS = (98, None)


# short term debt signifiers.  See reference:
# http://www.xbrlsite.com/2014/Protototype/Classes/
# currentLiabilities_Tree.html

SHORT_TERM_GAAP = [
    "LOANSPAYABLETOBANKCURRENT",
    "OTHERLOANSPAYABLECURRENT",
    "MEDIUMTERMNOTESCURRENT",
    "CONVERTIBLENOTESPAYABLECURRENT",
    "NOTESPAYABLETOBANKCURRENT",
    "SENIORNOTESCURRENT",
    "JUNIORSUBORDINATEDNOTESCURRENT",
    "OTHERNOTESPAYABLECURRENT",
    "LOANSPAYABLECURRENT",
    "NOTESPAYABLECURRENT",
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
    "NOTESANDLOANSPAYABLECURRENT",
    "LONGTERMDEBTCURRENT",
    "CAPITALLEASEOBLIGATIONSCURRENT",
    "BANKOVERDRAFTS",
    "COMMERCIALPAPER",
    "BRIDGELOAN",
    "CONSTRUCTIONLOAN",
    "SHORTTERMBANKLOANSANDNOTESPAYABLE",
    "SHORTTERMNONBANKLOANSANDNOTESPAYABLE",
    "SECURITIESSOLDUNDERAGREEMENTSTOREPURCHASE",
    "WAREHOUSEAGREEMENTBORROWINGS",
    "OTHERSHORTTERMBORROWINGS",
    "DEBTCURRENT",
    "LONGTERMDEBTANDCAPITALLEASEOBLIGATIONSCURRENT",
    "SHORTTERMBORROWINGS",
    "LIABILITIESCURRENT",
    "ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT",
    "ACCOUNTSPAYABLECURRENT",
    "ACCOUNTSPAYABLETRADECURRENT",
    "ACCOUNTSPAYABLEOTHERCURRENT",
    "ACCRUEDLIABILITIESCURRENT",
    "OTHERACCRUEDLIABILITIESCURRENT",
    "ACCOUNTSPAYABLERELATEDPARTIESCURRENT",
    "OTHERLIABILITIESCURRENT"
]

# Long term debt signifiers.  See reference:
# http://www.xbrlsite.com/2014/Protototype/Classes/
# currentLiabilities_Tree.html

LONG_TERM_GAAP = [
    "LONGTERMNOTESPAYABLE",
    "OTHERLONGTERMNOTESPAYABLE",
    "NOTESPAYABLETOBANKNONCURRENT",
    "CONVERTIBLELONGTERMNOTESPAYABLE",
    "SENIORLONGTERMNOTES",
    "JUNIORSUBORDINATEDLONGTERMNOTES",
    "OTHERLOANSPAYABLELONGTERM",
    "LONGTERMLOANSFROMBANK",
    "LONGTERMNOTESANDLOANS",
    "LONGTERMLOANSPAYABLE",
    "LONGTERMDEBTNONCURRENT",
    "OTHERLONGTERMDEBTNONCURRENT",
    "LONGTERMPOLLUTIONCONTROLBOND",
    "LONGTERMTRANSITIONBOND",
    "CONVERTIBLESUBORDINATEDDEBTNONCURRENT",
    "CONVERTIBLEDEBTNONCURRENT",
    "UNSECUREDLONGTERMDEBT",
    "SUBORDINATEDLONGTERMDEBT",
    "SECUREDLONGTERMDEBT",
    "CONSTRUCTIONLOANNONCURRENT",
    "COMMERCIALPAPERNONCURRENT",
    "LONGTERMLINEOFCREDIT",
    "CAPITALLEASEOBLIGATIONSNONCURRENT",
    "LONGTERMDEBTANDCAPITALLEASEOBLIGATIONS",
    "LIABILITIESOTHERTHANLONGTERMDEBTNONCURRENT",
    "LIABILITIESNONCURRENT"
]

# mapping between common phrase extracted during HTML / Text processing
# and gaap standard terminology

RAW_TO_GAAP = {
    "ACCOUNTS PAYABLE": "ACCOUNTSPAYABLECURRENT",

    "ACCOUNTS PAYABLE AND ACCRUED EXPENSES":
    "ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT",

    "ACCOUNTS PAYABLE AND ACCRUED LIABILITIES":
    "ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT",

    "ACCOUNTS PAYABLE AND OTHER ACCRUED LIABILITIES":
    "ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT",

    "ACCOUNTS PAYABLE AND OTHER LIABILITIES":
    "ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT",

    "ACCOUNTS PAYABLE RELATED PARTIES":
    "ACCOUNTSPAYABLERELATEDPARTIESCURRENT",

    "ACCOUNTS PAYABLE TRADE": "ACCOUNTSPAYABLETRADECURRENT",

    "ACCRUED AND OTHER CURRENT LIABILITIES": "LIABILITIESCURRENT",

    "ACCRUED EXPENSES AND OTHER CURRENT LIABILITIES":
    "OTHERACCRUEDLIABILITIESCURRENT",

    "CURRENT INSTALLMENTS OF LONG TERM DEBT": "LONGTERMDEBTCURRENT",

    "CURRENT LIABILITIES": "LIABILITIESCURRENT",

    "CURRENT LIABILITIES OF DISCONTINUED OPERATIONS":
    "OTHERACCRUEDLIABILITIESCURRENT",

    "CURRENT MATURITIES OF LONG TERM DEBT": "LONGTERMDEBTCURRENT",

    "CURRENT PORTION OF LONG TERM DEBT": "LONGTERMDEBTCURRENT",

    "LONG TERM DEBT": "LONGTERMDEBTNONCURRENT",

    "LONG TERM DEBT LESS CURRENT INSTALLMENTS": "LONGTERMDEBTNONCURRENT",

    "LONG TERM DEBT LESS CURRENT MATURITIES": "LONGTERMDEBTNONCURRENT",

    "LONG TERM DEBT LESS CURRENT PORTION": "LONGTERMDEBTNONCURRENT",

    "LONG TERM DEBT NET OF CURRENT PORTION": "LONGTERMDEBTNONCURRENT",

    "LONG TERM LIABILITIES": "LIABILITIESNONCURRENT",

    "OTHER CURRENT LIABILITIES": "OTHERACCRUEDLIABILITIESCURRENT",

    "OTHER LONG TERM LIABILITIES":
    "LIABILITIESOTHERTHANLONGTERMDEBTNONCURRENT",

    "OTHER NON CURRENT LIABILITIES":
    "LIABILITIESOTHERTHANLONGTERMDEBTNONCURRENT",

    "OTHER NONCURRENT LIABILITIES":
    "LIABILITIESOTHERTHANLONGTERMDEBTNONCURRENT",

    "OTHER SHORT TERM BORROWINGS": "OTHERSHORTTERMBORROWINGS",

    "SHORT TERM BORROWINGS": "SHORTTERMBORROWINGS",

    "SHORT TERM DEBT": "SHORTTERMBORROWINGS",

    "TOTAL CURRENT LIABILITIES": "LIABILITIESCURRENT",

    "TOTAL LIABILITIES": "LIABILITIESNONCURRENT",

    "TOTAL LIABILITIES ASSUMED": "LIABILITIESNONCURRENT",

    "TOTAL LIABILITIES AT FAIR VALUE": "LIABILITIESNONCURRENT",

    "TOTAL LIABILITIES MEASURED AT FAIR VALUE": "LIABILITIESNONCURRENT",

    "TOTAL LONG TERM LIABILITIES": "LIABILITIESNONCURRENT",

    "TOTAL NON CURRENT LIABILITIES": "LIABILITIESNONCURRENT",

    "TRADE ACCOUNTS PAYABLE": "ACCOUNTSPAYABLETRADECURRENT",

    "ACCRUED LIABILITIES": "ACCRUEDLIABILITIESCURRENT",

    "CURRENT LIABILITIES ACCOUNTS PAYABLE": "ACCOUNTSPAYABLECURRENT",

    "CURRENT LIABILITIES NOTES PAYABLE": "NOTESPAYABLECURRENT",

    "OTHER ACCRUED LIABILITIES": "OTHERACCRUEDLIABILITIESCURRENT",

    "CURRENT LIABILITIES CURRENT PORTION OF LONG TERM DEBT":
        "LONGTERMDEBTCURRENT",

    "CURRENT LIABILITIES LONG TERM DEBT DUE WITHIN ONE YEAR":
        "LONGTERMDEBTCURRENT",

    "ACCOUNTS PAYABLE AFFILIATED COMPANIES":
        "ACCOUNTSPAYABLERELATEDPARTIESCURRENT",

    "CURRENT LIABILITIES SHORT TERM DEBT": "SHORTTERMBORROWINGS",

    "CURRENT LIABILITIES SHORT TERM BORROWINGS": "SHORTTERMBORROWINGS",

    "CURRENT LIABILITIES NOTES PAYABLE TO BANKS": "NOTESPAYABLETOBANKCURRENT",

    "CURRENT LIABILITIES ACCOUNTS PAYABLE AND ACCRUED EXPENSES":
        "ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT",

    "CURRENT LIABILITIES CURRENTLY MATURING LONG TERM DEBT":
        "LONGTERMDEBTCURRENT",

    "CURRENT LIABILITIES SHORT TERM DEBT INCLUDING CURRENT MATURITIES":
        "SHORTTERMBORROWINGS",

    "LIABILITIES ACCOUNTS PAYABLE": "ACCOUNTSPAYABLECURRENT",

    "ACCOUNTS PAYABLE AFFILIATES": "ACCOUNTSPAYABLERELATEDPARTIESCURRENT",

    "NOTES PAYABLE AND CURRENT PORTION OF LONG TERM DEBT":
        "LONGTERMDEBTCURRENT",

    "CURRENT LIABILITIES ACCOUNTS PAYABLE TRADE":
        "ACCOUNTSPAYABLETRADECURRENT",

    "CURRENT LIABILITIES TRADE ACCOUNTS PAYABLE":
        "ACCOUNTSPAYABLETRADECURRENT",

    "ACCOUNTS PAYABLE AND ACCRUALS":
        "ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT",

    "ACCOUNTS PAYABLE TO AFFILIATES": "ACCOUNTSPAYABLERELATEDPARTIESCURRENT",

    "CURRENT LIABILITIES ACCOUNTS AND NOTES PAYABLE": "ACCOUNTSPAYABLECURRENT",

    "PAYABLES AND ACCRUED LIABILITIES":
        "ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT",

    "CURRENT LIABILITIES LOANS PAYABLE": "LOANSPAYABLECURRENT",

    "CURRENT LIABILITIES DEBT DUE WITHIN ONE YEAR": "DEBTCURRENT",

    "CURRENT LIABILITIES NOTES PAYABLE BANKS": "NOTESPAYABLETOBANKCURRENT",

    "SHORT TERM NOTES": "NOTESPAYABLECURRENT",

    "CURRENT LIABILITIES NOTES AND LOANS PAYABLE":
        "NOTESANDLOANSPAYABLECURRENT",

    "CURRENT LIABILITIES CURRENT PORTION OF LONG TERM OBLIGATIONS":
        "LONGTERMDEBTCURRENT",

    "SHORT TERM NOTES PAYABLE": "NOTESPAYABLECURRENT",

    "CURRENT PORTION OF LONG TERM DEBT AND CAPITAL LEASE OBLIGATIONS":
        "LONGTERMDEBTANDCAPITALLEASEOBLIGATIONSCURRENT",

    "SHORT TERM BORROWINGS AND CURRENT PORTION OF LONG TERM DEBT":
        "DEBTCURRENT",

    "ACCRUED LIABILITIES AND OTHER": "ACCRUEDLIABILITIESCURRENT",

    "ACCOUNTS PAYABLE TRADE CREDITORS": "ACCOUNTSPAYABLETRADECURRENT",

    "CURRENT MATURITIES OF LONG TERM DEBT AND CAPITAL LEASE OBLIGATIONS":
        "LONGTERMDEBTANDCAPITALLEASEOBLIGATIONSCURRENT",

    "AND ACCRUED LIABILITIES": "ACCRUEDLIABILITIESCURRENT",

    "CURRENT LIABILITIES BANK LOANS": "SHORTTERMBANKLOANSANDNOTESPAYABLE",

    "ACCOUNTS PAYABLE PARENT AND AFFILIATES": "ACCOUNTSPAYABLECURRENT",

    "ACCOUNTS PAYABLE AND OTHER":
        "ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT",

    "CURRENT LIABILITIESACCOUNTS PAYABLE": "ACCOUNTSPAYABLECURRENT",

    "ACCOUNTS PAYABLE TO AFFILIATED COMPANIES":
        "ACCOUNTSPAYABLERELATEDPARTIESCURRENT",

    "ACCOUNTS PAYABLE FOR GRAIN": "OTHERLIABILITIESCURRENT",

    "ACCRUED LIABILITIES AND OTHER PAYABLES":
        "ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT",

    "ACCRUED LIABILITIES AFFILIATE": "OTHERLIABILITIESCURRENT",

    "CURRENT MATURITIES OF LONG TERM DEBT AND OBLIGATIONS UNDER CAPITAL LEASE":
        "LONGTERMDEBTANDCAPITALLEASEOBLIGATIONSCURRENT",

    "CURRENT LIABILITIES CURRENT PORTION OF LONG DEBT": "LONGTERMDEBTCURRENT",

    "CURRENT LIABILITIES COMMERCIAL PAPER": "COMMERCIALPAPER",

    "CURRENT LIABILITIES NOTE PAYABLE": "NOTESPAYABLECURRENT",

    "ACCRUED PAYROLL AND RELATED LIABILITIES":
        "OTHERACCRUEDLIABILITIESCURRENT",

    "CURRENT PORTION OF LONG TERM DEBT AND SHORT TERM BORROWINGS":
        "DEBTCURRENT",

    "ACCRUED LIABILITIES AND INCOME TAXES": "ACCRUEDLIABILITIESCURRENT",

    "CURRENT LIABILITIES NOTES PAYABLE TO BANK": "NOTESPAYABLETOBANKCURRENT",

    "SHORT TERM BANK DEBT": "SHORTTERMBANKLOANSANDNOTESPAYABLE",

    "CURRENT LIABILITIES CURRENT PORTION OF LONG TERM DEBT AND CAPITAL LEASES":
        "LONGTERMDEBTANDCAPITALLEASEOBLIGATIONSCURRENT",

    "CURRENT LIABILITIES NOTES PAYABLE AND CURRENT PORTION OF LONG TERM DEBT":
        "DEBTCURRENT",

    "CURRENT LIABILITIES DEBT MATURING WITHIN ONE YEAR": "DEBTCURRENT",

    "CURRENT LIABILITIES NOTES AND ACCEPTANCES PAYABLE": "NOTESPAYABLECURRENT",

    "CURRENT LIABILITIES TRADE PAYABLES": "ACCOUNTSPAYABLETRADECURRENT",

    "ADDITION TO SHORT TERM BORROWINGS": "OTHERSHORTTERMBORROWINGS",

    "OTHER SHORT TERM DEBT": "OTHERSHORTTERMBORROWINGS",

    "CURRENT LIABILITIES NOTES PAYABLE BANK": "NOTESPAYABLETOBANKCURRENT",

    "CURRENT PORTION OF NOTES PAYABLE": "NOTESPAYABLECURRENT",

    "CURRENT PORTION OF DEBT": "DEBTCURRENT",

    "LIABILITIES SHORT TERM DEBT": "SHORTTERMBORROWINGS",

    "ACCRUED EXPENSES AND OTHER LIABILITIES": "OTHERLIABILITIESCURRENT",

    "CURRENT LIABILITIES CURRENT MATURITIES OF LONG TERM DEBT":
        "LONGTERMDEBTCURRENT",

    "CURRENT LIABILITIES CURRENT INSTALLMENTS OF LONG TERM DEBT":
        "LONGTERMDEBTCURRENT",

    "ACCOUNTS PAYABLE AND OTHER CURRENT LIABILITIES":
        "ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT",

    "ACCOUNTS PAYABLE ACCRUED EXPENSES AND OTHER LIABILITIES":
        "ACCOUNTSPAYABLEANDACCRUEDLIABILITIESCURRENT",

    "TOTAL SHORT TERM BORROWINGS": "SHORTTERMBORROWINGS",

    "SHORT TERM DEBT AND CURRENT PORTION OF LONG TERM DEBT": "DEBTCURRENT",

    'OTHER LONG TERM DEBT': "OTHERLONGTERMDEBTNONCURRENT",

    'LONG TERM DEBT DUE WITHIN ONE YEAR': "LONGTERMDEBTCURRENT",

    'OBLIGATIONS UNDER CAPITAL LEASES':
        "CAPITALLEASEOBLIGATIONSNONCURRENT",

    'LONG TERM BORROWINGS': "LONGTERMLOANSPAYABLE",

    'CAPITAL LEASE OBLIGATIONS': "CAPITALLEASEOBLIGATIONSNONCURRENT",

    'PAYMENTS ON LONG TERM DEBT': "LONGTERMDEBTCURRENT",

    'LONG TERM DEBT NET OF CURRENT MATURITIES': "LONGTERMDEBTNONCURRENT",

    'OTHER NONCURRENT LIABILITIES OBLIGATIONS UNDER CAPITAL LEASES':
        "CAPITALLEASEOBLIGATIONSNONCURRENT",

    'TOTAL LONG TERM DEBT': "LONGTERMDEBTNONCURRENT",

    'PRINCIPAL PAYMENTS ON LONG TERM DEBT': "LONGTERMDEBTCURRENT",

    'NOTES PAYABLE AND CURRENT MATURITIES OF LONG TERM DEBT':
        "LONGTERMDEBTCURRENT",

    'LONG TERM LIABILITIES LONG TERM DEBT': "LIABILITIESNONCURRENT",

    'PAYMENTS OF LONG TERM DEBT': "LONGTERMDEBTCURRENT",

    'LONG TERM DEBT EXCLUDING CURRENT INSTALLMENTS': "LONGTERMDEBTNONCURRENT",

    'OTHER ACCOUNTS PAYABLE': "ACCOUNTSPAYABLEOTHERCURRENT",

    'LONG TERM DEBT NET': "LONGTERMDEBTNONCURRENT",

    'NONCURRENT LIABILITIES LONG TERM DEBT': "LONGTERMDEBTNONCURRENT",

    'OTHER NONCURRENT LIABILITIES NUCLEAR FUEL LEASE OBLIGATIONS':
        'LIABILITIESOTHERTHANLONGTERMDEBTNONCURRENT',

    'CURRENT PORTION OF LEASE OBLIGATIONS': "CAPITALLEASEOBLIGATIONSCURRENT",

    'CAPITALIZED LEASE OBLIGATIONS': "CAPITALLEASEOBLIGATIONSNONCURRENT",

    'LONG TERM DEBT DUE AFTER ONE YEAR': "LONGTERMDEBTNONCURRENT",

    'SENIOR LONG TERM DEBT': "SENIORLONGTERMNOTES",

    'LONG TERM DEBT AND CAPITAL LEASE OBLIGATIONS':
        "LONGTERMDEBTANDCAPITALLEASEOBLIGATIONS",

    'CURRENT PORTION OF OBLIGATIONS UNDER CAPITAL LEASES':
        "CAPITALLEASEOBLIGATIONSCURRENT",

    'LONG TERM DEBT EXCLUDING CURRENT PORTION': "LONGTERMDEBTNONCURRENT",

    'LONG TERM DEBT CURRENT PORTION': "LONGTERMDEBTCURRENT",

    'OTHER LIABILITIES LONG TERM DEBT': "OTHERLONGTERMDEBTNONCURRENT",

    'LONG TERM NOTES PAYABLE': "LONGTERMNOTESPAYABLE",

    'CURRENT PORTION OF CAPITAL LEASE OBLIGATIONS':
        "CAPITALLEASEOBLIGATIONSCURRENT",

    'PAYMENT OF CAPITAL LEASE OBLIGATIONS': "CAPITALLEASEOBLIGATIONSCURRENT",

    'LONG TERM DEBT EXCLUDING CURRENT MATURITIES': "LONGTERMDEBTNONCURRENT",

    'CURRENT OBLIGATIONS UNDER CAPITAL LEASES':
        "CAPITALLEASEOBLIGATIONSCURRENT",

    'TERM LOANS AND SHORT TERM DEBT': "SHORTTERMBORROWINGS",

    'ACCOUNTS PAYABLE TO ASSOCIATED COMPANIES':
        "ACCOUNTSPAYABLERELATEDPARTIESCURRENT",

    'PRINCIPAL PAYMENTS OF LONG TERM DEBT': "LONGTERMDEBTCURRENT",

    'SHORT TERM BORROWINGS COMMERCIAL PAPER': "COMMERCIALPAPER",

    'SHORT TERM DEBT AND CURRENT MATURITIES OF LONG TERM DEBT': "DEBTCURRENT",

    'COMMERCIAL PAPER AND OTHER SHORT TERM BORROWINGS': "SHORTTERMBORROWINGS",

    'NOTE PAYABLE AND CURRENT MATURITIES OF LONG TERM DEBT OBLIGATIONS':
        "SHORTTERMBORROWINGS",

    'PAYMENTS ON LONG TERM BORROWINGS': "LONGTERMDEBTCURRENT",

    'LONG TERM DEBT DEBENTURES': "OTHERLONGTERMDEBTNONCURRENT",

    'CONSTRUCTION AND OTHER SHORT TERM LOANS': "OTHERLOANSPAYABLECURRENT",

    'SHORT TERM BORROWINGS AND FHLB ADVANCES': "OTHERSHORTTERMBORROWINGS",

    'SHORT TERM DEBT FINANCINGS NET': "SHORTTERMBORROWINGS",

    'LONG TERM DEBT NET OF AMOUNT DUE WITHIN ONE YEAR':
        "LONGTERMDEBTNONCURRENT",

    'LIABILITIES ACCOUNTS PAYABLE TO AFFILIATES':
        "ACCOUNTSPAYABLERELATEDPARTIESCURRENT",

    'LONG TERM OBLIGATIONS UNDER CAPITAL LEASES':
        "CAPITALLEASEOBLIGATIONSNONCURRENT",

    'LONG TERM DEBT AND OBLIGATIONS UNDER CAPITAL LEASES':
        "LONGTERMDEBTANDCAPITALLEASEOBLIGATIONS",

    'SHORT TERM DEBT INCLUDING CURRENT PORTION OF LONG TERM DEBT':
        "DEBTCURRENT",

    'LONG TERM DEBT NOTES PAYABLE': "LONGTERMNOTESPAYABLE",

    'ACCRUED LIABILITIES OTHER': "OTHERACCRUEDLIABILITIESCURRENT",

    'ACCRUED LIABILITIES AND EXPENSES': "ACCRUEDLIABILITIESCURRENT",

    'SHORT TERM LOANS': "LOANSPAYABLECURRENT",

    'CURRENT DEBT MATURITIES': "DEBTCURRENT",

    'ACCRUALS AND OTHER CURRENT LIABILITIES': "ACCRUEDLIABILITIESCURRENT",

    'LONG TERM LIABILITIES LESS CURRENT MATURITIES': "LIABILITIESNONCURRENT",

    'NOTES PAYABLE CAPITALIZED LEASES AND OTHER LONG TERM DEBT':
        "LONGTERMDEBTANDCAPITALLEASEOBLIGATIONS",

    'CAPITAL LEASE OBLIGATIONS LESS CURRENT PORTION':
        "CAPITALLEASEOBLIGATIONSNONCURRENT",

    'LONG TERM DEBT AND CAPITALIZED LEASE OBLIGATIONS':
        "LONGTERMDEBTANDCAPITALLEASEOBLIGATIONS",

    'SHORT TERM BANK BORROWINGS': "SHORTTERMBANKLOANSANDNOTESPAYABLE",

    'LONG TERM DEBT AND AND OTHER BORROWINGS': "LONGTERMDEBTNONCURRENT",

    'LONG TERM DEBT AND CAPITAL LEASES':
        "LONGTERMDEBTANDCAPITALLEASEOBLIGATIONS",

    'CURRENT LIABILITIES LONG TERM DEBT DUE WITHIN TWELVE MONTHS':
        "LONGTERMDEBTCURRENT",

    'SUBORDINATED LONG TERM DEBT': "SUBORDINATEDLONGTERMDEBT",

    'LOANS PAYABLE SHORT TERM COMMERCIAL PAPER': "COMMERCIALPAPER",

    'CURRENT LIABILITIES LONG TERM DEBT DUE WITHIN TWELVE MONTHS':
        "LONGTERMDEBTCURRENT",

    'PRINCIPAL PAYMENTS ON CAPITAL LEASE OBLIGATIONS':
        "CAPITALLEASEOBLIGATIONSCURRENT",

    'CURRENT MATURITIES OF CAPITALIZED LEASE OBLIGATIONS':
        'CAPITALLEASEOBLIGATIONSCURRENT',

    'PRINCIPAL PAYMENTS ON LONG TERM DEBT AND CAPITAL LEASE OBLIGATIONS':
        'LONGTERMDEBTANDCAPITALLEASEOBLIGATIONSCURRENT' 

}


RAW_PHRASES = list(RAW_TO_GAAP.keys())

# compute trigram sets for phrases
RAW_PHRASE_GRAMS = [set(nltk.ngrams(w, n=3)) for w in RAW_PHRASES]
