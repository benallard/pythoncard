import unittest
from python.lang import ArrayIndexOutOfBoundsException

from pythoncard.security import RSAPublicKey, PublicKey, Key, CryptoException, KeyBuilder

class testRSAPublicKey(unittest.TestCase):
    
    def testinheritance(self):
        pubk = KeyBuilder.buildKey(KeyBuilder.TYPE_RSA_PUBLIC, KeyBuilder.LENGTH_RSA_1024, False)
        self.assertTrue(isinstance(pubk, RSAPublicKey))
        self.assertTrue(isinstance(pubk, PublicKey))
        self.assertTrue(isinstance(pubk, Key))


    def testGetters(self):
        pubk = KeyBuilder.buildKey(KeyBuilder.TYPE_RSA_PUBLIC, KeyBuilder.LENGTH_RSA_1024, False)
        try:
            pubk.getExponent([], 0)
            self.fail("Got exponent")
        except CryptoException, ce:
            self.assertEquals(CryptoException.UNINITIALIZED_KEY,
                             ce.getReason())
        try:
            pubk.getModulus([], 0)
            self.fail("Got modulus")
        except CryptoException, ce:
            self.assertEquals(CryptoException.UNINITIALIZED_KEY,
                             ce.getReason())
        pubk.setExponent([], 0, 0)
        pubk.setModulus([65]*128, 0, 128)
        try:
            pubk.getExponent([], 0)
        except CryptoException:
            self.fail()

    def testValue(self):
        pubk = KeyBuilder.buildKey(KeyBuilder.TYPE_RSA_PUBLIC, KeyBuilder.LENGTH_RSA_1024, False)
        pubk.setExponent([0,1,2,3,4,5,6,7,8,9], 5, 5)
        pubk.setModulus([65]*128, 0, 128)
        buf = []
        try:
            self.assertEquals(5, pubk.getExponent([], 7))
            self.fail()
        except ArrayIndexOutOfBoundsException:
            pass
        buf = [0 for i in range(20)]
        self.assertEquals(5, pubk.getExponent(buf, 7))
        self.assertEquals([5,6,7,8,9], buf[7:7+5])

    def testInit(self):
        pubk = KeyBuilder.buildKey(KeyBuilder.TYPE_RSA_PUBLIC, KeyBuilder.LENGTH_RSA_1024, False)
        self.assertEquals(False, pubk.isInitialized())
        pubk.setExponent([0,1,2,3,4,5,6,7,8,9], 5, 5)
        self.assertEquals(False, pubk.isInitialized())
        pubk.setModulus([0,0,0,0,0]+[0,1,2,3,4,5,6,7]*16, 5, 128)
        self.assertEquals(True, pubk.isInitialized())

        pubk = KeyBuilder.buildKey(KeyBuilder.TYPE_RSA_PUBLIC, KeyBuilder.LENGTH_RSA_1024, False)
        self.assertEquals(False, pubk.isInitialized())
        pubk.setModulus([0,0,0,0,0]+[0,1,2,3,4,5,6,7]*16, 5, 128)
        self.assertEquals(False, pubk.isInitialized())
        pubk.setExponent([0,1,2,3,4,5,6,7,8,9], 5, 5)
        self.assertEquals(True, pubk.isInitialized())

