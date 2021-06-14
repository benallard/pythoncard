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
OUT_BLOCKSIZE = 0x100

from ..framework import APDUException, ISOException, ISO7816

from ..utils import u1

# there can only be one (1) APDU at a time ...
_current = None

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
        self.buffer = [0 for i in range(255 + 2)] # 2 for SW
        # only header is available
        for i in range(4):
            self.buffer[i] = bytesarr[i]
        self._offsetincoming = 4
        if len(bytesarr) > 4:
            # there is a P3
            P3len = 1
            if (bytesarr[ISO7816.OFFSET_LC] == 0) and (len(bytesarr) > ISO7816.OFFSET_LC + 3):
                # P3 is extended
                P3len = 3
            for i in range(ISO7816.OFFSET_LC, ISO7816.OFFSET_LC + P3len):
                self.buffer[i] = bytesarr[i]
            self._offsetincoming += P3len

        global _current
        _current = self
        self._state = self.STATE_INITIAL
        self._broken = False

        # determine the APDU type
        # Just for the fun, it's not used anywhere else
        self._cdataoffs = ISO7816.OFFSET_CDATA
        if len(bytesarr) == 4:
            self.type = 1
            self.Nc = 0
            # Set Ne to None: Jan said Length is optionnal, so we might
            # actually have a type 2 APDU ...
            (self.Ne, self._lelength) = (None, 0)
        elif ((len(bytesarr) == 5) or
              ((self.__buffer[4] == 0) and (len(bytesarr) == 7))):
            self.type = 2
            self.Nc = 0
            (self.Ne, self._lelength) = self.__getOutLengths(len(bytesarr))
        elif ((len(bytesarr) == self.__buffer[4] + 5) or
              (len(bytesarr) == self.__getInLengths()[0] + 5)):
            self.type = 3
            (self.Nc, lclength) = self.__getInLengths()
            # same joke about Ne (see type 1)
            (self.Ne, self._lelength) = (None, 0)
            self._cdataoffs += lclength - 1
        else:
            self.type = 4
            (self.Nc, lclength)  = self.__getInLengths()
            (self.Ne, self._lelength) = self.__getOutLengths(len(bytesarr))
            self._cdataoffs += lclength - 1

            if 4 + lclength + self._lelength + self.Nc != len(bytesarr):
                # Final sanity check (as we are in an else statement)
                self._broken = True
            
        self._outgoinglength = 0


    def __getInLengths(self):
        """ return a tuple (value, length of value) """
        if self.__buffer[ISO7816.OFFSET_LC] == 0:
            return (u1(self.__buffer[ISO7816.OFFSET_LC + 1]) * 256 +
                    u1(self.__buffer[ISO7816.OFFSET_LC + 2])), 3
        else:
            return u1(self.__buffer[ISO7816.OFFSET_LC]), 1

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
                    return u1(self.__buffer[length-1]) * 256 + u1(self.__buffer[length]), 2
            return u1(self.__buffer[length]), 1


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
        return (APDU.PROTOCOL_MEDIA_DEFAULT << 4) | APDU.PROTOCOL_T1

    def getNAD(self):
        pass

    def setIncomingAndReceive(self):
        if self._state != self.STATE_INITIAL:
            raise APDUException(APDUException.ILLEGAL_USE)

        if self._broken:
            """ We benefit from the fact that this is the first function called """
            raise ISOException(ISO7816.SW_WRONG_LENGTH)
            

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
        if (self.Ne is not None) and (len > self.Ne):
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
        return _current

    @staticmethod
    def getCurrentAPDUBuffer():
        return _current.getBuffer()

    @staticmethod
    def getCLAChannel():
        return _current.getBuffer()[ISO7816.OFFSET_CLA] & 0x3

    @staticmethod
    def waitExtension():
        pass

    def isCommandChainingCLA(self):
        cla = self.__buffer[ISO7816.OFFSET_CLA]
        return bool(cla & 0x10)

    def isSecureMessagingCLA(self):
        pass

    def isISOInterindustryCLA(self):
        cla = self.__buffer[ISO7816.OFFSET_CLA]
        return (cla & 0x80) == 0x00

    def getIncomingLength(self):
        return self.Nc

    def _getOutgoingLength(self):
        # To prevent troubles with a None value of Ne
        return self.Ne or 0

    def getOffsetCdata(self):
        return self._cdataoffs


