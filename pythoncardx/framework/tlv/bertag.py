"""
Credits have to be given there:
http://code.activestate.com/recipes/577244-simple-ber-decoding-in-python/
"""

from pythoncard.utils import NotAlwaysStatic

def sanitycheck(array):
    mask = (1 << 8) - 1
    for i in range(len(array)):
        if array[i] > ((1 << (8)-1) - 1):
            array[i] =  -(~(array[i]-1) & mask)

from pythoncardx.framework.tlv import TLVException

class BERTag(object):
    BER_TAG_CLASS_MASK_APPLICATION = 0
    BER_TAG_CLASS_MASK_CONTEXT_SPECIFIC = 1
    BER_TAG_CLASS_MASK_PRIVATE = 2
    BER_TAG_CLASS_MASK_UNIVERSAL = 3
    BER_TAG_TYPE_CONSTRUCTED = 4
    BER_TAG_TYPE_PRIMITIVE = 5

    def __init__(self):
        self._tagClass = 0
        self._tagNumber = 0
        self._size = 0

    @staticmethod
    def getInstance(bArray, bOff):
        if (bArray[bOff] >> 5) & 0x1:
            tag = ConstructedBERTag()
        else:
            tag = PrimitiveBERTag()
        tag.init(bArray, bOff)
        return tag

    def init(self, bArray, bOff):
        """ supposedly abstract """
        self._tagClass = (bArray[bOff] & 0xff) >> 6
        self._tagConstr = bool(bArray[bOff] & 0x20)
        if (bArray[bOff] & 0x1f) == 0x1f:
            self._tagNumber = 0
            bLen = 1
            while (bArray[bOff+bLen] & 0x80) == 0x80:
                self._tagNumber = self._tagNumber << 7
                self._tagNumber += bArray[bOff+bLen] & 0x7f
                bLen += 1
            self._tagNumber = self._tagNumber << 7
            self._tagNumber += bArray[bOff+bLen] & 0x7f
            self._size = bLen
        else:
            self._tagNumber = bArray[bOff] & 0x1f
            self._size = 1

    def _toBytesBound(self, outBuf, bOffset):
        outBuf[bOffset] = self._tagClass << 6
        outBuf[bOffset] += (self._tagConstr and 1 or 0) << 5
        if self._tagNumber <= 30:
            outBuf[bOffset] += self._tagNumber
            sanitycheck(outBuf)
            return 1
        else:
            tagNumber = self._tagNumber
            outBuf[bOffset] += 0x1f
            chunks = []
            while tagNumber > 0:
                chunks.append(tagNumber & 0x7f)
                tagNumber = tagNumber >> 7
            bLen = 1
            for i in reversed(chunks):
                outBuf[bOffset+bLen] = 0x80
                outBuf[bOffset+bLen] += i
                bLen += 1
            #clear the high bit on the last part
            outBuf[bOffset+bLen-1] &= 0x7f
            sanitycheck(outBuf)
            return bLen
    @staticmethod
    def _toBytesStatic(tagClass, isConstructed, tagNumber, outArray, bOff):
        tag = {True: ConstructedBERTag,
               False: PrimitiveBERTag}[isConstructed]()
        tag.init(tagClass, tagNumber)
        return tag.toBytes(outArray, bOff)
    toBytes = NotAlwaysStatic('_toBytesBound', '_toBytesStatic')

    def _sizeBound(self):
        return self._size
    @staticmethod
    def _sizeStatic(berTagArray, bOff):
        tag = BERTag()
        tag.init(berTagArray, bOff)
        return tag.size()
    size = NotAlwaysStatic('_sizeBound', '_sizeStatic')

    def _isConstructedBound(self):
        return self._tagConstr
    @staticmethod
    def _isConstructedStatic(berTagArray, bOff):
        tag = BERTag.getInstance(berTagArray, bOff)
        return tag.isConstructed()
    isConstructed = NotAlwaysStatic('_isConstructedBound', '_isConstructedStatic')

    def _tagClassBound(self):
        return self._tagClass
    @staticmethod
    def _tagClassStatic(berTagArray, bOff):
        tag = BERTag.getInstance(berTagArray, bOff)
        return tag.tagClass()
    tagClass = NotAlwaysStatic('_tagClassBound', '_tagClassStatic')

    def _tagNumberBound(self):
        return self._tagNumber
    @staticmethod
    def _tagNumberStatic(berTagArray, bOff):
        tag = BERTag.getInstance(berTagArray, bOff)
        return tag.tagNumber()
    tagNumber = NotAlwaysStatic('_tagNumberBound', '_tagNumberStatic')

    def __str__(self):
        return '<BERTag: %d%s, %d>' % (self._tagClass, self._tagConstr and ', CONSTR' or '', self._tagNumber)

    def __eq__(self, other):
        return ((self._tagClass == other._tagClass) and
                (self._tagConstr == other._tagConstr) and
                (self._tagNumber == other._tagNumber))

class PrimitiveBERTag(BERTag):
    def __init__(self):
        BERTag.__init__(self)
        self._tagConstr = False # primitive

    def init(self, param1, param2):
        self._tagClass = None
        self._tagNumber = None
        if isinstance(param1, list):
            if (param1[param2] & 0x20) == 0x20:
                # constructed tag
                raise TLVException(TLVException.MALFORMED_TAG)
            BERTag.init(self, param1, param2)
        else:
            tagClass = param1
            tagNumber = param2
            self._tagClass = tagClass
            self._tagNumber = tagNumber

class ConstructedBERTag(BERTag):
    def __init__(self):
        BERTag.__init__(self)
        self._tagConstr = True # constructed

    def init(self, param1, param2):
        self._tagClass = None
        self._tagNumber = None
        if isinstance(param1, list):
            if (param1[param2] & 0x20) == 0:
                # primitive tag
                raise TLVException(TLVException.MALFORMED_TAG)
            BERTag.init(self, param1, param2)
        else:
            self._tagClass = param1
            self._tagNumber = param2

