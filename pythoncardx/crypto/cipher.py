import os

from Crypto.PublicKey import RSA

from pythoncard.security import CryptoException, Key, RSAPrivateKey, RSAPrivateCrtKey, RSAPublicKey

from pythoncard.security.key import _arrayTolong, _longToArray

class Cipher(object):
    
    ALG_DES_CBC_NOPAD = 1
    ALG_DES_CBC_ISO9797_M1 = 2
    ALG_DES_CBC_ISO9797_M2 = 3
    ALG_DES_CBC_PKCS5 = 4
    ALG_DES_ECB_NOPAD = 5
    ALG_DES_ECB_ISO9797_M1 = 6
    ALG_DES_ECB_ISO9797_M2 = 7
    ALG_DES_ECB_PKCS5 = 8
    ALG_RSA_ISO14888 = 9
    ALG_RSA_PKCS1 = 10
    ALG_RSA_ISO9796 = 11
    ALG_RSA_NOPAD = 12
    ALG_AES_BLOCK_128_CBC_NOPAD = 13
    ALG_AES_BLOCK_128_ECB_NOPAD = 14
    ALG_RSA_PKCS1_OAEP = 15
    ALG_KOREAN_SEED_ECB_NOPAD = 16
    ALG_KOREAN_SEED_CBC_NOPAD = 17

    MODE_DECRYPT = 1
    MODE_ENCRYPT = 2

    @staticmethod
    def getInstance(algorithm, shared):
        return Cipher(algorithm)

    def __init__(self, algorithm):
        if algorithm not in [self.ALG_RSA_NOPAD, self.ALG_RSA_PKCS1]:
            raise CryptoException(CryptoException.NO_SUCH_ALGORITHM)
        self.algorithm = algorithm
        self.initialized = False

    def init(self, theKey, theMode, bArray = [], bOff = 0, bLen = 0):
        if not isinstance(theKey, Key):
            raise CryptoException(CryptoException.ILLEGAL_VALUE)
        if not theKey.isInitialized():
            raise CryptoException(CryptoException.UNINITIALIZED_KEY)
        if not theMode in [self.MODE_ENCRYPT, self.MODE_DECRYPT]:
            raise CryptoException(CryptoException.ILLEGAL_VALUE)
        self.mode = theMode

        #initialise the Crypto something with the IV in parameter
        
        if self.algorithm in [self.ALG_RSA_NOPAD, self.ALG_RSA_PKCS1]:
            if not isinstance(theKey, (RSAPublicKey, RSAPrivateKey,  RSAPrivateCrtKey)):
                raise CryptoException(CryptoException.ILLEGAL_VALUE)

            self._theKey = theKey

        self.initialized = True

    def getAlgorithm(self):
        return self.algorithm

    def update(self, inBuff, inOffset, inLength, outBuff, outOffset):
        if not self.initialized:
            raise CryptoException(CryptoException.INVALID_INIT)

    def doFinal(self, inBuff, inOffset, inLength, outBuff, outOffset):
        if not self.initialized:
            raise CryptoException(CryptoException.INVALID_INIT)
        if self.algorithm == self.ALG_RSA_PKCS1:
            if self.mode == self.MODE_ENCRYPT:
                if inLength > self._theKey.getSize() - 11:
                    raise CryptoException(CryptoException.ILLEGAL_VALUE)
                rdm = os.urandom(self._theKey.getSize()-inLength-3)
                data = [0, 2] + [ord(x) for x in rdm] + [0] + inBuff[inOffset:inOffset+inLength]
            else:
                data = inBuff[inOffset:inOffset+inLength]
        elif self.algorithm == self.ALG_RSA_NOPAD:
            if inLength != self._theKey.getSize():
                raise CryptoException(CryptoException.ILLEGAL_VALUE)
            data = inBuff[inOffset:inOffset+inLength]

        assert(len(data) == self._theKey.getSize())

        action = {self.MODE_ENCRYPT: self._theKey._theKey.encrypt,
                  self.MODE_DECRYPT: self._theKey._theKey.decrypt}

        if self.mode == self.MODE_ENCRYPT:
            (res, ) = self._theKey._theKey.encrypt(_arrayTolong(data), None)
        else:
            res = self._theKey._theKey.decrypt(_arrayTolong(data))

        buf = _longToArray(res)

        try:
            for i in range(len(buf)):
                outBuff[outOffset+i] = buf[i]
        except IndexError:
            raise ArrayIndexOutOfBoundException()

        return len(buf)

