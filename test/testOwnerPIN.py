import unittest

from pythoncard.framework import OwnerPIN

class testOwnerPIN(unittest.TestCase):
    
    def testOk(self):
        pin = OwnerPIN(3, 15)
        self.assertFalse(pin.isValidated())
        pin.update(u"1234", 0, 4)
        self.assertTrue(pin.check("oo1234--", 2,4))
        self.assertTrue(pin.isValidated())
        pin.reset()
        self.assertFalse(pin.isValidated())
        self.assertFalse(pin.check("123456", 0, 3))
        self.assertFalse(pin.check("1111", 0, 4))
        self.assertEquals(1, pin.getTriesRemaining())

    def testRetryCounter(self):
        pin = OwnerPIN(9, 6)
        pin.update([0,0,1,2,3,4,5,6,7,8,9,0], 3, 5)
        self.assertTrue(pin.check([0,0,1,2,3,4,5,6,7,8,9,0], 3, 5))
        for i in range(9, 0, -1):
            self.assertEquals(i, pin.getTriesRemaining())
            self.assertFalse(pin.check("0000", 0, 4))
        for i in range(5):
            self.assertEquals(0, pin.getTriesRemaining())
            self.assertFalse(pin.check("0000", 0, 4))
        self.assertFalse(pin.check([0,0,1,2,3,4,5,6,7,8,9,0], 3, 5))
        pin.resetAndUnblock()
        self.assertTrue(pin.check([0,0,1,2,3,4,5,6,7,8,9,0], 3, 5))
        for i in range(9, 0, -1):
            self.assertEquals(i, pin.getTriesRemaining())
            self.assertFalse(pin.check("0000", 0, 4))
        for i in range(5):
            self.assertEquals(0, pin.getTriesRemaining())
            self.assertFalse(pin.check("0000", 0, 4))
        self.assertFalse(pin.check([0,0,1,2,3,4,5,6,7,8,9,0], 3, 5))
        
            
