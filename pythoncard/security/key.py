def _longToArray(long):
    """
    Used to transform long to Array
    >>> longToArray(25L)
    [25]
    >>> longToArray(4867L)
    [3, 19]
    """
    s = hex(long)[2:-1]
    if len(s) % 2 != 0:
        s = '0'+s
    out = []
    for i in range(len(s),0,-2):
        out.append(int(s[i-2:i],16))
    return out

def _arrayTolong(bytes):
    """
    make a long from an Array
    >>> arrayTolong([25])
    25L
    >>> arrayTolong([3, 19])
    4867L
    """
    l = 0L
    for i in range(len(bytes)-1, -1, -1):
        l = l << 8
        l += bytes[i]
    return l

def _binaryToarray(bytes):
    return [ord(c) for c in bytes]

def _arrayTobinary(array):
    return ''.join([chr(i & 0xff) for i in array])

class Key(object):

    def __init__(self, typ, size):
        self.initialized = False
        self.size = size
        self.type = typ

    def isInitialized(self):
        return self.initialized

    def _setInitialized(self):
        self.initialized = True

    def clearKey(self):
        pass
    
    def getType(self):
        return self.type

    def getSize(self):
        return self.size
