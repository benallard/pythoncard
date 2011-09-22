from python.lang import NullPointerException, ArithmeticException
from pythoncard.framework import Util

def from_bcd(data):
    """
    >>> from_bcd(0x59)
    59
    """
    return int(hex(data)[2:])

def to_bcd(data):
    """
    >>> to_bcd(59)
    0x59
    """
    a = data // 10
    b = data % 10
    return (a << 4) + b

def from_hex(data):
    """
    >>> from_hex(0x59)
    786
    """
    return data
to_hex = from_hex

class BigNumber(object):
    FORMAT_BCD = 1
    FORMAT_HEX = 2

    def __init__(self, maxBytes = None):
        if maxBytes is not None and maxBytes <= 0:
            raise ArithmeticException()
        self.maxBytes = maxBytes
        self._value = None

    def init(self, bArray, bOff, bLen, arrayFormat):
        if bLen == 0:
            raise ArithmeticException()
        if bArray is None:
            raise NullPointerException()
        if arrayFormat == self.FORMAT_BCD:
            self._value = 0
            for i in xrange(bLen):
                self._value *= 100
                self._value += from_bcd(bArray[bOff+i])
        elif arrayFormat == self.FORMAT_HEX:
            self._value = 0
            for i in xrange(bLen):
                self._value = self._value << 8
                self._value += from_hex(bArray[bOff+i])
        else:
            raise ArithmeticException

    @staticmethod
    def getMaxBytesSupported():
        # We have to lie there for practical reasons
        return 20

    def multiply(self, bArray, bOff, bLen, arrayFormat):
        other = BigNumber()
        other.init(bArray, bOff, bLen, arrayFormat)
        self._value *= other._value

    def subtract(self, bArray, bOff, bLen, arrayFormat):
        other = BigNumber()
        other.init(bArray, bOff, bLen, arrayFormat)
        self._value -= other._value

    def compareTo(self, operand):
        if self._value == operand._value:
            return 0
        elif self._value > operand._value:
            return 1
        else:
            return -1

    def toBytes(self, outBuf, bOff, numBytes, arrayFormat):
        array = []
        if arrayFormat == self.FORMAT_BCD:
            value = self._value
            while value > 100:
                array.append(to_bcd(value % 100))
                value = value // 100
        elif arrayFormat == self.FORMAT_HEX:
            value = self._value
            while value > 0xff:
                array.append(to_hex(value % 0xff))
                value = value // 0xff
        else:
            raise ArithmeticException
        if numBytes < len(array):
            raise ArithmeticException
        array.extend([0 for i in range(numBytes - len(array))])
        array.reverse()
        Util.arrayCopy(array, 0, outBuf, bOff, numBytes)

