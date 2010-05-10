from pythoncard.framework import APDUException, ISO7816

BUFFER = [0 for i in range(255)]

class APDU(object):
    """
    The APDU Object
    """

    STATE_INITIAL = 0
    STATE_PARTIAL_INCOMING = 1
    STATE_FULL_INCOMING = 2
    STATE_OUTGOING = 3
    STATE_OUTGOING_LENGTH_KNOWN = 4
    STATE_PARTIAL_OUTGOING = 5
    STATE_FULL_OUTGOING = 6

    PROTOCOL_MEDIA_CONTACTLESS_TYPE_A = 0
    PROTOCOL_MEDIA_CONTACTLESS_TYPE_B = 1
    PROTOCOL_MEDIA_DEFAULT = 2
    PROTOCOL_MEDIA_MASK = 3
    PROTOCOL_MEDIA_USB = 4
    PROTOCOL_T0 = 5
    PROTOCOL_T1 = 6
    PROTOCOL_TYPE_MASK = 7
    STATE_ERROR_IO = -1
    STATE_ERROR_NO_T0_GETRESPONSE = -2
    STATE_ERROR_NO_T0_REISSUE = -3
    STATE_ERROR_T1_IFD_ABORT = -4

    def __init__(self, bytesarr):
        for i in range(len(bytesarr)):
            BUFFER[i] = bytesarr[i]
        self._state = self.STATE_INITIAL

    def getBuffer(self):
        return BUFFER

    @staticmethod
    def getInBlockSize():
        pass

    @staticmethod
    def getOutBlockSize():
        pass

    @staticmethod
    def getProtocol():
        pass

    def getNAD(self):
        pass

    def setOutgoing(self):
        if self._state >= self.STATE_OUTGOING:
            raise APDUException(APDUException.ILLEGAL_USE)
        self._state = self.STATE_OUTGOING

    def setoutgoingNoChaining(self):
        pass

    def setOutgoingLength(self, len):
        if self._state < self.STATE_OUTGOING:
            raise APDUException(APDUException.ILLEGAL_USE)
        self._state = self.STATE_OUTGOING_LENGTH_KNOWN
        self._outgoinglength = len

    def receiveBytes(self, bOffs):
        """ Everything is returned at once ... """
        if ((self._state < self.STATE_PARTIAL_INCOMING) or
            (self._state >= self.STATE_OUTGOING)):
            raise APDUException(APDUException.ILLEGAL_USE)
        return 0

    def setIncomingAndReceive(self):
        if self._state != self.STATE_INITIAL:
            raise APDUException(APDUException.ILLEGAL_USE)
        self._state = self.STATE_FULL_INCOMING
        return self.getIncomingLength()

    def sendBytes(self, bOffs, len):
        if self._state < self.STATE_OUTGOING_LENGTH_KNOWN:
            raise APDUException(APDUException.ILLEGAL_USE)
        self._outgoinglength -= len
        if self._outgoinglength > 0:
            self._state = self.STATE_PARTIAL_OUTGOING
        else:
            self._state = self.STATE_FULL_OUTGOING

    def sendBytesLong(self, outData, bOffs, len):
        pass

    def setOutgoingAndSend(self, bOffs, len):
        self.setOutgoingLength(len)
        self.sendBytes(bOffs, len)

    def getCurrentState(self):
        return self._state

    @staticmethod
    def getCurrentAPDU():
        return None

    @staticmethod
    def getCurrentAPDUBuffer():
        return BUFFER

    @staticmethod
    def getCLAChannel():
        return BUFFER[ISO7816.OFFSET_CLA] & 0x3

    @staticmethod
    def waitExtension():
        pass

    def isCommandChainingCLA(self):
        pass

    def isSecureMessagingCLA(self):
        pass

    def isISOInterindustryCLA(self):
        pass

    def getIncomingLength(self):
        return BUFFER[ISO7816.OFFSET_LC]

    def getOffsetCdata(self):
        pass


