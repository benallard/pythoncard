from pythoncard.framework import CardRuntimeException

class CryptoException(CardRuntimeException):
    ILLEGAL_VALUE = 1
    UNINITIALIZED_KEY = 2
    NO_SUCH_ALGORITHM = 3
    INVALID_INIT = 4
    ILLEGAL_USE = 5

from pythoncard.security import keypair, key, publickey

KeyPair = keypair.KeyPair
Key = key.Key
PublicKey = publickey.PublicKey
RSAPublicKey = publickey.RSAPublicKey

