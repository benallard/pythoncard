import warnings

ARRAY_TYPE_BOOLEAN = 1
ARRAY_TYPE_BYTE = 2
ARRAY_TYPE_INT = 4
ARRAY_TYPE_OBJECT = 5
ARRAY_TYPE_SHORT = 3

CLEAR_ON_DESELECT = 2
CLEAR_ON_RESET = 1

MEMORY_TYPE_PERSISTENT = 0
MEMORY_TYPE_TRANSIENT_DESELECT = 2
MEMORY_TYPE_TRANSIENT_RESET = 1

NOT_A_TRANSIENT_OBJECT = 0


def abortTransaction():
    pass

def beginTransaction():
    pass

def commitTransaction():
    pass

def makeTransientShortArray(length, event):
    warnings.warn("Array is not transient")
    return [0 for i in range(length)]

makeTransientByteArray = makeTransientShortArray

def makeTransientBooleanArray(length, event):
    warnings.warn("Array is not transient")
    return [False for i in range(length)]
    

def makeTransientObjectArray(length, event):
    warnings.warn("Array is not transient")
    return [None for i in range(length)]

def requestObjectDeletion():
    pass

def getAvailableMemory(*args):
    """ return the max we can return """
    if len(args) == 1:
        memoryType = args
        return 0x7fff
    elif len(args) == 3:
        buffer, offset, memoryType = args
        if buffer is None:
            raise NullPointerException()
        try:
            buffer[offset] = 0x7f
            buffer[offset+1] = 0xff
        except IndexError:
            raise ArrayIndexOutOfBoundsException()
    else:
        raise TypeError(args)

def makeGlobalArray(type, length):
    if length < 0:
        raise NegativeArraySizeException()
    warnings.warn("Array is not global")
    val = {ARRAY_TYPE_BOOLEAN: False,
           ARRAY_TYPE_BYTE: 0,
           ARRAY_TYPE_INT: 0,
           ARRAY_TYPE_OBJECT: None,
           ARRAY_TYPE_SHORT: 0}[type]
    return [val for i in range(length)]
