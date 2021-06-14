import unittest
from pythoncard.security import MessageDigest, CryptoException

class testMessageDigest(unittest.TestCase):

    def testSHA1(self):
        md = MessageDigest.getInstance(MessageDigest.ALG_SHA, False)
        self.assertEqual(MessageDigest.ALG_SHA, md.getAlgorithm())
        self.assertEqual(MessageDigest.LENGTH_SHA, md.getLength())
        res = [0]*20
        self.assertEqual(MessageDigest.LENGTH_SHA, md.doFinal([],0,0,res,0))
        self.assertEqual(['\xda', '\x39', '\xa3', '\xee', '\x5e', '\x6b', '\x4b', '\x0d', '\x32', '\x55', '\xbf', '\xef', '\x95', '\x60', '\x18', '\x90', '\xaf', '\xd8', '\x07', '\x09'], res)

        testarray = [ "abc", "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", "a", "0123456701234567012345670123456701234567012345670123456701234567"]
        repeatcount = [1, 1, 1000000, 10]
        resultarray = [['\xA9', '\x99', '\x3E', '\x36', '\x47', '\x06', '\x81', '\x6A', '\xBA', '\x3E', '\x25', '\x71', '\x78', '\x50', '\xC2', '\x6C', '\x9C', '\xD0', '\xD8', '\x9D'],
                       ['\x84', '\x98', '\x3E', '\x44', '\x1C', '\x3B', '\xD2', '\x6E', '\xBA', '\xAE', '\x4A', '\xA1', '\xF9', '\x51', '\x29', '\xE5', '\xE5', '\x46', '\x70', '\xF1'],
                       ['\x34', '\xAA', '\x97', '\x3C', '\xD4', '\xC4', '\xDA', '\xA4', '\xF6', '\x1E', '\xEB', '\x2B', '\xDB', '\xAD', '\x27', '\x31', '\x65', '\x34', '\x01', '\x6F'],
                       ['\xDE', '\xA3', '\x56', '\xA2', '\xCD', '\xDD', '\x90', '\xC7', '\xA7', '\xEC', '\xED', '\xC5', '\xEB', '\xB5', '\x63', '\x93', '\x4F', '\x46', '\x04', '\x52']]

        for i in range(4):
            md.reset()
            for j in range(repeatcount[i]-1):
                md.update(testarray[i], 0, len(testarray[i]))
            md.doFinal(testarray[i], 0, len(testarray[i]), res, 0)
            self.assertEqual(resultarray[i], res)

    def testLengths(self):
        md = MessageDigest.getInstance(MessageDigest.ALG_SHA_512, False)
        self.assertEqual(MessageDigest.ALG_SHA_512, md.getAlgorithm())
        self.assertEqual(MessageDigest.LENGTH_SHA_512, md.getLength())
        md = MessageDigest.getInstance(MessageDigest.ALG_MD5, False)
        self.assertEqual(MessageDigest.LENGTH_MD5, md.getLength())
        md = MessageDigest.getInstance(MessageDigest.ALG_RIPEMD160, False)
        self.assertEqual(MessageDigest.LENGTH_RIPEMD160, md.getLength())
        md = MessageDigest.getInstance(MessageDigest.ALG_SHA_256, False)
        self.assertEqual(MessageDigest.LENGTH_SHA_256, md.getLength())
        md = MessageDigest.getInstance(MessageDigest.ALG_SHA_384, False)
        self.assertEqual(MessageDigest.LENGTH_SHA_384, md.getLength())
        md = MessageDigest.getInstance(MessageDigest.ALG_SHA, False)
        self.assertEqual(MessageDigest.LENGTH_SHA, md.getLength())
