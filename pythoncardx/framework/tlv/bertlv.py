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

def getLengthLen(length):
    """ how much btes are needed to write 'length' """
    if length > 127:
        return (length // 127) + 1
    else:
        return 1

class BERTLV(object):
    def __init__(self):
        self._tag = None
        self._length = 0
        self._value = None

    @staticmethod
    def getInstance(bArray, bOff, bLen = None):
        if bLen is None:
            # This is a trick of mine, the JC framework will anyway always
            # call it will three arguments  
            bLen = BERTLV.getLength(bArray, bOff)
        tag = BERTag.getInstance(bArray, bOff)
        if tag.isConstructed():
            tlv = ConstructedBERTLV(0)
        else:
            tlv = PrimitiveBERTLV(0)
        bOff += tag.size()
        l, length = _getLength(bArray[bOff:])
        # this calls the init method of the child class, not BERTLV
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
        return self._tag.size() + getLengthLen(self._length) + self._length

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
        """ append a piece to the value of the out TLV, making it even more
        constructed """
        intlv = BERTLV.getInstance(berTLVInArray, bTLVInOff)
        outtlv = BERTLV.getInstance(berTLVOutArray, bTLVOutOff)
        outtlv.append(intlv)
        return outtlv.toBytes(berTLVOutArray, bTLVOutOff)
    append = NotAlwaysStatic('_appendBound', '_appendStatic')

    def _find(self, tag, offset=0):
        """ returns the offset of the found tag """
        while offset < self._length:
            tlv = BERTLV.getInstance(self._value, offset)
            if tlv.getTag() == tag:
                return offset
            offset += tlv.size()
        return -1

    def _findBound(self, tag):
        if tag is None:
            # return the first one
            return BERTLV.getInstance(self._value, 0)
        offset = self._find(tag)
        if offset == -1:
            return None
        return BERTLV.getInstance(self._value, offset)
    @staticmethod
    def _findStatic(berTLVArray, bTLVOff, berTagArray, bTagOff):
        tlv = BERTLV.getInstance(berTLVArray, bTLVOff)
        firstOff = bTLVOff + tlv.getTag().size() + getLengthLen(tlv.getLength())
        if berTagArray is None:
            # return the first one
            return firstOff
        return firstOff + tlv._find(BERTag.getInstance(berTagArray, bTagOff))
    find = NotAlwaysStatic('_findBound', '_findStatic')

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

    @staticmethod
    def getValueOffset(berTLVArray, bTLVOff):
        tlv = BERTLV.getInstance(berTLVArray, bTLVOff)
        return bTLVOff + tlv.getTag().size() + getLengthLen(tlv.getLength())
