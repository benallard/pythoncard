from pythoncard.framework import CardRuntimeException

class CryptoException(CardRuntimeException):
    ILLEGAL_USE = 0
    ILLEGAL_VALUE = 1
    INVALID_INIT = 2
    NO_SUCH_ALGORITHM = 3
    UNINITIALIZED_KEY = 4

from pythoncard.security import keypair, key, publickey

KeyPair = keypair.KeyPair
Key = key.Key
PublicKey = publickey.PublicKey
RSAPublicKey = publickey.RSAPublicKey

