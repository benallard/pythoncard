from python.lang import ArrayIndexOutOfBoundsException
from pythoncard.security import CryptoException
from pythoncard.security.key import Key, _longToArray, _arrayTolong

from Crypto.PublicKey import RSA

class PublicKey(Key):
    pass

def standardGetter(f):
    def getter(self, *args, **kwargs):
        if not self.isInitialized():
            raise CryptoException(CryptoException.UNINITIALIZED_KEY)
        try:
            return f(self, *args, **kwargs)
        except IndexError:
            raise ArrayIndexOutOfBoundsException()
    return getter

def standardSetter(f):
    """
    Set the initialized status + also set the internal rep is not already thre
    """
    def setter(self, *args, **kwargs):
        f(self, *args, **kwargs)
        if (self.modulus is not None) and (self.exponent is not None):
            if self._theKey is None: #if not aready set, set it
                self._theKey = RSA.construct([_arrayTolong(self.modulus),
                                              _arrayTolong(self.exponent)])
            self.size = len(self.modulus)
            self._setInitialized()
    return setter

class RSAPublicKey(PublicKey):

    def __init__(self):
        PublicKey.__init__(self)
        self.exponent = None
        self.modulus = None
        self._theKey = None

    @standardGetter
    def getExponent(self, buffer, offset):
        for i in range(len(self.exponent)):
            buffer[offset+i] = self.exponent[i]
        return len(self.exponent)
    
    @standardGetter
    def getModulus(self, buffer, offset):
        for i in range(len(self.modulus)):
            buffer[offset+i] = self.modulus[i]
        return len(self.modulus)

    @standardSetter
    def setExponent(self, buffer, offset, length):
        self.exponent = []
        for b in buffer[offset:offset+length]:
            self.exponent.append(b)

    @standardSetter
    def setModulus(self, buffer, offset, length):
        self.modulus = []
        for b in buffer[offset:offset+length]:
            self.modulus.append(b)

    @standardSetter
    def setTheKey(self, theKey):
        self._theKey = theKey
        self.exponent = _longToArray(theKey.e)
        self.modulus = _longToArray(theKey.n)
