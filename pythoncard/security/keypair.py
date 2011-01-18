from pythoncard.security import CryptoException, RSAPrivateKey, RSAPrivateCrtKey, RSAPublicKey
from pythoncard.security import publickey, privatekey

from pythoncard.security.key import _longToArray


class KeyPair(object):
    ALG_DSA = 3
    ALG_EC_F2M = 4
    ALG_EC_FP = 5
    ALG_RSA = 1
    ALG_RSA_CRT = 2

    def __init__(self, param1, param2):
        if isinstance(param1, int):
            algorithm = param1
            keylength = param2
            self._algorithm = algorithm
            self._keylength = keylength
            self._publicKey = None
            self._privateKey = None
        else:
            if not isinstance(param1, RSAPublicKey):
                raise CryptoException(CryptoException.ILLEGAL_VALUE)
            if not isinstance(param2, (RSAPrivateKey,  RSAPrivateCrtKey)):
                raise CryptoException(CryptoException.ILLEGAL_VALUE)
            self._publicKey = param1
            self._privateKey = param2

    def _pyCryptogenKeyPair(self):
        from Crypto.PublicKey import RSA
        if self._algorithm not in [self.ALG_RSA, self.ALG_RSA_CRT]:
            raise CryptoException(CryptoException.ILLEGAL_VALUE)
        keypair = RSA.generate(self._keylength)
        # fill in the public key components
        self._publicKey = publickey.PyCryptoRSAPublicKey()
        self._publicKey.setTheKey(keypair.publickey())
        # private key
        if self._algorithm == self.ALG_RSA:
            self._privateKey = privatekey.PyCryptoRSAPrivateKey()
            self._privateKey.setTheKey(keypair)
        elif self._algorithm == self.ALG_RSA_CRT:
            self._privateKey = privatekey.PyCryptoRSAPrivateCrtKey()
            self._privateKey.setTheKey(keypair)

    def genKeyPair(self):
        if self._publicKey is not None or self._privateKey is not None:
            raise CryptoException(CryptoException.ILLEGAL_VALUE)
        self._pyCryptogenKeyPair()
        

    def getPrivate(self):
        return self._privateKey
    
    def getPublic(self):
        return self._publicKey
