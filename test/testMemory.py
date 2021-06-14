import unittest

from pythoncardx.external import Memory, ExternalException

class testMemory(unittest.TestCase):

    def Mifare(self):
        try:
            myaccess = Memory.getMemoryAccessInstance(Memory.MEMORY_TYPE_MIFARE, [], 0)
            self.fail()
        except ExternalException as ee:
            self.assertEqual(ExternalException.NO_SUCH_SUBSYSTEM, ee.getReason())
