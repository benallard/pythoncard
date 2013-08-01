import os

from pythoncard.framework import Util

from pythoncard.security import CryptoException, Key, RSAPrivateKey, \
     RSAPrivateCrtKey, RSAPublicKey

from pythoncard.security.secretkey import pyDesDESKey

from pythoncard.security.key import _arrayTolong, _longToArray, \
     _arrayTobinary, _binaryToarray

try:
    from pyDes import pyDes
except ImportError:
    pyDes = None

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
    ALG_AES_BLOCK_192_CBC_NOPAD = 18
    ALG_AES_BLOCK_192_ECB_NOPAD = 19
    ALG_AES_BLOCK_256_CBC_NOPAD = 20
    ALG_AES_BLOCK_256_ECB_NOPAD = 21
    ALG_AES_CBC_ISO9797_M1 = 22
    ALG_AES_CBC_ISO9797_M2 = 23
    ALG_AES_CBC_PKCS5 = 24
    ALG_AES_ECB_ISO9797_M1 = 25
    ALG_AES_ECB_ISO9797_M2 = 26
    ALG_AES_ECB_PKCS5 = 27

    MODE_DECRYPT = 1
    MODE_ENCRYPT = 2

    CIPHER_AES_CBC = 1
    CIPHER_AES_ECB = 2
    CIPHER_DES_CBC = 3
    CIPHER_DES_ECB = 4
    CIPHER_KOREAN_SEED_CBC = 5
    CIPHER_KOREAN_SEED_ECB = 6
    CIPHER_RSA = 7

    PAD_NULL = 0
    PAD_NOPAD = 1
    PAD_ISO9797_M1 = 2
    PAD_ISO9797_M2 = 3
    PAD_ISO9797_1_M1_ALG3 = 4
    PAD_ISO9797_1_M2_ALG3 = 5
    PAD_PKCS5 = 6
    PAD_PKCS1 = 7
    PAD_PKCS1_PSS = 8
    PAD_PKCS1_OAEP = 9
    PAD_ISO9796 = 10
    PAD_ISO9796_MR = 11
    PAD_RFC2409 = 12


    @staticmethod
    def getInstance(*args):
        if len(args) == 2:
             algorithm, externalAccess = args
        elif len(args) == 3:
             # map to old style algorithm name
             cipherAlgorithm, paddingAlgorithm, externalAccess = args
             if cipherAlgorithm == Cipher.CIPHER_RSA:
                  algorithm = dict([(Cipher.PAD_NOPAD, Cipher.ALG_RSA_NOPAD),
                                    (Cipher.PAD_PKCS1, Cipher.ALG_RSA_PKCS1)]). \
                              get(paddingAlgorithm, None)
             elif cipherAlgorithm == Cipher.CIPHER_DES_CBC:
                  algorithm = dict([(Cipher.PAD_NOPAD, Cipher.ALG_DES_CBC_NOPAD),
                                    (Cipher.PAD_PKCS5, Cipher.ALG_DES_CBC_PKCS5)]). \
                              get(paddingAlgorithm, None)
             elif cipherAlgorithm == Cipher.CIPHER_DES_ECB:
                  algorithm = dict([(Cipher.PAD_NOPAD, Cipher.ALG_DES_ECB_NOPAD),
                                    (Cipher.PAD_PKCS5, Cipher.ALG_DES_ECB_PKCS5)]). \
                              get(paddingAlgorithm, None)
        else:
            raise TypeError(args)

        if algorithm in [Cipher.ALG_RSA_NOPAD, Cipher.ALG_RSA_PKCS1]:
             return _PyCryptoRSACipher(algorithm)
        elif algorithm in [Cipher.ALG_DES_ECB_NOPAD, 
                           Cipher.ALG_DES_ECB_PKCS5,
                           Cipher.ALG_DES_CBC_NOPAD, 
                           Cipher.ALG_DES_CBC_PKCS5]:
             return _pyDesDESCipher(algorithm)
        print "algorithm not known: %d" % algorithm
        raise CryptoException(CryptoException.NO_SUCH_ALGORITHM)

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

class _PyCryptoRSACipher(Cipher):

    def __init__(self, algorithm):
        Cipher.__init__(self, algorithm)

    def init(self, theKey, theMode, bArray = [], bOff = 0, bLen = 0):
        Cipher.init(self, theKey, theMode, bArray, bOff, bLen)

        if not isinstance(theKey, (RSAPublicKey, RSAPrivateKey,  RSAPrivateCrtKey)):
            raise CryptoException(CryptoException.ILLEGAL_VALUE)

        self._theKey = theKey
        self.initialized = True

    def EME_PKCS1_v1_5_enc(self, M):
        """ EME-PKCS1-v1_5 Encoding """

        def zeroFreeRandom(n):
            out = []
            while len(out) < n:
                rdm = ord(os.urandom(1))
                if rdm != 0:
                    out.append(rdm)
            return out

        if len(M) > (self._theKey.getSize() // 8) - 11:
            raise CryptoException(CryptoException.ILLEGAL_VALUE)
        PS = zeroFreeRandom((self._theKey.getSize() // 8)-len(M)-3)
        return [0, 2] + PS + [0] + M

    def EME_PKCS1_v1_5_dec(self, buf):
        if buf[:2] != [0, 2]:
            raise CryptoException(CryptoException.ILLEGAL_VALUE)
        return buf[buf.index(0,3)+1:]

    def doFinal(self, inBuff, inOffset, inLength, outBuff, outOffset):
        Cipher.doFinal(self, inBuff, inOffset, inLength, outBuff, outOffset)

        data = [0 for i in xrange(inLength)]
        Util.arrayCopy(inBuff, inOffset, data, 0, inLength)
        if ((self.algorithm == self.ALG_RSA_PKCS1) and
            (self.mode == self.MODE_ENCRYPT)):
            data = self.EME_PKCS1_v1_5_enc(data)

        if len(data) != (self._theKey.getSize() // 8):
            raise CryptoException(CryptoException.ILLEGAL_VALUE)

        if self.mode == self.MODE_ENCRYPT:
            (res, ) = self._theKey._theKey.encrypt(_arrayTolong(data), None)
        else:
            if isinstance(self._theKey, RSAPublicKey):
                # We are actually verifying, which can be done the same way as
                # encrypting ...
                (res, ) = self._theKey._theKey.encrypt(_arrayTolong(data), None)
            else:
                res = self._theKey._theKey.decrypt(_arrayTolong(data))

        buf = _longToArray(res)

        # remove padding
        if ((self.algorithm == self.ALG_RSA_PKCS1) and
            (self.mode == self.MODE_DECRYPT)):
            buf = self.EME_PKCS1_v1_5_dec(buf)

        Util.arrayCopy(buf, 0, outBuff, outOffset, len(buf))

        return len(buf)

class _pyDesDESCipher(Cipher):

    def __init__(self, algorithm):
        if pyDes is None:
            # shouldn't happen as it is included in pythoncard
            raise CryptoException(CryptoException.NO_SUCH_ALGORITHM)
        Cipher.__init__(self, algorithm)
        self.desmode = {Cipher.ALG_DES_ECB_NOPAD: pyDes.ECB,
                        Cipher.ALG_DES_ECB_ISO9797_M1: pyDes.ECB,
                        Cipher.ALG_DES_ECB_ISO9797_M2: pyDes.ECB,
                        Cipher.ALG_DES_ECB_PKCS5: pyDes.ECB,
                        Cipher.ALG_DES_CBC_NOPAD: pyDes.CBC,
                        Cipher.ALG_DES_CBC_ISO9797_M1: pyDes.CBC,
                        Cipher.ALG_DES_CBC_ISO9797_M2: pyDes.CBC,
                        Cipher.ALG_DES_CBC_PKCS5: pyDes.CBC}[algorithm]
        self.padmode = {Cipher.ALG_DES_ECB_NOPAD: pyDes.PAD_NORMAL,
                        Cipher.ALG_DES_ECB_ISO9797_M1: None,
                        Cipher.ALG_DES_ECB_ISO9797_M2: None,
                        Cipher.ALG_DES_ECB_PKCS5: pyDes.PAD_PKCS5,
                        Cipher.ALG_DES_CBC_NOPAD: pyDes.PAD_NORMAL,
                        Cipher.ALG_DES_CBC_ISO9797_M1: None,
                        Cipher.ALG_DES_CBC_ISO9797_M2: None,
                        Cipher.ALG_DES_CBC_PKCS5: pyDes.PAD_PKCS5}[algorithm]

    def init(self, theKey, theMode, bArray = [0,0,0,0,0,0,0,0], bOff = 0, bLen = 8):
        Cipher.init(self, theKey, theMode, bArray, bOff, bLen)

        if not isinstance(theKey, pyDesDESKey):
            raise CryptoException(CryptoException.ILLEGAL_VALUE)

        if bLen != 8:
            raise CryptoException(CryptoException.ILLEGAL_VALUE)

        iv = [0 for i in xrange(8)]
        Util.arrayCopy(bArray, bOff, iv, 0, bLen)

        iv = _arrayTobinary(iv)

        if 64 == theKey.getSize():
            # DES
            self._cipher = pyDes.des(theKey._key, self.desmode, iv,
                                     padmode = self.padmode)
        else:
            #3DES
            self._cipher = pyDes.triple_des(theKey._key, self.desmode, iv,
                                            padmode = self.padmode)

        self.initialized = True

    def  doFinal(self, inBuff, inOffset, inLength, outBuff, outOffset):
        Cipher.doFinal(self, inBuff, inOffset, inLength, outBuff, outOffset)

        data = [0 for i in xrange(inLength)]
        Util.arrayCopy(inBuff, inOffset, data, 0, inLength)
        data = _arrayTobinary(data)

        if self.mode == Cipher.MODE_ENCRYPT:
            result = self._cipher.encrypt(data)
        else:
            result = self._cipher.decrypt(data)

        result = _binaryToarray(result)
        Util.arrayCopy(result, 0, outBuff, outOffset, len(result))

        return len(result)
