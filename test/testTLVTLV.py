import unittest

from pythoncardx.framework.tlv import BERTag, PrimitiveBERTag, ConstructedBERTag, \
                                      BERTLV, PrimitiveBERTLV, ConstructedBERTLV

class BERTLVTest(unittest.TestCase):

    def testConstrInit(self):
        tag = ConstructedBERTag()
        tag.init(3, 1)
        self.assertEquals(3, tag._tagClass)
        self.assertEquals(1, tag._PC)
        self.assertEquals(1, tag._tagNumber)
        array = [0 for i in range(10)]
        tag.toBytes(array, 0)
        tlv = BERTLV.getInstance(array, 0, 2)
        self.assertEquals(tag, tlv.getTag())

class StaticTest(unittest.TestCase):

    def testtoBytes(self):
        pass
