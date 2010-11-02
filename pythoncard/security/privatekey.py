from pythoncard.security import CryptoException
from pythoncard.security.key import Key, _longToArray

class PrivateKey(Key):
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
    def setter(self, *args, **kwargs):
        f(self, *args, **kwargs)
        if (self.modulus is not None) and (self.exponent is not None):
            self.size = len(self.modulus)
            self._setInitialized()
    return setter

class RSAPrivateKey(PrivateKey):
    """ This is the same code as for PublicKey """
    def __init__(self):
        PrivateKey.__init__(self)
        self.exponent = None
        self.modulus = None

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
        self.modulus = _longToArray(theKey.d)

class RSAPrivateCrtKey(PrivateKey):
    def setTheKey(self, theKey):
        self._theKey = theKey
        self.p = _longToArray(keypair.p)
        self.q = _longToArray(keypair.q)
        self.pq = _longToArray(keypair.u)
        self.dp1 = _longToArray(keypair.d % (keypair.p - 1))
        self.dq1 = _longToArray(keypair.d % (keypair.q - 1))
        # someone should set size over there ...
        self._setInitialized()
