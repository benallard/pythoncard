import unittest

from pythoncard.framework import ISOException, ISO7816
from python.lang import ArrayIndexOutOfBoundsException, IndexOutOfBoundsException

class testExceptions(unittest.TestCase):
    
    def testthrowIt(self):
        try:
            ISOException.throwIt(ISO7816.SW_NO_ERROR)
            self.fail()
        except ISOException, isoe:
            self.assertEquals(0x9000,
                              isoe.getReason())

    def testInheritance(self):
        try:
            raise ArrayIndexOutOfBoundsException()
        except IndexOutOfBoundsException:
            pass
        except:
            self.fail()