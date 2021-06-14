from python.lang import ArrayIndexOutOfBoundsException
from pythoncard.framework import PINException


class OwnerPIN(object):
    """
    /!\ This is intentionnally not secure ... so don't come complaining /!\
    """

    def __init__(self, tryLimit, maxPINSize):
        self._trylimit = tryLimit
        self._triesremaining = 0
        self._maxpinsize = maxPINSize
        self.__pin = [0 for i in range(maxPINSize)]
        self._validated = False

    def getValidatedFlag(self):
        return self._validated

    def setValidatedFlag(self, value):
        self._validated = value

    def getTriesRemaining(self):
        return self._triesremaining

    def check(self, pin, offset, length):
        self._validated = False

        if self._triesremaining <= 0:
            return False

        if (len(pin) < offset) or (len(pin) < offset + length):
            self._triesremaining -= 1
            raise ArrayIndexOutOfBoundsException()

        Pin = [0 for i in range(self._maxpinsize)]
        if isinstance(pin, str):
            i = 0
            for char in pin[offset:offset+length]:
                Pin[i] = ord(char)
                i += 1
            for i in range(length, self._maxpinsize):
                Pin[i] = 0
        else:
            for i in range(offset, offset+length):
                Pin[offset - i] = pin[i]
            for i in range(length, self._maxpinsize):
                Pin[i] = 0

        if self.__pin != Pin:
            self._triesremaining -= 1
            return False

        self._validated = True
        self._triesremaining = self._trylimit
        return True

    def isValidated(self):
        return self._validated

    def reset(self):
        if self._validated:
            self.resetAndUnblock()

    def update(self, pin, offset, length):
        if length > self._maxpinsize:
            raise PINException(length)
        if length+offset > len(pin):
            raise ArrayIndexOutOfBoundsException()

        if isinstance(pin, str):
            i = 0
            for char in pin[offset:offset+length]:
                self.__pin[i] = ord(char)
                i += 1
        else:
            for i in range(offset, offset+length):
                self.__pin[offset - i] = pin[i]

        for i in range(length, self._maxpinsize):
            self.__pin[i] = 0
        self._validated = True
        self._triesremaining = self._trylimit

    def resetAndUnblock(self):
        self._validated = False
        self._triesremaining = self._trylimit

