import re
from edgarScraper.config.regexUtils import (
    makeFilterRegex, makeHTMLRegex, makeJointRegexNoNumbers
)
from edgarScraper.config.constants import LONG_TERM_GAAP, SHORT_TERM_GAAP


NUMBER = r"(\$.{0,}?)?\s?(?P<value>\(?(-+|blank|\d{1,3}\.\d*|\d{1,3}(,\d{3})*)\s?\)?)"

W_SPACE = r'.{0,5}?'
MODIFIER_SPACE = r'.{0,25}?'
NEG_SPACE = r'.{0,10}?'
FREE_TEXT_SPACE = r'.{0,100}?[\s\S]{0,1}?.{0,100}?'


SHORT_TERM_MODIFIERS = [
    r'Short' + W_SPACE + 'Term',
    r'(?<!(Non))[/s.]?Current',
    r'Within' + W_SPACE + 'Year',
    r'Accrued'
]

LONG_TERM_MODIFIERS = [
    r'Long' + W_SPACE + 'Term',
    r'Non' + W_SPACE + 'Current',
    r'Excluding' + W_SPACE + 'Current',
    r'After' + W_SPACE + 'Year',
    r'less' + W_SPACE + 'current',
    r'net' + W_SPACE + 'current',
]

DEBT_ENTITIES = [
    r'Debt',
    r'Liabilities',
    r'Borrowings',
    r'Loans',
    r'Commercial' + W_SPACE + 'Paper',
    r'Notes',
]

NEGATIONS = [
    r"NET",
    r"LESS",
    r"EXCLUDING",
    r"EXCLUDES"
]

FILTER_WORDS = [
    r'PAGE',
    r'PROCEEDS',
    r'REDUCTION',
    r'AMORTIZATION',
    r'AMORTIZED',
    r'REPAYMENT',
    r'CASH',
    r'CHANGE',
    r'COMMON STOCK',
    r'STOCKHOLDER',
    r'SHAREHOLDER',
    r'STOCK',
    r'ASSET',
    r'EQUITY',
    r'DECREASE',
    r'INCREASE',
    r'INTEREST',
    r'ISSUED',
    r'ISSUANCE',
    r'IX',
    r'ACTIVITY',
    r'PROCEEDS',
    r'RETIREMENT',
    r'SCHEDULE',
    r'TAX LIABILITY',
    r'COST OF ISSUANCE',
    r'SHAREOWNER',
    r'REDEMPTION',
    r'SECURITIES',
    r'RETIRED',
    r'CAPITALIZATION',
]

SHORT_TERM_MISC = [r'(Accounts' + W_SPACE + 'Payable)']
LONG_TERM_MISC = [
    r'(Total' + W_SPACE + 'Liabilities)',
    r'(obligations' + MODIFIER_SPACE + 'lease)',
    r'(lease' + MODIFIER_SPACE + 'obligations)'
]
JOINT_MISC = SHORT_TERM_MISC + LONG_TERM_MISC

SHORT_TERM = makeHTMLRegex(
    modifiers=SHORT_TERM_MODIFIERS,
    instruments=DEBT_ENTITIES,
    numExp=NUMBER,
    additional=SHORT_TERM_MISC,
    spaceToken=MODIFIER_SPACE
)

LONG_TERM = makeHTMLRegex(
    modifiers=LONG_TERM_MODIFIERS,
    instruments=DEBT_ENTITIES,
    numExp=NUMBER,
    additional=LONG_TERM_MISC,
    spaceToken=MODIFIER_SPACE
)

FILTER = makeFilterRegex(
    negations=NEGATIONS,
    filters=FILTER_WORDS,
    spaceToken=NEG_SPACE
)

TAGS_WO_NUMS = makeJointRegexNoNumbers(
    shortTermModifiers=SHORT_TERM_MODIFIERS,
    longTermModifiers=LONG_TERM_MODIFIERS,
    instruments=DEBT_ENTITIES,
    spaceToken=MODIFIER_SPACE,
    additionalMisc=JOINT_MISC
)

FREE_TEXT_SHORT_TERM = makeHTMLRegex(
    modifiers=SHORT_TERM_MODIFIERS,
    instruments=DEBT_ENTITIES,
    numExp=NUMBER,
    additional=SHORT_TERM_MISC,
    spaceToken=FREE_TEXT_SPACE
)

FREE_TEXT_LONG_TERM = makeHTMLRegex(
    modifiers=LONG_TERM_MODIFIERS,
    instruments=DEBT_ENTITIES,
    numExp=NUMBER,
    additional=LONG_TERM_MISC,
    spaceToken=FREE_TEXT_SPACE
)

XBRL_CONTEXT = re.compile(r'(?:(?:xbrli:context)|(?:context))', re.I)
XBRL_DATE = re.compile(
    r'(xbrli:instant)|(xbrli:endDate)|(endDate)|(instant)',
    re.I
)

# GAAP_RE_DICT = {
#     tag: re.compile(r'^us-gaap:{}$'.format(tag), re.IGNORECASE)
#     for tag in SHORT_TERM_GAAP + LONG_TERM_GAAP
# }

GAAP_RE = re.compile(
    "|".join(
        [r'(^us-gaap:'+term+r'$)' for term in SHORT_TERM_GAAP + LONG_TERM_GAAP]
    ),
    re.I
)


NOTES = re.compile(
    r'\(NOTES?\s?\d+(,\s?\d)*(,?\s?and \d+)?\)',
    re.I
)

XBRL_SECTION = re.compile(r"<XBRL[.\s\S]*?\/XBRL>", re.M | re.I)
# XBRL_CONTEXT_SECTION = re.compile(
#     r'<(?:(?:xbrli:context)|(?:context))[.\s\S]*?\/(?:(?:xbrli:context)|(?:context))>',
#     re.M | re.I
# )
HTML_SECTION = re.compile(r"<HTML[.\s\S]*?\/HTML>", re.M | re.I)
TABLE_SECTION = re.compile(r"<TABLE[.\s\S]*?\/TABLE>", re.M | re.I)
TEXT_SECTION = re.compile(r"<TEXT[.\s\S]*?\/TEXT>", re.M | re.I)

BALANCE_SHEET = re.compile(r'BALANCE SHEET', re.I)
LIABILITIES = re.compile(r'LIABILITIES', re.I)
TABLE = re.compile(r'TABLE', re.I)
EMPTY_OR_DOLLAR = re.compile(r'(^\s{0,}?\$\s{0,}?)|(^$)|\s+', re.I)
TEXT_TABLE_COLUMNS = re.compile(r'.{0,}?<s>.{0,}?<c>.{0,}?<c>', re.I)

EDGAR_SUB = re.compile('edgar/')
DEBT_DISCLOSURE = re.compile(r'^us-gaap:DebtDisclosureTextBlock$', re.I)
XBRL_CONTEXT_SECTION = re.compile(r'^(xbrli:context)|(context)$', re.I)

XBRL_COMPOSITE_SOUP = re.compile(
    "|".join(
        [
            r'(^us-gaap:'+term+r'$)' 
            for term in SHORT_TERM_GAAP + LONG_TERM_GAAP
        ] +
        [r'(^us-gaap:DebtDisclosureTextBlock$)'] +
        [r'(?:(?:xbrli:context)|(?:context))']
    ), re.I
)
