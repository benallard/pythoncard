from javacard.framework import CardRuntimeException

class TLVException(CardRuntimeException):
    EMPTY_TAG = 0
    EMPTY_TLV = 1
    ILLEGAL_SIZE = 2
    INSUFFICIENT_STORAGE = 3
    INVALID_PARAM = 4
    MALFORMED_TAG = 5
    MALFORMED_TLV = 6
    TAG_NUMBER_GREATER_THAN_32767 = 7
    TAG_SIZE_GREATER_THAN_127 = 8
    TLV_LENGTH_GREATER_THAN_32767 = 9
    TLV_SIZE_GREATER_THAN_32767 = 10

from pythoncard.framework.tlv import bertag

BERTag = bertag.BERTag
