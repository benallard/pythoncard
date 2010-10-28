#from Crypto.PublicKey import RSA

from pythoncard.security import CryptoException, Key

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
        self.algorithm = algorithm
        self.initialized = False

    def init(self, theKey, theMode, bArray = [], bOff = 0, bLen = 0):
        if not isinstance(theKey, Key):
            raise CryptoException(CryptoException.ILLEGAL_VALUE)
        if not theKey.isInitialized():
            raise CryptoException(CryptoException.UNINITIALIZED_KEY)
        if not theMode in [self.MODE_ENCRYPT, self.MODE_DECRYPT]:
            raise CryptoException(CryptoException.ILLEGAL_VALUE)
        self.key = theKey
        self.mode = theMode

        #initialise the Crypto something with the IV in parameter
        
        self.initialized = True

    def getAlgorithm(self):
        return self.algorithm

    def update(self, inBuff, inOffset, inLength, outBuff, outOffset):
        if not self.initialized:
            raise CryptoException(CryptoException.INVALID_INIT)

    def doFinal(self, inBuff, inOffset, inLength, outBuff, outOffset):
        if not self.initialized:
            raise CryptoException(CryptoException.INVALID_INIT)
        
    
