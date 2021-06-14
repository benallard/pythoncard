import unittest
import random

from pythoncard.framework import Util
from python.lang import ArrayIndexOutOfBoundsException

class testUtil(unittest.TestCase):
    
    def testArrayCompare(self):
        a1 = [1,2,3,4]
        a2 = [0,1,2,3,4]

        self.assertEqual(0, Util.arrayCompare(a1, 0, a2, 1, 4))

        self.assertEqual(1, Util.arrayCompare(a1, 2, a2, 0, 2))

        self.assertEqual(-1, Util.arrayCompare(a2, 0, a1, 2, 2))

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
        self.assertEqual(a1[2:2+3], a2[0:0+3])

    def testShort(self):
        a = [0,0,0,0]
        for i in range(30):
            s1 = random.randint(-128, 127)
            s2 = random.randint(-128, 127)
            s = Util.makeShort(s1, s2)
            Util.setShort(a, 1, s)
            self.assertEqual(s1, a[1])
            self.assertEqual(s2, a[2])
            self.assertEqual(s, Util.getShort(a, 1))
