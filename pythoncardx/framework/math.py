from python.lang import NullPointerException, ArithmeticException
from pythoncard.framework import Util

from pythoncard.utils import s1

def from_bcd(data):
    """
    >>> from_bcd(0x59)
    59
    """
    data &= 0xff
    return ((data >> 4) * 10) + (data & 0x0f)

def to_bcd(data):
    """
    >>> to_bcd(59)
    0x59
    """
    data = data & 0xff
    a = data // 10
    b = data % 10
    return s1((a << 4) + b)

def from_hex(data):
    """
    >>> from_hex(0x59)
    89
    >>> from_hex(-128)
    128
    >>> from_hex(-1)
    255
    """
    return data & 0xff

def to_hex(data):
    return s1(data & 0xff)

class BigNumber(object):
    """ big numbers are unsigned """
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

    def add(self, bArray, bOff, bLen, arrayFormat):
        other = BigNumber()
        other.init(bArray, bOff, bLen, arrayFormat)
        self._value += other._value

    def compareTo(self, param1, *args):
        if isinstance(param1, BigNumber):
            operand = param1
            if self._value == operand._value:
                return 0
            elif self._value > operand._value:
                return 1
            else:
                return -1
        else:
            bArray = param1
            (bOff, bLen, arrayFormat) = args
            operand = BigNumber()
            operand.init(bArray, bOff, bLen, arrayFormat)
            return self.compareTo(operand)

    def toBytes(self, outBuf, bOff, numBytes, arrayFormat):
        array = []
        if arrayFormat == self.FORMAT_BCD:
            value = self._value
            while value > 0:
                array.append(to_bcd(value % 100))
                value = value // 100
        elif arrayFormat == self.FORMAT_HEX:
            value = self._value
            while value > 0:
                array.append(to_hex(value & 0xff))
                value = value >> 8
        else:
            raise ArithmeticException
        if numBytes < len(array):
            raise ArithmeticException
        array.extend([0 for i in range(numBytes - len(array))])
        array.reverse()
        Util.arrayCopy(array, 0, outBuf, bOff, numBytes)

