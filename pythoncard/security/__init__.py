from pythoncard.framework import CardRuntimeException

class CryptoException(CardRuntimeException):
    ILLEGAL_VALUE = 1
    UNINITIALIZED_KEY = 2
    NO_SUCH_ALGORITHM = 3
    INVALID_INIT = 4
    ILLEGAL_USE = 5

from pythoncard.security import key, keybuilder, privatekey, publickey

Key = key.Key
KeyBuilder = keybuilder.KeyBuilder
PrivateKey = privatekey.PrivateKey
PublicKey = publickey.PublicKey
RSAPrivateCrtKey = privatekey.RSAPrivateCrtKey
RSAPrivateKey = privatekey.RSAPrivateKey
RSAPublicKey = publickey.RSAPublicKey

from pythoncard.security import keypair

KeyPair = keypair.KeyPair

from pythoncard.security import signature, random

Signature = signature.Signature
Random = random.Random

from pythoncard.security import messagedigest

MessageDigest = messagedigest.MessageDigest
