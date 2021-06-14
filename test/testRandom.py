import unittest

from pythoncard.security import RandomData, CryptoException

class testRandom(unittest.TestCase):

    def testgetInstance(self):
        try:
            rdm = RandomData.getInstance(RandomData.ALG_SECURE_RANDOM)
        except CryptoException:
            self.fail()
            
        try:
            rdm = RandomData.getInstance(RandomData.ALG_PSEUDO_RANDOM)
            self.fail()
        except CryptoException as ce:
            if ce.getReason() != CryptoException.NO_SUCH_ALGORITHM:
                self.fail()

    def testGeneratedData(self):
        rdm = RandomData.getInstance(RandomData.ALG_SECURE_RANDOM)
        buf = [0 for i in range(50)]
        rdm.generateData(buf, 0, 25)
        self.assertEqual([0 for i in range(25)], buf[25:])
        rdm.generateData(buf, 25, 25)
        self.assertTrue(buf[:25] != buf[25:])
        
