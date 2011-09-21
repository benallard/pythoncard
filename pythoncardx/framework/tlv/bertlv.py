"""
Credits have to be given there:
http://code.activestate.com/recipes/577244-simple-ber-decoding-in-python/
"""

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
        if tag._PC:
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

    def getLength(self):
        return self._length

    def size(self):
        return self._size

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
