"""
It's 2.2 ... not that prioritary ...
"""

class BERTag(object):
    BER_TAG_CLASS_MASK_APPLICATION = 0
    BER_TAG_CLASS_MASK_CONTEXT_SPECIFIC = 1
    BER_TAG_CLASS_MASK_PRIVATE = 2
    BER_TAG_CLASS_MASK_UNIVERSAL = 3
    BER_TAG_TYPE_CONSTRUCTED = 4
    BER_TAG_TYPE_PRIMITIVE = 5

    def __init__(self):
        self._tag = 0
        self._length = 0
        self._value = []
    
    def equals(self, otherTag):
        pass

    @classmethod
    def getInstance(classs, bArray, bOff):
        c = classs()
        c.init(bArray, bOff)
        return c
    
