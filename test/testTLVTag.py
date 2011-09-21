import unittest

from pythoncardx.framework.tlv import BERTag, PrimitiveBERTag, ConstructedBERTag

class StaticTest(unittest.TestCase):

    def testtoBytes(self):
        array = [0 for i in xrange(10)]
        self.assertEquals(1, BERTag.toBytes(1, False, 5, array, 0))
        self.assertEquals(0x45, array[0])

        self.assertEquals(3, BERTag.toBytes(1, False, 0x3fff, array, 0))
        self.assertEquals(0x5f, array[0])
        self.assertEquals(0xff, array[1])
        self.assertEquals(0x7f, array[2])

        self.assertEquals(2, BERTag,toBytes())

class BERTagTest(unittest.TestCase):

    def testConstrInit(self):
        tag = ConstructedBERTag()
        tag.init(3, 1)
        self.assertEquals(3, tag._tagClass)
        self.assertEquals(1, tag._PC)
        self.assertEquals(1, tag._tagNumber)
