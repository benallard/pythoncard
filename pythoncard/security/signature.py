class Signature(object):
    ALG_DES_MAC4_NOPAD = 1
    ALG_DES_MAC8_NOPAD = 2
    ALG_DES_MAC4_ISO9797_M1 = 3
    ALG_DES_MAC8_ISO9797_M1 = 4
    ALG_DES_MAC4_ISO9797_M2 = 5
    ALG_DES_MAC8_ISO9797_M2 = 6
    ALG_DES_MAC4_PKCS5 = 7
    ALG_DES_MAC8_PKCS5 = 8
    ALG_RSA_SHA_ISO9796 = 9
    ALG_RSA_SHA_PKCS1 = 10
    ALG_RSA_MD5_PKCS1 = 11
    ALG_RSA_RIPEMD160_ISO9796 = 12
    ALG_RSA_RIPEMD160_PKCS1 = 13
    ALG_DSA_SHA	= 14
    ALG_RSA_SHA_RFC2409	= 15
    ALG_RSA_MD5_RFC2409 = 16
    ALG_ECDSA_SHA = 17
    ALG_AES_MAC_128_NOPAD = 18
    ALG_DES_MAC4_ISO9797_1_M2_ALG3 = 19
    ALG_DES_MAC8_ISO9797_1_M2_ALG3 = 20
    ALG_RSA_SHA_PKCS1_PSS = 21
    ALG_RSA_MD5_PKCS1_PSS = 22
    ALG_RSA_RIPEMD160_PKCS1_PSS = 23
    ALG_HMAC_SHA1 = 24
    ALG_HMAC_SHA_256 = 25
    ALG_HMAC_SHA_384 = 26
    ALG_HMAC_SHA_512 = 27
    ALG_HMAC_MD5 = 28
    ALG_HMAC_RIPEMD160 = 29
    ALG_RSA_SHA_ISO9796_MR = 30
    ALG_RSA_RIPEMD160_ISO9796_MR = 31
    ALG_KOREAN_SEED_MAC_NOPAD = 32

    MODE_SIGN = 1
    MODE_VERIFY	= 2

    SIG_CIPHER_DES_MAC4 = 1
    SIG_CIPHER_DES_MAC8 = 2
    SIG_CIPHER_RSA = 3
    SIG_CIPHER_DSA = 4
    SIG_CIPHER_ECDSA = 5
    SIG_CIPHER_AES_MAC128 = 6
    SIG_CIPHER_HMAC = 7
    SIG_CIPHER_KOREAN_SEED_MAC = 8

    @staticmethod
    def getInstance(*args):
        if len(args == 2):
            algorithm, externalaccess = args
        elif len(args) == 3:
            messageDigestAlgorithm, cipherAlgorithm, paddingAlgorithm, externalAccess = args
            raise NotImplementedError(args)
        else:
            raise TypeError(args)
        if algorithm in [Signature.ALG_RSA_SHA_PKCS1]:
            return _RSASHASignature(algorithm)
        raise CryptoException(CryptoException.NO_SUCH_ALGORITHM)

    def getLength(self):
        raise NotImplementedError()

    def init(self, theKey, theMode, bArray = [], bOff = 0, bLen = 0):
        pass

    def sign(self, inBuff, inOffset, inLength, sigBuff, sigOffset):
        pass

    def update(self, inBuff, inOffset, inLength):
        pass

    def verify(self, inBuff, inOffset, inLength, sigBuff, sigOffset, sigLength):
        pass

class _RSASHASignature(Signature):
    pass
