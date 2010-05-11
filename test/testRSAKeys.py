import unittest
from python.lang import ArrayIndexOutOfBoundsException

from pythoncard.security import RSAPublicKey, PublicKey, Key, CryptoException

class testRSAPublicKey(unittest.TestCase):
    
    def testinheritance(self):
        pubk = RSAPublicKey()
        self.assertTrue(isinstance(pubk, RSAPublicKey))
        self.assertTrue(isinstance(pubk, PublicKey))
        self.assertTrue(isinstance(pubk, Key))


    def testGetters(self):
        pubk = RSAPublicKey()
        try:
            pubk.getExponent([], 0)
            self.fail()
        except CryptoException, ce:
            self.assertEquals(CryptoException.UNINITIALIZED_KEY,
                             ce.getReason())
        try:
            pubk.getModulus([], 0)
            self.fail()
        except CryptoException, ce:
            self.assertEquals(CryptoException.UNINITIALIZED_KEY,
                             ce.getReason())
        pubk.setExponent([], 0, 0)
        try:
            pubk.getExponent([], 0)
        except CryptoException:
            self.fail()

    def testValue(self):
        pubk = RSAPublicKey()
        pubk.setExponent([0,1,2,3,4,5,6,7,8,9], 5, 5)
        buf = []
        try:
            self.assertEquals(5, pubk.getExponent([], 7))
            self.fail()
        except ArrayIndexOutOfBoundsException:
            pass
        buf = [0 for i in range(20)]
        self.assertEquals(5, pubk.getExponent(buf, 7))
        self.assertEquals([5,6,7,8,9], buf[7:7+5])
