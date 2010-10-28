import unittest
from pythoncardx.crypto import Cipher
from pythoncard.security import CryptoException, RSAPublicKey

class testCipher(unittest.TestCase):

    def testInit(self):
        c = Cipher.getInstance(Cipher.ALG_RSA_NOPAD, False)
        self.assertEquals(Cipher.ALG_RSA_NOPAD, c.getAlgorithm())
        try:
            c.update([], 0, 0, [], 0)
            self.fail()
        except CryptoException, ce:
            self.assertEquals(CryptoException.INVALID_INIT, ce.getReason())
        try:
            c.init("abcd", Cipher.MODE_ENCRYPT)
            self.fail()
        except CryptoException, ce:
            self.assertEquals(CryptoException.ILLEGAL_VALUE, ce.getReason())

        pbk = RSAPublicKey()
        try:
            c.init(pbk, Cipher.MODE_ENCRYPT)
            self.fail()
        except CryptoException, ce:
            self.assertEquals(CryptoException.UNINITIALIZED_KEY, ce.getReason())

        pbk.setExponent([0,1,2,3,4,5,6,7,8,9], 5, 5)
        pbk.setModulus([7,8,9], 0, 3)

        c.init(pbk, Cipher.MODE_ENCRYPT)
        
        c.update([], 0, 0, [], 0)
        
