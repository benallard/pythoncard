import unittest

from test.tlvtag import Tag, TLV

from pythoncardx.framework.tlv import BERTag, PrimitiveBERTag, ConstructedBERTag

class BERTagTest(unittest.TestCase):

    def testConstrInit(self):
        tag = ConstructedBERTag()
        tag.init(3, 1)
        self.assertEqual(3, tag.tagClass())
        self.assertEqual(True, tag.isConstructed())
        self.assertEqual(1, tag.tagNumber())

    def testGetInstance(self):
        tag = BERTag.getInstance(Tag(3, True, 5), 0)
        self.assertEqual(3, tag.tagClass())
        self.assertEqual(True, tag.isConstructed())
        self.assertEqual(5, tag.tagNumber())

        tag = BERTag.getInstance(Tag(2, False, 6780087076965536589667), 0)
        self.assertEqual(2, tag.tagClass())
        self.assertEqual(False, tag.isConstructed())
        self.assertEqual(6780087076965536589667, tag.tagNumber())

class StaticTest(unittest.TestCase):

    def testtoBytes(self):
        array = [0 for i in range(10)]
        self.assertEqual(1, BERTag.toBytes(1, False, 5, array, 0))
        self.assertEqual(0x45, array[0])

        self.assertEqual(3, BERTag.toBytes(1, False, 0x3fff, array, 0))
        self.assertEqual(0x5f, array[0])
        self.assertEqual(-1, array[1])
        self.assertEqual(0x7f, array[2])

        self.assertEqual(1, BERTag.toBytes(3, True, 1, array, 3))
        self.assertEqual(-31, array[3])
