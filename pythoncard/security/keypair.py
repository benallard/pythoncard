from pythoncard.security import CryptoException, RSAPrivateKey, RSAPrivateCrtKey, RSAPublicKey

from pythoncard.security.key import _longToArray

from Crypto.PublicKey import RSA

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
            publicKey = param1
            privateKey = param2
            self._publicKey = publicKey
            self._privateKey = privateKey

    def genKeyPair(self):
        if self._publicKey is not None or self._privateKey is not None:
            raise CryptoException(CryptoException.ILLEGAL_VALUE)
        if self._algorithm not in [self.ALG_RSA, self.ALG_RSA_CRT]:
            raise CryptoException(CryptoException.ILLEGAL_VALUE)
        keypair = RSA.generate(self._keylength)
        # fill in the public key components
        self._publicKey = RSAPublicKey()
        self._publicKey.setTheKey(keypair.publickey())
        # private key
        if self._algorithm == self.ALG_RSA:
            self._privateKey = RSAPrivateKey()
            self._privateKey.setTheKey(keypair)
        elif self._algorithm == self.ALG_RSA_CRT:
            self._privateKey = RSAPrivateCrtKey()
            self._privateKey.setTheKey(keypair)

    def getPrivate(self):
        return self._privateKey
    
    def getPublic(self):
        return self._publicKey
