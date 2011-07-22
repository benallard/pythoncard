from pythoncard.security import publickey, privatekey, secretkey

class KeyBuilder(object):
    LENGTH_AES_128 = 128
    LENGTH_AES_192 = 192
    LENGTH_AES_256 = 256
    LENGTH_DES = 64
    LENGTH_DES3_2KEY = 128
    LENGTH_DES3_3KEY = 192
    LENGTH_DSA_1024 = 1024
    LENGTH_DSA_512 = 512
    LENGTH_DSA_768 = 768
    LENGTH_EC_F2M_113 = 113
    LENGTH_EC_F2M_131 = 131
    LENGTH_EC_F2M_163 = 163
    LENGTH_EC_F2M_193 = 193
    LENGTH_EC_FP_112 = 112
    LENGTH_EC_FP_128 = 128
    LENGTH_EC_FP_160 = 160
    LENGTH_EC_FP_192 = 192
    LENGTH_HMAC_SHA_1_BLOCK_64 = 64
    LENGTH_HMAC_SHA_256_BLOCK_64 = 64
    LENGTH_HMAC_SHA_384_BLOCK_128 = 128
    LENGTH_HMAC_SHA_512_BLOCK_128 = 128
    LENGTH_KOREAN_SEED_128 = 128
    LENGTH_RSA_1024 = 1024
    LENGTH_RSA_1280 = 1280
    LENGTH_RSA_1536 = 1536
    LENGTH_RSA_1984 = 1984
    LENGTH_RSA_2048 = 2048
    LENGTH_RSA_512 = 512
    LENGTH_RSA_736 = 736
    LENGTH_RSA_768 = 768
    LENGTH_RSA_896 = 896
    TYPE_AES = 15
    TYPE_AES_TRANSIENT_DESELECT = 14
    TYPE_AES_TRANSIENT_RESET = 13
    TYPE_DES = 3
    TYPE_DES_TRANSIENT_DESELECT = 2
    TYPE_DES_TRANSIENT_RESET = 1
    TYPE_DSA_PRIVATE = 8
    TYPE_DSA_PUBLIC = 7
    TYPE_EC_F2M_PRIVATE = 10
    TYPE_EC_F2M_PUBLIC = 9
    TYPE_EC_FP_PRIVATE = 12
    TYPE_EC_FP_PUBLIC = 11
    TYPE_HMAC = 21
    TYPE_HMAC_TRANSIENT_DESELECT = 20
    TYPE_HMAC_TRANSIENT_RESET = 19
    TYPE_KOREAN_SEED = 18
    TYPE_KOREAN_SEED_TRANSIENT_DESELECT = 17
    TYPE_KOREAN_SEED_TRANSIENT_RESET = 16
    TYPE_RSA_CRT_PRIVATE = 6
    TYPE_RSA_PRIVATE = 5
    TYPE_RSA_PUBLIC = 4

    @staticmethod
    def buildKey(keyType, keyLength, keyEncryption):
        if keyType == KeyBuilder.TYPE_RSA_PUBLIC:
            return publickey.PyCryptoRSAPublicKey(keyLength)
        elif keyType == KeyBuilder.TYPE_RSA_PRIVATE:
            return privatekey.PyCryptoRSAPrivateKey(keyLength)
        elif keyType == KeyBuilder.TYPE_RSA_CRT_PRIVATE:
            return privatekey.PyCryptoRSAPrivateKey(keyLength)
        elif keyType in [KeyBuilder.TYPE_DES,
                         KeyBuilder.TYPE_DES_TRANSIENT_DESELECT,
                         KeyBuilder.TYPE_DES_TRANSIENT_RESET]:
            return secretkey.pyDesDESKey(keyType, keyLength)
