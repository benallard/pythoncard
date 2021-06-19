import unittest
from pythoncard.security import MessageDigest
from pythoncard.security.key import _binaryToarray

class testMessageDigest(unittest.TestCase):

    def testEmptySHA1(self):
        md = MessageDigest.getInstance(MessageDigest.ALG_SHA, False)
        self.assertEqual(MessageDigest.ALG_SHA, md.getAlgorithm())
        self.assertEqual(MessageDigest.LENGTH_SHA, md.getLength())
        res = [0]*20
        self.assertEqual(MessageDigest.LENGTH_SHA, md.doFinal([],0,0,res,0))
        'da39a3ee5e6b4b0d3255bfef95601890afd80709'
        self.assertEqual(_binaryToarray(bytes.fromhex('da39a3ee5e6b4b0d3255bfef95601890afd80709')), res)

    def testComplexSHA1(self):
        md = MessageDigest.getInstance(MessageDigest.ALG_SHA, False)
        testarray = [ b"abc", b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", b"a", b"0123456701234567012345670123456701234567012345670123456701234567"]
        repeatcount = [1, 1, 1000000, 10]
        resultarray = [_binaryToarray(bytes.fromhex('A9993E364706816ABA3E25717850C26C9CD0D89D')),
                       _binaryToarray(bytes.fromhex('84983E441C3BD26EBAAE4AA1F95129E5E54670F1')),
                       _binaryToarray(bytes.fromhex('34AA973CD4C4DAA4F61EEB2BDBAD27316534016F')),
                       _binaryToarray(bytes.fromhex('DEA356A2CDDD90C7A7ECEDC5EBB563934F460452'))]

        for i in range(4):
            md.reset()
            res = [0]*20
            for j in range(repeatcount[i]-1):
                md.update(testarray[i], 0, len(testarray[i]))
            md.doFinal(testarray[i], 0, len(testarray[i]), res, 0)
            self.assertEqual(resultarray[i], res)

    def testLengths(self):
        for algo, length in [(MessageDigest.ALG_SHA_512, MessageDigest.LENGTH_SHA_512),
                 (MessageDigest.ALG_MD5, MessageDigest.LENGTH_MD5),
                 (MessageDigest.ALG_RIPEMD160, MessageDigest.LENGTH_RIPEMD160),
                 (MessageDigest.ALG_SHA_256, MessageDigest.LENGTH_SHA_256),
                 (MessageDigest.ALG_SHA_384, MessageDigest.LENGTH_SHA_384),
                 (MessageDigest.ALG_SHA, MessageDigest.LENGTH_SHA)]:
            md = MessageDigest.getInstance(algo, False)
            self.assertEqual(algo, md.getAlgorithm())
            self.assertEqual(length, md.getLength())
