from pythoncard.security import CryptoException, RSAPrivateKey, RSAPrivateCrtKey, RSAPublicKey
from pythoncard.security import KeyBuilder

from pythoncard.security.key import _longToArray

try:
    from Crypto.PublicKey import RSA as pyCryptoRSA
except ImportError:
    pyCryptoRSA = None

class KeyPair(object):
    ALG_DSA = 3
    ALG_EC_F2M = 4
    ALG_EC_FP = 5
    ALG_RSA = 1
    ALG_RSA_CRT = 2

    def __init__(self, param1, param2):
        if isinstance(param1, int):
            self._algorithm = param1
            self._keylength = param2
            if self._algorithm == self.ALG_RSA:
                self._publicKey = KeyBuilder.buildKey(KeyBuilder.TYPE_RSA_PUBLIC, self._keylength, None)
                self._privateKey = KeyBuilder.buildKey(KeyBuilder.TYPE_RSA_PRIVATE, self._keylength, None)
            elif self._algorithm == self.ALG_RSA_CRT:
                self._publicKey = KeyBuilder.buildKey(KeyBuilder.TYPE_RSA_PUBLIC, self._keylength, None)
                self._privateKey = KeyBuilder.buildKey(KeyBuilder.TYPE_RSA_CRT_PRIVATE, self._keylength, None)
            else:
                raise CryptoException(CryptoException.NO_SUCH_ALGORITHM)
        else:
            if not isinstance(param1, RSAPublicKey):
                raise CryptoException(CryptoException.ILLEGAL_VALUE)
            if not isinstance(param2, (RSAPrivateKey,  RSAPrivateCrtKey)):
                raise CryptoException(CryptoException.ILLEGAL_VALUE)
            self._publicKey = param1
            self._privateKey = param2

    def _pyCryptogenKeyPair(self):
        if pyCryptoRSA is None:
            raise CryptoException(CryptoException.NO_SUCH_ALGORITHM)
        if self._algorithm not in [self.ALG_RSA, self.ALG_RSA_CRT]:
            raise CryptoException(CryptoException.ILLEGAL_VALUE)
        keypair = pyCryptoRSA.generate(self._keylength)
        # fill in the public key components
        self._publicKey = KeyBuilder.buildKey(KeyBuilder.TYPE_RSA_PUBLIC, self._keylength, False)
        self._publicKey.setTheKey(keypair)
        # private key
        if self._algorithm == self.ALG_RSA:
            self._privateKey = KeyBuilder.buildKey(KeyBuilder.TYPE_RSA_PRIVATE, self._keylength, False)
            self._privateKey.setTheKey(keypair)
        elif self._algorithm == self.ALG_RSA_CRT:
            self._privateKey = KeyBuilder.buildKey(KeyBuilder.TYPE_RSA_CRT_PRIVATE, self._keylength, False)
            self._privateKey.setTheKey(keypair)

    def genKeyPair(self):
        if self._publicKey.isInitialized() or self._privateKey.isInitialized():
            raise CryptoException(CryptoException.ILLEGAL_VALUE)
        self._pyCryptogenKeyPair()
        

    def getPrivate(self):
        return self._privateKey
    
    def getPublic(self):
        return self._publicKey
