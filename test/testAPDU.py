import unittest

from pythoncard.framework import APDU, ISO7816

class testAPDU(unittest.TestCase):

    def testState(self):
        apdu = APDU([0x00, 0x20, 0x01, 0x00, 0x04, 0x31, 0x32, 0x33, 0x34])
        self.assertEquals(APDU.STATE_INITIAL, apdu.getCurrentState())
        apdu.setIncomingAndReceive()
        self.assertTrue(APDU.STATE_PARTIAL_INCOMING <= apdu.getCurrentState())
        self.assertEquals(4, apdu.getIncomingLength())

    def testBuffer(self):
        apdu = APDU([0x00, 0x20, 0x01, 0x00, 0x04, 0x31, 0x32, 0x33, 0x34])
        buffer = apdu.getBuffer()
        self.assertEquals(0x00, buffer[ISO7816.OFFSET_CLA])
        self.assertEquals(0x20, buffer[ISO7816.OFFSET_INS])
        self.assertEquals(0x01, buffer[ISO7816.OFFSET_P1])
        self.assertEquals(0x00, buffer[ISO7816.OFFSET_CLA])

        buffer[0] = 1; buffer[1] = 2; buffer[2] = 3

        buff = apdu.getBuffer()
        self.assertEquals(1, buff[0])
        self.assertEquals(2, buff[1])
        self.assertEquals(3, buff[2])

    def testAPDUDoc(self):
        """ This is an adaptation of the piece of code on the APDU page """
        apdu = APDU([0x00, 0x20, 0x01, 0x00, 0x04, 0x31, 0x32, 0x33, 0x34])
        buffer = apdu.getBuffer()
        cla = buffer[ISO7816.OFFSET_CLA]
        ins = buffer[ISO7816.OFFSET_INS]

        # assume this command has incoming data
        # Lc tells us the incoming apdu command length
        bytesLeft = buffer[ISO7816.OFFSET_LC]

        readCount = apdu.setIncomingAndReceive()
        while  bytesLeft > 0:
            # process bytes in buffer[5] to buffer[readCount+4];
            bytesLeft -= readCount
            readCount = apdu.receiveBytes ( ISO7816.OFFSET_CDATA )

        # Note that for a short response as in the case illustrated here
        # the three APDU method calls shown : setOutgoing(),setOutgoingLength() & sendBytes()
        # could be replaced by one APDU method call : setOutgoingAndSend().

        # construct the reply APDU
        le = apdu.setOutgoing()
        apdu.setOutgoingLength( 3 )

        # build response data in apdu.buffer[ 0.. outCount-1 ];
        buffer[0] = 1; buffer[1] = 2; buffer[3] = 3
        apdu.sendBytes ( 0 , 3 )