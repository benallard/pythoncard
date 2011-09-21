"""
Credits have to be given there:
http://code.activestate.com/recipes/577244-simple-ber-decoding-in-python/
"""

from pythoncardx.framework.tlv import TLVException

class NotAlwaysStatic(object):
    """ This makes a function both static and not static
    credits goes there (in decreasing order of importance).
    http://users.rcn.com/python/download/Descriptor.htm
    and there:
    http://stackoverflow.com/questions/114214/class-method-differences-in-python-bound-unbound-and-static/114289#114289
    and here:
    http://code.activestate.com/recipes/52304-static-methods-aka-class-methods-in-python/
    """
    def __init__(self, boundname, staticname):
        self.boundname = boundname
        self.staticname = staticname

    def __get__(self, obj, objtype=None):
        if obj is not None:
            return getattr(obj, self.boundname)
        else:
            return getattr(objtype, self.staticname)

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
        self._tagClass = bArray[bOff] >> 6
        self._PC = (bArray[bOff] >> 5) & 0x1
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
        outBuf[bOffset] += self._PC << 5
        if self._tagNumber <= 30:
            outBuf[bOffset] += self._tagNumber
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


class PrimitiveBERTag(BERTag):
    def __init__(self):
        BERTag.__init__(self)
        self._PC = 0 # primitive

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
        self._PC = 1 # constructed

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
    
