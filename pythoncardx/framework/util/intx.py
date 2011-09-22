import warnings

def signed(value, depth):
    """
    return the signed value of the number on the specified depth
    """
    mask = (1 << (depth*8)) - 1
    if value > ((1 << (depth*8)-1) - 1):
        return -(~(value-1) & mask)
    else:
        return value

def s4(i):
    return signed(i, 4)

def sanatize(array):
    for i in range(len(array)):
        array[i] = signed(array[i], 1)

class JCint(object):

    @staticmethod
    
    def getInt(bArray, bOff):
        i =  bArray[bOff] << 24 + \
            bArray[bOff + 1] << 16 + \
            bArray[bOff + 2] << 8 + \
            bArray[bOff + 3]
        return s4(i)
    
    @staticmethod
    def makeInt(*args):
        if len(args) == 4:
            (b1, b2, b3, b4) = args
            i = b1 << 24 + b2 << 16 + b3 << 8 + b4
            return s4(i)
        else:
            (s1, s2) = args
            i = s1 << 16 + s2
            return s4(i)

    @staticmethod
    def makeTransientIntArray(length, event):
        warnings.warn("Array is not transient")
        return [0 for i in range(length)]

    @staticmethod
    def setInt(bArray, bOff, iValue1, iValue2):
        # ints are transmited as two params ...
        iVal = JCint.makeInt(iValue1, iValue2)
        bArray[bOff] = (iVal >> 24) & 0xff
        bArray[bOff + 1] = iVal >> 16 & 0xff
        bArray[bOff + 2] = iVal >> 8 & 0xff
        bArray[bOff + 3] = iVal & 0xff
        return bOff + 4
