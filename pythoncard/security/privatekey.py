from pythoncard.framework import Util
from pythoncard.security import CryptoException
from pythoncard.security.key import Key, _longToArray

class PrivateKey(Key):
    pass


class RSAPrivateKey(PrivateKey):
    def __init__(self, size):
        PrivateKey.__init__(self, 5, size)

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
    def setter(self, *args, **kwargs):
        f(self, *args, **kwargs)
        if (self.modulus is not None) and (self.exponent is not None):
            self._setInitialized()
    return setter

class PyCryptoRSAPrivateKey(RSAPrivateKey):
    """ This is the same code as for PublicKey """
    def __init__(self, size):
        RSAPrivateKey.__init__(self, size)
        self.exponent = None
        self.modulus = None

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
        if length != (self.size // 8):
            raise CryptoException(CryptoException.ILLEGAL_VALUE)
        self.modulus = buffer[offset:offset+length]

    @standardSetter
    def setTheKey(self, theKey):
        self._theKey = theKey
        self.exponent = _longToArray(theKey.e)
        self.modulus = _longToArray(theKey.d)

class RSAPrivateCrtKey(PrivateKey):
    def __init__(self, size):
        PrivateKey.__init__(self, 6, size)

    def getDP1(buffer, offset):
        raise NotImplementedError

    def getDQ1(buffer, offset):
        raise NotImplementedError

    def getP(buffer, offset):
        raise NotImplementedError

    def getPQ(buffer, offset):
        raise NotImplementedError

    def getQ(buffer, offset):
        raise NotImplementedError

    def setDP1(buffer, offset, length):
        raise NotImplementedError

    def setDQ1(buffer, offset, length):
        raise NotImplementedError

    def setP(buffer, offset, length):
        raise NotImplementedError

    def setPQ(buffer, offset, length):
        raise NotImplementedError

    def setQ(buffer, offset, length):
        raise NotImplementedError

class PyCryptoRSAPrivateCrtKey(RSAPrivateCrtKey):
    def __init__(self, size):
        RSAPrivateKey.__init__(self, size)

    def setTheKey(self, theKey):
        self._theKey = theKey
        self.p = _longToArray(keypair.p)
        self.q = _longToArray(keypair.q)
        self.pq = _longToArray(keypair.u)
        self.dp1 = _longToArray(keypair.d % (keypair.p - 1))
        self.dq1 = _longToArray(keypair.d % (keypair.q - 1))
        # someone should set size over there ...
        self._setInitialized()
