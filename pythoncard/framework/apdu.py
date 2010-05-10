BUFFER = []

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
        BUFFER = bytesarr
        self.state = self.STATE_INITIAL

    def getBuffer(self):
        pass

    @staticmethod
    def getCLAChannel():
        pass

    @staticmethod
    def getCurrentAPDU():
        return None

    @staticmethod
    def getCurrentAPDUBuffer():
        return BUFFER

    def getCurrentState(self):
        pass

    @staticmethod
    def getInBlockSize():
        pass

    def getIncomingLength(self):
        pass

    def getNAD(self):
        pass

    def getOffsetCdata(self):
        pass

    @staticmethod
    def getOutBlockSize():
        pass

    @staticmethod
    def getProtocol():
        pass

    def isCommandChainingCLA(self):
        pass

    def isISOInterindustryCLA(self):
        pass

    def isSecureMessagingCLA(self):
        pass
    
    def receiveBytes(self, bOffs):
        pass

    def sendBytes(self, bOffs, len):
        pass

    def sendBytesLong(self, outData, bOffs, len):
        pass

    def setIncomingAndReceive(self):
        pass

    def setOutgoing(self):
        pass

    def setOutgoingAndSend(self, bOffs, len):
        pass

    def setOutgoingLength(self, len):
        pass

    def setoutgoingNoChaining(self):
        pass

    @staticmethod
    def waitExtension():
        pass

