import unittest

from pythoncard.security import Random, CryptoException

class testRandom(unittest.TestCase):

    def testgetInstance(self):
        try:
            rdm = Random.getInstance(Random.ALG_SECURE_RANDOM)
        except CryptoException:
            self.fail()
            
        try:
            rdm = Random.getInstance(Random.ALG_PSEUDO_RANDOM)
            self.fail()
        except CryptoException, ce:
            if ce.getReason() != CryptoException.NO_SUCH_ALGORITHM:
                self.fail()

    def testGeneratedData(self):
        rdm = Random.getInstance(Random.ALG_SECURE_RANDOM)
        buf = [0 for i in range(50)]
        rdm.generateData(buf, 0, 25)
        self.assertEquals([0 for i in range(25)], buf[25:])
        rdm.generateData(buf, 25, 25)
        self.assert_(buf[:25] != buf[25:])
        