from python.lang import NullPointerException, ArithmeticException

def from_bcd(data):
    """
    >>> from_bcd(0x59)
    59
    """
    return int(hex(data)[2:])

def from_hex(data):
    """
    >>> from_hex(0x59)
    786
    """
    return data

class BigNumber(object):
    FORMAT_BCD = 1
    FORMAT_HEX = 2

    def __init__(self, maxBytes):
        if maxBytes <= 0:
            raise ArithmeticException()
        self.maxBytes = maxBytes
        self._value = None

    def init(self, bArray, bOff, bLen, arrayFormat):
        if bLen == 0:
            raise ArithmeticException()
        if arrayFormat not in (self.FORMAT_BCD, self.FORMAT_HEX):
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
                self._value += bArray[bOff+i]

    @staticmethod
    def getMaxBytesSupported():
        # We have to lie there for practical reasons
        return 20

    def multiply(self, bArray, bOff, bLen, arrayFormat):
        other = BigNumber(70)
        other.init(bArray, bOff, bLen, arrayFormat)
        self._value *= other._value

    def compareTo(self, operand):
        if self._value == operand._value:
            return 0
        elif self._value > operand._value:
            return 1
        else:
            return -1
