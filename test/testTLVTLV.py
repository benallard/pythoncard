import unittest

from test.tlvtag import Tag, TLV

from pythoncardx.framework.tlv import BERTag, PrimitiveBERTag, ConstructedBERTag, \
                                      BERTLV, PrimitiveBERTLV, ConstructedBERTLV

class BERTLVTest(unittest.TestCase):

    def testConstrInit(self):
        tag = ConstructedBERTag()
        tag.init(3, 1)
        array = [0 for i in range(10)]
        tag.toBytes(array, 0)
        tlv = BERTLV.getInstance(array, 0, 2)
        self.assertEqual(tag, tlv.getTag())

class BERTLVfindTest(unittest.TestCase):

    def testfindOk(self):
        tlv = BERTLV.getInstance(
            TLV(Tag(constr=True, number=8),
                 TLV(Tag(number=7), [0,6,7,56]) +
                 TLV(Tag(cls=2, number=5), [89,4,3,6,1,6,])
                 ),
            0)

        tlv2 = tlv.find(BERTag.getInstance(Tag(number=7), 0))
        self.assertEqual(BERTag.getInstance(Tag(number=7), 0), tlv2.getTag())
        array = [0 for i in range (10)]
        size = tlv2.getValue(array, 0)
        self.assertEqual(4, size)
        self.assertEqual([0, 6, 7, 56], array[0:size])

        tlv2 = tlv.find(BERTag.getInstance(Tag(cls=2, number=5), 0))
        self.assertEqual(BERTag.getInstance(Tag(cls=2, number=5), 0), tlv2.getTag())
        size = tlv2.getValue(array, 0)
        self.assertEqual(6, size)
        self.assertEqual([89, 4, 3, 6, 1, 6], array[0:size])

    def testfindNOK(self):
        tlv = BERTLV.getInstance(
            TLV(Tag(constr=True, number=8),
                 TLV(Tag(number=7), [0,6,7,56]) +
                 TLV(Tag(cls=2, number=5), [89,4,3,6,1,6,])
                 ),
            0)

        self.assertEqual(None, tlv.find(BERTag.getInstance(Tag(number=3), 0)))

    def testfindFirst(self):
        tlv = BERTLV.getInstance(
            TLV(Tag(constr=True, number=8),
                 TLV(Tag(number=7), [0,6,7,56]) +
                 TLV(Tag(cls=2, number=5), [89,4,3,6,1,6,])
                 ),
            0)

        tlv2 = tlv.find(None)
        self.assertEqual(BERTag.getInstance(Tag(number=7), 0), tlv2.getTag())
        array = [0 for i in range (10)]
        size = tlv2.getValue(array, 0)
        self.assertEqual(4, size)
        self.assertEqual([0, 6, 7, 56], array[0:size])

    def testfindFirstNOK(self):
        tlv = BERTLV.getInstance(
            TLV(Tag(constr=True, number=17)),
            0)

        self.assertEqual(None, tlv.find(None))

class BERTLVfindNextTest(unittest.TestCase):

    def testfindNextOK(self):
        tag1 = Tag(number=1)
        tag2 = Tag(cls=2, number=2)
        tlv = BERTLV.getInstance(
            TLV(Tag(constr=True),
                 TLV(tag1, [0,6,7,56]) + # tlv2
                 TLV(tag2, [89,4,3,6,1,6,]) +
                 TLV(tag2, [0,6,7,56]) +
                 TLV(tag1, [89,4,3,3,1,6,7,8]) + # tlv3
                 TLV(tag2, [0,6,7,0, 0, 0, 0]) +
                 TLV(tag1, [0,6,7,56]) + # tlv2 (bis)
                 TLV(tag1, [89,4]) # tlv4
                 ),
            0)

        tlv2 = tlv.find(BERTag.getInstance(tag1, 0))
        tlv3 = tlv.findNext(
            BERTag.getInstance(tag1, 0),
            tlv2,
            1)

        self.assertEqual(BERTag.getInstance(tag1, 0), tlv3.getTag())
        array = [0 for i in range (10)]
        size = tlv3.getValue(array, 0)
        self.assertEqual(8, size)
        self.assertEqual([89,4,3,3,1,6,7,8], array[0:size])

        tlv4 = tlv.findNext(
            BERTag.getInstance(tag1, 0),
            tlv2,
            2)
        self.assertEqual(BERTag.getInstance(tag1, 0), tlv4.getTag())
        size = tlv4.getValue(array, 0)
        self.assertEqual(2, size)
        self.assertEqual([89,4], array[0:size])

    def testfindNextNOK(self):
        tag1 = Tag(number=1)
        tag2 = Tag(cls=2, number=2)
        tlv = BERTLV.getInstance(
            TLV(Tag(constr=True),
                 TLV(tag1, [0,6,7,56]) + # tlv2
                 TLV(tag2, [89,4,3,6,1,6,]) +
                 TLV(tag2, [0,6,7,56]) +
                 TLV(tag1, [89,4,3,3,1,6,7,8]) +
                 TLV(tag2, [0,6,7,0, 0, 0, 0]) +
                 TLV(tag1, [0,6,7,56]) + # tlv2 (bis)
                 TLV(tag1, [89,4])
                 ),
            0)

        tlv2 = tlv.find(BERTag.getInstance(tag1, 0))
        self.assertEqual(None, tlv.findNext(
            BERTag.getInstance(Tag(number=5), 0),
            tlv2,
            1))

class StaticTest(unittest.TestCase):

    def testtoBytes(self):
        pass
