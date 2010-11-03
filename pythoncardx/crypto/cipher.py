import os

from Crypto.PublicKey import RSA

from pythoncard.security import CryptoException, Key, RSAPrivateKey, RSAPrivateCrtKey, RSAPublicKey

from pythoncard.security.key import _arrayTolong, _longToArray

def zeroFreeRandom(n):
    out = []
    while len(out) < n:
        rdm = ord(os.urandom(1))
        if rdm != 0:
            out.append(rdm)
    return out

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
        if algorithm in [Cipher.ALG_RSA_NOPAD, Cipher.ALG_RSA_PKCS1]:
            return _RSACipher(algorithm)
        raise CryptoException(CryptoException.NO_SUCH_ALGORITHM)


    def init(self, theKey, theMode, bArray = [], bOff = 0, bLen = 0):
        if not isinstance(theKey, Key):
            raise CryptoException(CryptoException.ILLEGAL_VALUE)
        if not theKey.isInitialized():
            raise CryptoException(CryptoException.UNINITIALIZED_KEY)
        if not theMode in [self.MODE_ENCRYPT, self.MODE_DECRYPT]:
            raise CryptoException(CryptoException.ILLEGAL_VALUE)
        self.mode = theMode

        #initialise the Crypto something with the IV in parameter

    def getAlgorithm(self):
        return self.algorithm

    def update(self, inBuff, inOffset, inLength, outBuff, outOffset):
        if not self.initialized:
            raise CryptoException(CryptoException.INVALID_INIT)

    def doFinal(self, inBuff, inOffset, inLength, outBuff, outOffset):
        if not self.initialized:
            raise CryptoException(CryptoException.INVALID_INIT)


class _RSACipher(Cipher):

    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.initialized = False

    def init(self, theKey, theMode, bArray = [], bOff = 0, bLen = 0):
        Cipher.init(self, theKey, theMode, bArray, bOff, bLen)

        if not isinstance(theKey, (RSAPublicKey, RSAPrivateKey,  RSAPrivateCrtKey)):
            raise CryptoException(CryptoException.ILLEGAL_VALUE)

        self._theKey = theKey
        self.initialized = True

    def doFinal(self, inBuff, inOffset, inLength, outBuff, outOffset):
        Cipher.doFinal(self, inBuff, inOffset, inLength, outBuff, outOffset)

        if self.algorithm == self.ALG_RSA_PKCS1:
            if self.mode == self.MODE_ENCRYPT:
                if inLength > self._theKey.getSize() - 11:
                    raise CryptoException(CryptoException.ILLEGAL_VALUE)
                data = [0, 2] + zeroFreeRandom(self._theKey.getSize()-inLength-3) + [0] + inBuff[inOffset:inOffset+inLength]
            else:
                data = inBuff[inOffset:inOffset+inLength]
        elif self.algorithm == self.ALG_RSA_NOPAD:
            if inLength != self._theKey.getSize():
                raise CryptoException(CryptoException.ILLEGAL_VALUE)
            data = inBuff[inOffset:inOffset+inLength]

        assert(len(data) == self._theKey.getSize())

        if self.mode == self.MODE_ENCRYPT:
            (res, ) = self._theKey._theKey.encrypt(_arrayTolong(data), None)
        else:
            res = self._theKey._theKey.decrypt(_arrayTolong(data))

        buf = _longToArray(res)

        # remove padding
        if (self.algorithm == self.ALG_RSA_PKCS1) and (self.mode == self.MODE_DECRYPT):
            if buf[:2] != [0, 2]:
                raise CryptoException(CryptoException.ILLEGAL_VALUE)
            buf = buf[buf.index(0,3)+1:]

        try:
            for i in range(len(buf)):
                outBuff[outOffset+i] = buf[i]
        except IndexError:
            raise ArrayIndexOutOfBoundException()

        return len(buf)
