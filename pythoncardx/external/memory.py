from pythoncardx.external import ExternalException

class Memory(object):
    MEMORY_TYPE_MIFARE = 1
    MEMORY_TYPE_EXTENDED_STORE = 2

    @staticmethod
    def getMemoryAccessInstance(memoryType, memorySize, memorySizeOffset):
        raise ExternalException(ExternalException.NO_SUCH_SUBSYSTEM)
