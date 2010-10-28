from pythoncard.framework import CardRuntimeException

class ExternalException(CardRuntimeException):
    NO_SUCH_SUBSYSTEM = 1
    INVALID_PARAM = 2
    INTERNAL_ERROR = 3

from pythoncardx.external import memory

Memory = memory.Memory

