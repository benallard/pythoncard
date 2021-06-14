import unittest

from pythoncard.framework import ISOException, ISO7816
from python.lang import ArrayIndexOutOfBoundsException, IndexOutOfBoundsException
from python.io import IOException
from python.rmi import RemoteException
from pythoncard.security import CryptoException

class testExceptions(unittest.TestCase):
    
    def testthrowIt(self):
        try:
            ISOException.throwIt(ISO7816.SW_NO_ERROR)
            self.fail()
        except ISOException as isoe:
            self.assertEqual(0x9000,
                              isoe.getReason())

    def testInheritance(self):
        try:
            raise ArrayIndexOutOfBoundsException()
        except IndexOutOfBoundsException:
            pass
        except:
            self.fail()

    def testCryptoException(self):
        try:
            raise CryptoException(CryptoException.UNINITIALIZED_KEY)
        except CryptoException as ce:
            self.assertEqual(CryptoException.UNINITIALIZED_KEY,
                             ce.getReason())

    def testRemote(self):
        try:
            raise RemoteException()
        except IOException:
            pass
        except:
            self.fail()
