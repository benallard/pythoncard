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
            app.process(APDU([0,0,0,0]))
        except ISOException as isoe:
            self.assertEqual(0x9000,
                              isoe.getReason())
            

    def testBaseProcessApplet(self):

        class BaseProcessApplet(Applet):
            CHOICE_1 = 8
            CHOICE_2 = 56
            CHOICE_3 = 42
            
            def process(self, apdu):

                if self.selectingApplet():
                    return

                if apdu.isISOInterindustryCLA():
                    ISOException.throwIt(ISO7816.SW_CLA_NOT_SUPPORTED)

                buffer = apdu.getBuffer()
                if buffer[ISO7816.OFFSET_INS] == self.CHOICE_1:
                    self.choice1(apdu)
                elif buffer[ISO7816.OFFSET_INS] == self.CHOICE_2:
                    self.choice2(apdu)
                elif buffer[ISO7816.OFFSET_INS] == self.CHOICE_3:
                    return
                else:
                    ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED)

            def choice1(self, apdu):
                apdu.setIncomingAndReceive()
                buf = apdu.getBuffer()
                buf[0] = 55; buf[1] = 77; buf[2] = 99
                apdu.setOutgoingAndSend(0, 3)
            
            def choice2(self, apdu):
                pass

        testvec = [
            ([0, 0x80, 0x00, 0x00],[0x6E, 0x00]), # INS
            ([0x80, 0, 0, 0], [0x6D, 0x00]), # CLA
            ([0, 0xa4, 0, 0,],[0x90, 0x00]), # select
            ([0x80, 8, 0, 0, 0], [55, 77, 99, 0x90, 0x00]) # choice1
        ]

        app = BaseProcessApplet()

        for command, response in testvec:
            apdu = APDU(command)
            if command[1] == ISO7816.INS_SELECT:
                app._selectingApplet = True
            else:
                app._selectingApplet = False
            try:
                app.process(apdu)
                buf = apdu._APDU__buffer[:apdu._outgoinglength]
                buf.extend([0x90, 0x00])
                self.assertEqual(response, buf)
            except ISOException as isoe:
                sw = isoe.getReason()
                sw1 = sw // 256; sw2 = sw % 256
                self.assertEqual(response, [sw1, sw2])

    def testRSA2048Applet(self):

        apps = []

        def myregister(self, bArray, bOffset, bLength):
            apps.append(self)
        Applet.register = myregister

        tobeencrypted = [0x61, 0x62, 0x63, 0x64]

        import AppletRSA2048
        AppletRSA2048.HandsonRSA2048EncryptDecrypt.install([0], 0, 0)

        app = apps[0]

        app._selectingApplet = False

        apdu = APDU([0x00, 0xAA, 0x01, 0x00] + [len(tobeencrypted)] + tobeencrypted + [0x00])
        app.process(apdu)
        buf = apdu._APDU__buffer[:apdu._outgoinglength]
        self.assertEqual(len(buf), 1024//8)
        buf.extend([0x90, 0x00])

        apdu = APDU([0x00, 0xAA, 0x02, 0x00] + [len(buf)-2] + buf[:-2] + [0])
        app.process(apdu)
        buf = apdu._APDU__buffer[:apdu._outgoinglength]
        self.assertEqual(tobeencrypted, buf)

