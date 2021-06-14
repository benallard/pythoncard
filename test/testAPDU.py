import unittest, random

from pythoncard.framework import APDU, ISO7816

class testAPDU(unittest.TestCase):

    def testState(self):
        apdu = APDU([0x00, 0x20, 0x01, 0x00, 0x04, 0x31, 0x32, 0x33, 0x34, 0x00])
        self.assertEqual(APDU.STATE_INITIAL, apdu.getCurrentState())
        apdu.setIncomingAndReceive()
        self.assertTrue(APDU.STATE_PARTIAL_INCOMING <= apdu.getCurrentState())
        apdu.receiveBytes(ISO7816.OFFSET_CDATA)
        self.assertEqual(APDU.STATE_FULL_INCOMING, apdu.getCurrentState())
        apdu.setOutgoing()
        self.assertEqual(APDU.STATE_OUTGOING, apdu.getCurrentState())
        apdu.setOutgoingLength(10)
        self.assertEqual(APDU.STATE_OUTGOING_LENGTH_KNOWN, apdu.getCurrentState())
        apdu.sendBytes(0, 2)
        self.assertEqual(APDU.STATE_PARTIAL_OUTGOING, apdu.getCurrentState())
        apdu.sendBytes(0, 8)
        self.assertEqual(APDU.STATE_FULL_OUTGOING, apdu.getCurrentState())

    def testBuffer(self):
        apdu = APDU([0x00, 0x20, 0x01, 0x00, 0x04, 0x31, 0x32, 0x33, 0x34])
        buffer = apdu.getBuffer()
        self.assertEqual(0x00, buffer[ISO7816.OFFSET_CLA])
        self.assertEqual(0x20, buffer[ISO7816.OFFSET_INS])
        self.assertEqual(0x01, buffer[ISO7816.OFFSET_P1])
        self.assertEqual(0x00, buffer[ISO7816.OFFSET_CLA])

        buffer[0] = 1; buffer[1] = 2; buffer[2] = 3

        buff = apdu.getBuffer()
        self.assertEqual(1, buff[0])
        self.assertEqual(2, buff[1])
        self.assertEqual(3, buff[2])

    def testAPDUDoc(self):
        """ This is an adaptation of the piece of code on the APDU page """
        apdu = APDU([0x00, 0x20, 0x01, 0x00, 0x04, 0x31, 0x32, 0x33, 0x34, 0x00])
        buffer = apdu.getBuffer()
        cla = buffer[ISO7816.OFFSET_CLA]
        self.assertEqual(0, cla)
        ins = buffer[ISO7816.OFFSET_INS]
        self.assertEqual(0x20, ins)

        # assume this command has incoming data
        # Lc tells us the incoming apdu command length
        bytesLeft = buffer[ISO7816.OFFSET_LC]
        self.assertEqual(4, bytesLeft)

        readCount = apdu.setIncomingAndReceive()
        self.assertEqual(4, readCount)
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
        self.assertEqual(APDU.STATE_FULL_OUTGOING,
                          apdu.getCurrentState())


    def testExtAPDULength(self):
        pass

    def testReceiveData(self):

        def receiveData(apdu):
            buffer = apdu.getBuffer()
            LC = apdu.getIncomingLength()
            recvLen = apdu.setIncomingAndReceive()
            dataOffset = apdu.getOffsetCdata()

            while recvLen > 0:
                # process data in buffer[dataOffset]
                recvLen = apdu.receiveBytes(dataOffset)
            # done

        pass

    def testSendData(self):

        def sendData(apdu):
            buffer = apdu.getBuffer()
            LE = apdu.setOutgoing()
            toSend = random.randint(0,65535)

            if LE != toSend:
                apdu.setOutgoingLength(toSend)

            while toSend > 0:
                # prepare data to send in APDU buffer
                apdu.sendBytes(dataOffset, sentLen)
                toSend -= sentLen
            # done

        pass
