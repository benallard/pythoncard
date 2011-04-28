import warnings

def abortTransaction():
    pass

def beginTransaction():
    pass

def commitTransaction():
    pass

def makeTransientShortArray(length, event):
    warnings.warn("Array is not transient")
    return [0 for i in xrange(length)]

makeTransientByteArray = makeTransientShortArray

def makeTransientObjectArray(length, event):
    warnings.warn("Array is not transient")
    return [None for i in xrange(length)]

