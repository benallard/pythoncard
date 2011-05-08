"""
Using slicer operators would hide the exceptions ...
"""

from python.lang import ArrayIndexOutOfBoundsException
from pythoncard.framework import JCSystem

def arrayCompare(src, srcOff, dest, destOff, length):
    res = True
    try:
        for i in range(length):
            res = res and (src[srcOff+i] == dest[destOff+i])
    except IndexError:
        raise ArrayIndexOutOfBoundsException()
    return res
    
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
    return ((b1 & 0xff) << 8) + (b2 & 0xff)

def getShort(bArray, bOff):
    try:
        return makeShort(bArray[bOff], bArray[bOff+1])
    except IndexError:
        raise ArrayIndexOutOfBoundsException()

def setShort(bArray, bOff, sValue):
    b1 = (sValue & 0xFF00) >> 8
    b2 = sValue & 0xFF
    try:
        bArray[bOff] = b1
        bArray[bOff + 1] = b2
    except IndexError:
        raise ArrayIndexOutOfBoundsException()
