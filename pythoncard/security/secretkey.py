from pythoncard.framework.util import arrayCopy
from pythoncard.security.key import Key, _arrayTobinary, _binaryToarray

from pyDes import pyDes

class SecretKey(Key):
    pass

class DESKey(SecretKey):
    def getKey(self, keyData, keyOff):
        raise NotImplementedError

    def setKey(self, keyData, keyOff):
        raise NotImplementedError

class pyDesDESKey(DESKey):
    def __init__(self, typ, size):
        DESKey.__init__(self, typ, size)
        self._key = None
    
    def setKey(self, keyData, keyOff):
        self._key = _arrayTobinary(keyData[keyOff:keyOff+(self.size // 8)])
        self._setInitialized()

    def getKey(self, keyData, keyOff):
        arrayCopy(_binaryToarray(self._key), 0, keyData, keyOff, self.size // 8)
