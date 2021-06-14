import unittest

from pythoncardx.framework.math import BigNumber

class BigNumTest(unittest.TestCase):

    def testInitBCD(self):
        bn = BigNumber(8)
        bn.init([-128, 0x00], 0, 2, BigNumber.FORMAT_BCD)
        self.assertEqual(8000, bn._value)

    def testInitHEX(self):
        bn = BigNumber(8)
        bn.init([0x10, 0x00], 0, 2, BigNumber.FORMAT_HEX)
        self.assertEqual(4096, bn._value)

    def testtoBytesBCD(self):
        bn = BigNumber(8)
        bn.init([0x12, -128], 0, 2, BigNumber.FORMAT_BCD)
        array = [0 for i in range(3)]
        bn.toBytes(array, 0, 2, BigNumber.FORMAT_BCD)
        self.assertEqual([0x12, -128], array[0:2])

    def testtoBytesHEX(self):
        bn = BigNumber(8)
        bn.init([-127, 0x34], 0, 2, BigNumber.FORMAT_HEX)
        array = [0 for i in range(3)]
        bn.toBytes(array, 0, 2, BigNumber.FORMAT_HEX)
        self.assertEqual([-127, 0x34], array[0:2])
