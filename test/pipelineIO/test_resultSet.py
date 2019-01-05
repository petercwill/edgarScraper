import unittest
from datetime import date
from edgarScraper.pipelineIO.resultSet import DebtLineItem, ResultSet


class ResultSetShortTermTest(unittest.TestCase):

    testLineItem1 = DebtLineItem(
        'XBRL', 'SHORTTERMBORROWINGS', 1, date(2000, 1, 1), 'test'
    )

    testLineItem2 = DebtLineItem(
        'XBRL', 'SHORTTERMBORROWINGS', 2, date(2000, 3, 1), 'test'
    )

    testLineItem3 = DebtLineItem(
        'XBRL', 'DEBTCURRENT', 3, date(2000, 1, 2), 'test'
    )

    testLineItem4 = DebtLineItem(
        'XBRL', 'DEBTCURRENT', 4, date(2000, 1, 1), 'test'
    )

    testLineItem5 = DebtLineItem(
        'XBRL', 'DEBTCURRENT', 5, date(2000, 1, 3), 'testtesttest'
    )

    def test_shortTerm1(self):

        lineItems = [self.testLineItem1, self.testLineItem2]

        rs = ResultSet(lineItems)
        rs.processLineItems()

        self.assertEqual(rs.SHORTTERMBORROWINGS, self.testLineItem2)

        rs.formFinalShortTermResult()
        self.assertEqual(rs.FINALSHORTTERM, self.testLineItem2.value)

    def test_shortTerm2(self):

        lineItems = [
            self.testLineItem1,
            self.testLineItem2,
            self.testLineItem3,
            self.testLineItem4,
            self.testLineItem5
        ]

        rs = ResultSet(lineItems)
        rs.processLineItems()

        self.assertEqual(rs.SHORTTERMBORROWINGS, self.testLineItem2)
        self.assertEqual(rs.DEBTCURRENT, self.testLineItem3)

        rs.formFinalShortTermResult()
        self.assertEqual(rs.FINALSHORTTERM, self.testLineItem2.value)


class ResultSetLongTermTest(unittest.TestCase):

    testLineItem1 = DebtLineItem(
        'XBRL', 'OTHERLOANSPAYABLELONGTERM', 1, date(2000, 1, 1), 'test'
    )

    testLineItem2 = DebtLineItem(
        'XBRL', 'LONGTERMLOANSPAYABLE', 2, date(2000, 3, 1), 'test'
    )

    testLineItem3 = DebtLineItem(
        'XBRL', 'SENIORLONGTERMNOTES', 3, date(2000, 1, 2), 'test'
    )

    testLineItem4 = DebtLineItem(
        'XBRL', 'UNSECUREDLONGTERMDEBT', 4, date(2000, 1, 1), 'test'
    )

    def test_longTerm1(self):

        lineItems = [self.testLineItem1, self.testLineItem2]

        rs = ResultSet(lineItems)
        rs.processLineItems()

        self.assertEqual(
            rs.LONGTERMNOTESANDLOANS.value,
            self.testLineItem2.value
            )

        self.assertEqual(
            rs.LONGTERMDEBTNONCURRENT.value,
            self.testLineItem2.value
        )

        self.assertEqual(rs.FINALLONGTERM, self.testLineItem2.value)

    def test_longTerm2(self):

        lineItems = [
            self.testLineItem2,
            self.testLineItem3,
            self.testLineItem4,
        ]

        rs = ResultSet(lineItems)
        rs.processLineItems()

        self.assertEqual(
            rs.LONGTERMNOTESANDLOANS.value,
            (
                self.testLineItem2.value +
                self.testLineItem3.value
            )
        )

        self.assertEqual(
            rs.LONGTERMDEBTNONCURRENT.value,
            (
                self.testLineItem2.value +
                self.testLineItem3.value +
                self.testLineItem4.value
            )
        )

        self.assertEqual(rs.FINALLONGTERM, rs.LONGTERMDEBTNONCURRENT.value)


if __name__ == "__main__":
    unittest.main()
