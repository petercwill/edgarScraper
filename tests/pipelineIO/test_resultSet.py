import unittest
from resultSet import DebtLineItem, ResultSet
from datetime import date


class ResultSetTest(unittest.TestCase):

    testLineItem1 = DebtLineItem(
        'XRBL', 'ShortTermBorrowings', 1, date(2000, 1, 1), 'test'
    )

    testLineItem2 = DebtLineItem(
        'XRBL', 'ShortTermBorrowings', 2, date(2000, 3, 1), 'test'
    )

    testLineItem3 = DebtLineItem(
        'XRBL', 'DebtCurrent', 3, date(2000, 1, 2), 'test'
    )

    testLineItem4 = DebtLineItem(
        'XRBL', 'DebtCurrent', 4, date(2000, 1, 1), 'test'
    )

    testLineItem5 = DebtLineItem(
        'XRBL', 'DebtCurrent', 5, date(2000, 1, 3), 'testtesttest'
    )

    testLineItem6 = DebtLineItem(
        'XRBL', 'LiabilitiesCurrent', 6, date(2000, 2, 1), 'testtest'
    )

    testLineItem7 = DebtLineItem(
        'XRBL', 'LiabilitiesCurrent', 7, date(2000, 1, 1), 'test'
    )

    def test_shortTerm1(self):

        lineItems = [self.testLineItem1, self.testLineItem2]

        rs = ResultSet()
        rs.processLineItems(lineItems)

        self.assertEqual(rs.ShortTermBorrowings, self.testLineItem2)

        rs.formFinalShortTermResult()
        self.assertEqual(rs.finalShortTerm, self.testLineItem2.value)

    def test_shortTerm2(self):

        lineItems = [
            self.testLineItem1,
            self.testLineItem2,
            self.testLineItem3,
            self.testLineItem4,
            self.testLineItem5
        ]

        rs = ResultSet()
        rs.processLineItems(lineItems)

        self.assertEqual(rs.ShortTermBorrowings, self.testLineItem2)
        self.assertEqual(rs.DebtCurrent, self.testLineItem3)

        rs.formFinalShortTermResult()
        self.assertEqual(rs.finalShortTerm, self.testLineItem3.value)



if __name__ == '__main__':
    unittest.main()
