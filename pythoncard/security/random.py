import os

from pythoncard.security import CryptoException

class RandomData(object):
    ALG_PSEUDO_RANDOM =	1
    ALG_SECURE_RANDOM = 2
    
    @staticmethod
    def getInstance(algorithm):
        if algorithm == RandomData.ALG_SECURE_RANDOM:
            return _SecureRandomData()
        raise CryptoException(CryptoException.NO_SUCH_ALGORITHM)

    def generateData(self, buffer, offset, length):
        if length == 0:
            raise CryptoException(CryptoException.ILLEGAL_VALUE)
        
    def setSeed(self, buffer, offset, length):
        pass

class _SecureRandomData(RandomData):
    def generateData(self, buffer, offset, length):
        RandomData.generateData(self, buffer, offset, length)
        try:
            for i in range(length):
                buffer[offset+i] = ord(os.urandom(1))
        except IndexError:
            raise ArrayIndexOutOfBoundException()
