import unittest

class testImport(unittest.TestCase):
    
    def testFramework(self):
        try:
            from pythoncard.framework import Applet
        except ImportError:
            self.fail("Cannot import pythoncard.framework.Applet")

        try:
            from pythoncard.framework import AID
        except ImportError:
            self.fail("Cannot import pythoncard.framework.AID")

        try:
            from pythoncard.framework import APDU
        except ImportError:
            self.fail("Cannot import pythoncard.framework.APDU")

        try:
            from pythoncard.framework import OwnerPIN
        except ImportError:
            self.fail("Cannot import pythoncard.framework.OwnerPIN")

        try:
            from pythoncard.framework import ISO7816
        except ImportError:
            self.fail("Cannot import pythoncard.framework.ISO7816")


    def testCrpto(self):
        try:
            from pythoncard.crypto import Cipher
        except ImportError:
            self.fail("Cannot import pythoncard.crypto.Cipher")

    def security(self):
        try:
            from pythoncard.security import KeyPair
        except ImportError:
            self.fail("Cannot import pythoncard.security.KeyPair")
