from python.lang import ArrayIndexOutOfBoundsException
from pythoncard.framework import Util
from pythoncard.security import CryptoException
from pythoncard.security.key import Key, _longToArray, _arrayTolong

class PublicKey(Key):
    pass

class RSAPublicKey(PublicKey):
    def getExponent(self, buffer, offset):
        raise NotImplementedError
    
    def	getModulus(self, buffer, offset):
        raise NotImplementedError

    def setExponent(self, buffer, offset, length):
        raise NotImplementedError
        
    def setModulus(self, buffer, offset, length):
        raise NotImplementedError

def standardGetter(f):
    def getter(self, *args, **kwargs):
        if not self.isInitialized():
            raise CryptoException(CryptoException.UNINITIALIZED_KEY)
        return f(self, *args, **kwargs)
    return getter

def standardSetter(f):
    """
    Set the initialized status
    also set the internal rep if not already there
    """
    def setter(self, *args, **kwargs):
        f(self, *args, **kwargs)
        if (self.modulus is not None) and (self.exponent is not None):
            if self._theKey is None: #if not aready set, set it
                self._construct();
            self.size = len(self.modulus)
            self._setInitialized()
    return setter

class PyCryptoRSAPublicKey(RSAPublicKey):
    from Crypto.PublicKey import RSA
    def __init__(self):
        RSAPublicKey.__init__(self)
        self.exponent = None
        self.modulus = None
        self._theKey = None

    @standardGetter
    def getExponent(self, buffer, offset):
        Util.arrayCopy(self.exponent, 0, buffer, offset, len(self.exponent))
        return len(self.exponent)
    
    @standardGetter
    def getModulus(self, buffer, offset):
        Util.arrayCopy(self.modulus, 0, buffer, offset, len(self.modulus))
        return len(self.modulus)

    @standardSetter
    def setExponent(self, buffer, offset, length):
        self.exponent = buffer[offset:offset+length]

    @standardSetter
    def setModulus(self, buffer, offset, length):
        self.modulus = buffer[offset:offset+length]

    @standardSetter
    def setTheKey(self, theKey):
        self._theKey = theKey
        self.exponent = _longToArray(theKey.e)
        self.modulus = _longToArray(theKey.n)

    def _construct(self):
        self._theKey = RSA.construct([_arrayTolong(self.modulus),
                                      _arrayTolong(self.exponent)])
