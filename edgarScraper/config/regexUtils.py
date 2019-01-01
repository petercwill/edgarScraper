import re
from itertools import product


def makeHTMLRegex(modifiers, instruments, numExp, additional, spaceToken):

    products = product(modifiers, instruments)

    phrases = [
        '(' + m + spaceToken + i + ')'
        for (m, i) in products
    ]

    phrases += [
        '(' + i + spaceToken + m + ')'
        for (m, i) in products
    ]

    phrases += additional

    regexString = (r'(?P<name>.*(' + "|".join(phrases) + r').{0,}?\s\s+)')
    finalRe = re.compile(regexString + numExp, re.I)

    return finalRe


def makeFilterRegex(negations, filters, spaceToken):

    products = product(negations, filters)

    filterPhrases = [
        r'((?<!(' + n + r'))' + spaceToken  + i + ')'
        for (n, i) in products
    ]

    filterRegexString = "|".join(filterPhrases)
    finalRe = re.compile(filterRegexString, re.I)

    return finalRe


def makeJointRegexNoNumbers(
    shortTermModifiers,
    longTermModifiers,
    instruments,
    spaceToken,
    additionalMisc
):

    shortTermProducts = product(shortTermModifiers, instruments)
    longTermProducts = product(longTermModifiers, instruments)

    phrases = [
        '(' + m + spaceToken + i + ')'
        for (m, i) in shortTermProducts
    ]

    phrases += [
        '(' + i + spaceToken + m + ')'
        for (m, i) in shortTermProducts
    ]

    phrases = [
        '(' + m + spaceToken + i + ')'
        for (m, i) in longTermProducts
    ]

    phrases += [
        '(' + i + spaceToken + m + ')'
        for (m, i) in longTermProducts
    ]

    phrases += additionalMisc
    jointTermRegexString = r'(' + "|".join(phrases) + r')'
    finalRe = re.compile(jointTermRegexString, re.I)
    return finalRe
