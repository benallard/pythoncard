from pythoncard.security import CryptoException

import hashlib

class MessageDigest(object):
    ALG_MD5 = 2
    ALG_RIPEMD160 = 3
    ALG_SHA = 1
    ALG_SHA_256 = 4
    ALG_SHA_384 = 5
    ALG_SHA_512 = 6
    LENGTH_MD5 = 16
    LENGTH_RIPEMD160 = 20
    LENGTH_SHA = 20
    LENGTH_SHA_256 = 32
    LENGTH_SHA_384 = 48
    LENGTH_SHA_512 = 64


    _algorithm = None

    @staticmethod
    def getInstance(algorithm, externalaccess):
        if algorithm == MessageDigest.ALG_SHA:
            return _SHAMessageDigest()
        raise CryptoException(CryptoException.NO_SUCH_ALGORITHM)

    @staticmethod
    def getInitializedMessageDigestInstance(algorithm, externalaccess):
        raise CryptoException(CryptoException.NO_SUCH_ALGORITHM)

    def getAlgorithm(self):
        return self._algorithm

class _SHAMessageDigest(MessageDigest):
    m = None
    def __init__(self):
        self._algorithm = MessageDigest.ALG_SHA
        self.m = hashlib.sha1()

    def reset(self):
        self.m = hashlib.sha1()

    def update(self, inBuff, inOffset, inLength):
        self.m.update(''.join(inBuff[inOffset:inOffset+inLength]))

    def doFinal(self, inBuff, inOffset, inLength, outBuff, outOffset):
        self.update(inBuff, inOffset, inLength)
        try:
            for i, v in enumerate(self.m.digest()):
                outBuff[outOffset+i] = v
        except IndexError:
            raise ArrayIndexOutOfBoundsException()
        finally:
            self.reset()
        return self.getLength()

    def getLength(self):
        return self.m.digest_size

