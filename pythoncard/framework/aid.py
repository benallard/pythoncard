from python.lang import ArrayIndexOutOfBoundsException

class AID(object):
    def __init__(self, bArray, offset, length):
        if (length < 5) or (length > 16):
            raise ValueError(length)
        if len(bArray) < offset + length:
            raise ArrayIndexOutOfBoundsException(offset + length)
        self.aid = bArray[offset:offset + length]

    def equals(self, bArray, offset, length):
        if len(bArray) < offset + length:
            raise ArrayIndexOutOfBoundsException(offset + length)
        return self.aid == bArray[offset:offset + length]

    def getBytes(self, dest, offset):
        if len(dest) < offset + len(self.aid):
            raise ArrayIndexOutOfBoundsException(offset + len(self.aid))
        dest[offset:offset + len(self.aid)] = self.aid
        return len(self.aid)

    def getPartialBytes(self, aidOffset, dest, oOffset, oLength):
        if oLength == 0:
            oLength = len(self.aid)
        if len(dest) < oOffset + oLength:
            raise ArrayIndexOutOfBoundsException(oOffset + oLength)
        if len(self.aid) < aidOffset + oLength:
            raise ArrayIndexOutOfBoundsException(aidOffset + oLength)
        dest[oOffset:oOffset+oLength] = self.aid[aidOffset:aidOfset + oLength]
        return oLength

    def partialEquals(self, bArray, offset, length):
        if len(self.aid) < length:
            raise ArrayIndexOutOfBoundsException(length)
        if len(bArray) < offset + length:
            raise ArrayIndexOutOfBoundsException(offset + length)
        return self.aid[:length] == bArray[offset:offset + length]

    def RIDEquals(self, otherAID):
        return self.aid[:5] == otherAID.aid[:5]

    def __eq__(self, other):
        return self.aid == other.aid
