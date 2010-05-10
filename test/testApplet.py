import unittest

from pythoncard.framework import Applet, APDU, ISOException, ISO7816

class testApplet(unittest.TestCase):

    def testMiniApplet(self):

        class MiniApplet(Applet):
            def process(self, apdu):
                ISOException.throwIt(ISO7816.SW_NO_ERROR)

        app = MiniApplet()
        
        self.assertTrue(app.select())
        try:
            app.process(APDU([00]))
        except ISOException, isoe:
            self.assertEquals(0x9000,
                              isoe.getReason())
            
