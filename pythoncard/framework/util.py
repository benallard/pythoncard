"""
Using slicer operators would hide the exceptions ...
"""

from python.lang import ArrayIndexOutOfBoundsException
from pythoncard.framework import JCSystem

def arrayCompare(src, srcOff, dest, destOff, length):
    try:
        for i in range(length):
            if src[srcOff+i] > dest[destOff+i]:
                return 1
            elif src[srcOff+i] < dest[destOff+i]:
                return -1
    except IndexError:
        raise ArrayIndexOutOfBoundsException()
    return 0
    
def arrayCopy(src, srcOff, dest, destOff, length):
    JCSystem.beginTransaction()
    try:
        for i in range(length):
            dest[destOff+i] = src[srcOff+i]
    except IndexError:
        JCSystem.abortTransaction()
        raise ArrayIndexOutOfBoundsException()
    except: # be exception safe ...
        JCSystem.abortTransaction()
        raise
    JCSystem.commitTransaction()


def arrayCopyNonAtomic(src, srcOff, dest, destOff, length):
    try:
        for i in range(length):
            dest[destOff+i] = src[srcOff+i]
    except IndexError:
        raise ArrayIndexoutOfBoundsException()
    
def arrayFillNonAtomic(bArray, bOff, bLen, bValue):
    try:
        for i in range(bLen):
            bArray[bOff+i] = bValue
    except IndexError:
        raise ArrayIndexOutOfBoundsException()

def makeShort(b1, b2):
    """ a short is signed ... """
    return _signed2(((b1 << 8) & 0xFF00) | (b2 & 0xFF))

def getShort(bArray, bOff):
    try:
        return makeShort(bArray[bOff], bArray[bOff+1])
    except IndexError:
        raise ArrayIndexOutOfBoundsException()

def setShort(bArray, bOff, sValue):
    b1 = _signed1((sValue & 0xFF00) >> 8)
    b2 = _signed1(sValue & 0xFF)
    try:
        bArray[bOff] = b1
        bArray[bOff + 1] = b2
    except IndexError:
        raise ArrayIndexOutOfBoundsException()

# Taken from CAPRunner

def _signed(value, depth):
    """
    return the signed value of the number on the specified depth
    """
    mask = (1 << (depth*8)) - 1
    if value > ((1 << (depth*8)-1) - 1):
        return -(~(value-1) & mask)
    else:
        return value

def _signed1(value):
    return _signed(value, 1)

def _signed2(value):
    return _signed(value, 2)
