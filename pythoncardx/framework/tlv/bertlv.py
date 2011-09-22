"""
Credits have to be given there:
http://code.activestate.com/recipes/577244-simple-ber-decoding-in-python/
"""

from pythoncard.utils import NotAlwaysStatic

from pythoncard.framework import Util
from pythoncardx.framework.tlv.bertag import BERTag

from copy import copy

def _getLength(bArray):
    """ returns a tuple: (length, value) about the L of the TLV """
    if (bArray[0] & 0x80) == 0x80:
        # extended length
        length = bArray[0] & 0x7f
        value = 0
        for i in reversed(bArray[1:length+1]):
            value = value << 8
            value += i
        return (length, value)
    else:
        return (1, bArray[0])

class BERTLV(object):
    def __init__(self):
        self._tag = None
        self._length = 0
        self._value = None
        self._size = 0

    @staticmethod
    def getInstance(bArray, bOff, bLen):
        tag = BERTag.getInstance(bArray, bOff)
        if tag._tagConstr:
            tlv = ConstructedBERTLV(0)
        else:
            tlv = PrimitiveBERTLV(0)
        bOff += tag.size()
        l, length = _getLength(bArray[bOff:])
        tlv.init(tag, bArray, bOff + l, bLen - tag.size() - l)
        return tlv

    def init(self, bArray, bOff, bLen):
        """ supposedly abstract """
        self = BERTLV.getInstance(bArray, bOff, bLen)
        return self.size()

    def getTag(self):
        return self._tag

    def _getLengthBound(self):
        return self._length
    @staticmethod
    def _getLengthStatic(berTLVArray, bOff):
        tag = BERTag.getInstance(berTLVArray, bOff)
        lenOff = bOff + tag.size()
        (llen, length) = _getLength(berTLVArray[lenOff:])
        return tag.size() + llen + length
    getLength = NotAlwaysStatic('_getLengthBound', '_getLengthStatic')

    def size(self):
        return self._size

    def _toBytesBound(self, outBuf, bOff):
        bLen = self._tag.toBytes(outBuf, bOff)
        if self._length > 127:
            length = self._length
            chunks = []
            while length > 127:
                chunks.append(length & 0xff)
                length = length >> 8
            chunk.reverse()
            lLen =  len(chunk)
            outBuf[bOff+bLen] = 0x80 | lLen
            bLen += 1
            Util.arrayCopy(chunk, 0, outBuf, bOff+bLen, lLen)
            bLen += lLen
        else:
            outBuf[bOff+bLen] = self._length
            bLen += 1
        Util.arrayCopy(self._value, 0, outBuf, bOff+bLen, self._length)
        return bLen + self._length
    toBytes = _toBytesBound

class ConstructedBERTLV(BERTLV):
    def __init__(self, numValueBytes):
        BERTLV.__init__(self)

    def init(self, param1, *args):
        if isinstance(param1, BERTag):
            tag = param1
            (vArray, vOff, vLen) = args
            self._tag = copy(tag)
            self._length = vLen
            self._value = vArray[vOff:vOff+vLen]
            return self.size()
        else:
            bArray = param1
            (bOff, bLen) = args
            return BERTLV.init(self, bArray, bOff, bLen)

    def _appendBound(self, aTLV):
        array = [0 for i in range(aTLV.size())]
        aTLV.toBytes(array, 0)
        self._value.extend(array)
        self._length += aTLV.size()
        return self.size()
    @staticmethod
    def _appendStatic(berTLVInArray, bTLVInOff, berTLVOutArray, bTLVOutOff):
        # that's a funny one, actually, it is a CopyArrayAtomic (or not)
        # but just with the length parameter missing ...
        length = BERTLV.getLength(berTLVInArray, bTLVInOff)
        Util.arrayCopy(berTLVInArray, bTLVInOff, berTLVOutArray, bTLVOutOff, length)
    append = NotAlwaysStatic('_appendBound', '_appendStatic')


class PrimitiveBERTLV(BERTLV):
    def __init__(self, numValueBytes):
        BERTLV.__init__(self)

    def init(self, param1, *args):
        if isinstance(param1, BERTag):
            tag = param1
            (vArray, vOff, vLen) = args
            self._tag = copy(tag)
            self._length = vLen
            self._value = vArray[vOff:vOff+vLen]
            return self.size()
        else:
            bArray = param1
            (bOff, bLen) = args
            return BERTLV.init(self, bArray, bOff, bLen)
