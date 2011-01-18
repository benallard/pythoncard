import unittest
import random

from pythoncard.framework import Util
from python.lang import ArrayIndexOutOfBoundsException

class testUtil(unittest.TestCase):
    
    def testArrayCompare(self):
        a1 = [1,2,3,4]
        a2 = [0,1,2,3,4]

        self.assertTrue(Util.arrayCompare(a1, 0, a2, 1, 4))

        self.assertFalse(Util.arrayCompare(a1, 2, a2, 0, 2))

        try:
            # overflow near the end
            a1[3] = a2[0]
            Util.arrayCompare(a1, 3, a2, 0, 5)
            self.fail()
        except ArrayIndexOutOfBoundsException:
            pass

        try:
            # immediate first array overflow
            Util.arrayCompare(a1, 8, a2, 0, 5)
            self.fail()
        except ArrayIndexOutOfBoundsException:
            pass

        try:
            # immediate second array overflow
            Util.arrayCompare(a1, 0, a2, 8, 5)
            self.fail()
        except ArrayIndexOutOfBoundsException:
            pass

    def testArrayCopy(self):
        a1 = [1,2,3,4,5]
        a2 = [0,0,0,0,0,0,0,0,0]
        
        Util.arrayCopy(a1, 2, a2, 0, 3)
        self.assertEquals(a1[2:2+3], a2[0:0+3])

    def testShort(self):
        a = [0,0,0,0]
        for i in range(3):
            s = random.randint(0, 0xFFFF)
            Util.setShort(a, 1, s)
            self.assertEquals(s, Util.getShort(a, 1))
