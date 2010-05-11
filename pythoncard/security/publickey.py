from python.lang import ArrayIndexOutOfBoundsException
from pythoncard.security import CryptoException
from pythoncard.security.key import Key

class PublicKey(Key):
    pass

class RSAPublicKey(PublicKey):

    def __init__(self):
        PublicKey.__init__(self)
        self.exponent = None
        self.modulus = None

    def getExponent(self, buffer, offset):
        if self.exponent is None:
            raise CryptoException(CryptoException.UNINITIALIZED_KEY)
        try:
            for i in range(len(self.exponent)):
                buffer[offset+i] = self.exponent[i]
        except IndexError:
            raise ArrayIndexOutOfBoundsException()
        return len(self.exponent)
    
    def getModulus(self, buffer, offset):
        if self.modulus is None:
            raise CryptoException(CryptoException.UNINITIALIZED_KEY)
        try:
            for i in range(len(self.modulus)):
                buffer[offset+i] = self.modulus[i]
        except IndexError:
            raise ArrayIndexOutOfBoundsException()
        return len(self.modulus)

    def setExponent(self, buffer, offset, length):
        self.exponent = []
        for b in buffer[offset:offset+length]:
            self.exponent.append(b)

    def setModulus(self, buffer, offset, length):
        self.modulus = []
        for b in buffer[offset:offset+length]:
            self.modulus.append(b)
