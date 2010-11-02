"""
Few notes on extended APDU Nominal cases:

Case 1.
    not affected
Case 2S:
    1 >= LE >= 255
Case 2E:
    LE > 255
Case 3S:
    LC < 256
    LE = 0
Case 3E:
    LC > 255
    LE = 0
Case 4S:
    LC < 256
    LE < 256
Case 4E:
    LC > 256 or LE > 256
"""

IN_BLOCKSIZE = 0x80
OUT_BLOCKSIZE = 0x80

from pythoncard.framework import APDUException, ISO7816

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
        if len(bytesarr) < 4:
            raise APDUException(APDUException.BAD_LENGTH)
        self.__buffer = bytesarr
        self.buffer = [0 for i in range(255)]
        # only header is available
        for i in range(4):
            self.buffer[i] = bytesarr[i]
        self._offsetincoming = 4
        if len(bytesarr) > 5:
            if bytesarr[4] == 0:
                self.buffer[4] = bytesarr[4]
                self.buffer[5] = bytesarr[5]
                self.buffer[6] = bytesarr[6]
                self._offsetincoming += 3
            else:
                self.buffer[4] = bytesarr[4]
                self._offsetincoming += 1


        self._state = self.STATE_INITIAL

        # determine the APDU type
        self._cdataoffs = ISO7816.OFFSET_CDATA
        if len(bytesarr) == 4:
            self.type = 1
            self.Nc = 0
            (self.Ne, self._lelength) = (0, 0)
        elif ((len(bytesarr) == 5) or
              ((self.__buffer[4] == 0) and (len(bytesarr) == 7))):
            self.type = 2
            self.Nc = 0
            (self.Ne, self._lelength) = self.__getOutLengths(len(bytesarr))
        elif ((len(bytesarr) == self.__buffer[4] + 5) or
              (len(bytesarr) == self.__getInLengths()[0] + 5)):
            self.type = 3
            (self.Nc, lclength) = self.__getInLengths()
            (self.Ne, self._lelength) = (0, 0)
            self._cdataoffs += lclength - 1
        else:
            self.type = 4
            (self.Nc, lclength)  = self.__getInLengths()
            (self.Ne, self._lelength) = self.__getOutLengths(len(bytesarr))
            self._cdataoffs += lclength - 1
        self._outgoinglength = 0


    def __getInLengths(self):
        """ return a tuple (value, length of value) """
        if self.__buffer[ISO7816.OFFSET_LC] == 0:
            return (self.__buffer[ISO7816.OFFSET_LC + 1] * 256 +
                    self.__buffer[ISO7816.OFFSET_LC + 2]), 3
        else:
            return self.__buffer[ISO7816.OFFSET_LC], 1

    def __getOutLengths(self, length):
        """ return a tuple (value, length of value) """
        length -= 1
        if self.__buffer[length] == 0:
            # Lc and Le must have the same format
            if length != ISO7816.OFFSET_LC:
                if self.__buffer[ISO7816.OFFSET_LC] == 0:
                    if self.__buffer[length-1] == 0:
                        return 65536, 2
            return 256, 1
        else:
            if length != ISO7816.OFFSET_LC:
                if self.__buffer[ISO7816.OFFSET_LC] == 0:
                    return self.__buffer[length-1] * 256 + self.__buffer[length], 2
            return self.__buffer[length], 1


    def getBuffer(self):
        return self.buffer

    @staticmethod
    def getInBlockSize():
        return IN_BLOCKSIZE

    @staticmethod
    def getOutBlockSize():
        return OUT_BLOCKSIZE

    @staticmethod
    def getProtocol():
        pass

    def getNAD(self):
        pass

    def setIncomingAndReceive(self):
        if self._state != self.STATE_INITIAL:
            raise APDUException(APDUException.ILLEGAL_USE)

        tobeprocessed = min(IN_BLOCKSIZE, len(self.__buffer) - self._offsetincoming - self._lelength)
        for i in range(tobeprocessed):
            self.buffer[i+self._offsetincoming] = self.__buffer[i+self._offsetincoming]
        self._offsetincoming += tobeprocessed
        if self._offsetincoming == len(self.__buffer) - self._lelength:
            self._state = self.STATE_FULL_INCOMING
        else:
            self._state = self.STATE_PARTIAL_INCOMING
        return tobeprocessed

    def receiveBytes(self, bOffs):
        if ((self._state < self.STATE_PARTIAL_INCOMING) or
            (self._state >= self.STATE_OUTGOING)):
            raise APDUException(APDUException.ILLEGAL_USE)
        tobeprocessed = min(IN_BLOCKSIZE, len(self.__buffer) - self._offsetincoming - self._lelength)
        for i in range(tobeprocessed):
            self.buffer[bOffs+i] = self.__buffer[self._offsetincoming + i]
        self._offsetincoming += tobeprocessed
        if self._offsetincoming == len(self.__buffer) - self._lelength:
            self._state = self.STATE_FULL_INCOMING
        else:
            self._state = self.STATE_PARTIAL_INCOMING
        return tobeprocessed

    def setOutgoing(self):
        if self._state >= self.STATE_OUTGOING:
            raise APDUException(APDUException.ILLEGAL_USE)
        self._state = self.STATE_OUTGOING
        outgoinglength = self._getOutgoingLength()
        self._curoutgoinglength = 0
        self._outgoinglength = outgoinglength
        return outgoinglength

    def setoutgoingNoChaining(self):
        pass

    def setOutgoingLength(self, len):
        if self._state < self.STATE_OUTGOING:
            raise APDUException(APDUException.ILLEGAL_USE)
        if len > self.Ne:
            raise APDUException(APDUException.BAD_LENGTH)
        self._state = self.STATE_OUTGOING_LENGTH_KNOWN
        self._curoutgoinglength = 0
        self._outgoinglength = len

    def sendBytes(self, bOffs, len):
        if self._state < self.STATE_OUTGOING:
            raise APDUException(APDUException.ILLEGAL_USE)
        if self._curoutgoinglength+len > OUT_BLOCKSIZE:
            raise APDUException(APDUException.BUFFER_BOUNDS)
        self.__buffer[self._curoutgoinglength:self._curoutgoinglength+len] = self.buffer[bOffs:bOffs+len]
        self._curoutgoinglength += len
        if self._curoutgoinglength < self._outgoinglength:
            self._state = self.STATE_PARTIAL_OUTGOING
        else:
            self._state = self.STATE_FULL_OUTGOING

    def sendBytesLong(self, outData, bOffs, len):
        if self.STATE_PARTIAL_OUTGOING < self._state < self.STATE_OUTGOING_LENGTH_KNOWN:
            raise APDUException(APDUException.ILLEGAL_USE)
        if self._curoutgoinglength+len > OUT_BLOCKSIZE:
            raise APDUException(APDUException.BUFFER_BOUNDS)
        self.__buffer[self._curoutgoinglength:self._curoutgoinglength+len] = outData[bOffs:bOffs+len]
        self._curoutgoinglength += len
        if self._curoutgoinglength < self._outgoinglength:
            self._state = self.STATE_PARTIAL_OUTGOING
        else:
            self._state = self.STATE_FULL_OUTGOING

    def setOutgoingAndSend(self, bOffs, len):
        self.setOutgoing()
        self.setOutgoingLength(len)
        self.sendBytes(bOffs, len)

    def getCurrentState(self):
        return self._state

    @staticmethod
    def getCurrentAPDU():
        pass

    @staticmethod
    def getCurrentAPDUBuffer():
        pass

    @staticmethod
    def getCLAChannel():
        pass

    @staticmethod
    def waitExtension():
        pass

    def isCommandChainingCLA(self):
        pass

    def isSecureMessagingCLA(self):
        pass

    def isISOInterindustryCLA(self):
        cla = self.__buffer[ISO7816.OFFSET_CLA]
        return not bool(cla & 0x80) 

    def getIncomingLength(self):
        return self.Nc

    def _getOutgoingLength(self):
        return self.Ne

    def getOffsetCdata(self):
        return self._cdataoffs


