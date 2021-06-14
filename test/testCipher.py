import unittest
from pythoncardx.crypto import Cipher
from pythoncard.security import CryptoException, RSAPublicKey, KeyBuilder, KeyPair

class testCipher(unittest.TestCase):

    def testInit(self):
        c = Cipher.getInstance(Cipher.ALG_RSA_NOPAD, False)
        self.assertEqual(Cipher.ALG_RSA_NOPAD, c.getAlgorithm())
        try:
            c.update([], 0, 0, [], 0)
            self.fail()
        except CryptoException as ce:
            self.assertEqual(CryptoException.INVALID_INIT, ce.getReason())
        try:
            c.init("abcd", Cipher.MODE_ENCRYPT)
            self.fail()
        except CryptoException as ce:
            self.assertEqual(CryptoException.ILLEGAL_VALUE, ce.getReason())

        pbk = KeyBuilder.buildKey(KeyBuilder.TYPE_RSA_PUBLIC, KeyBuilder.LENGTH_RSA_1024, False)
        try:
            c.init(pbk, Cipher.MODE_ENCRYPT)
            self.fail()
        except CryptoException as ce:
            self.assertEqual(CryptoException.UNINITIALIZED_KEY, ce.getReason())

        pbk.setExponent([0,1,2,3,4,5,6,7,8,9], 5, 5)
        pbk.setModulus([7]*128, 0, 128) # 1024 // 8

        c.init(pbk, Cipher.MODE_ENCRYPT)

    def testRSAEncryptDecrypt(self):
        kp = KeyPair(KeyPair.ALG_RSA, KeyBuilder.LENGTH_RSA_1024)
        kp.genKeyPair()
        pubk = kp.getPublic()
        self.assertEqual(1024, pubk.getSize())
        privk = kp.getPrivate()
        self.assertEqual(1024, privk.getSize())

        c = Cipher.getInstance(Cipher.ALG_RSA_PKCS1, False)
        c.init(pubk, Cipher.MODE_ENCRYPT)
        res = [0]*1024
        l = c.doFinal([0,1,2,3,4,5], 0, 6, res, 0)

        c.init(privk, Cipher.MODE_DECRYPT)
        res2 = [0]*1024
        l = c.doFinal(res, 0, l, res2, 0)

        self.assertEqual([0,1,2,3,4,5], res2[:l])

    def testRSASignVerify(self):
        kp = KeyPair(KeyPair.ALG_RSA, KeyBuilder.LENGTH_RSA_1024)
        kp.genKeyPair()
        pubk = kp.getPublic()
        self.assertEqual(1024, pubk.getSize())
        privk = kp.getPrivate()
        self.assertEqual(1024, privk.getSize())

        c = Cipher.getInstance(Cipher.ALG_RSA_PKCS1, False)
        c.init(privk, Cipher.MODE_ENCRYPT)
        res = [0]*1024
        l = c.doFinal([0,1,2,3,4,5], 0, 6, res, 0)

        c.init(pubk, Cipher.MODE_DECRYPT)
        res2 = [0]*1024
        l = c.doFinal(res, 0, l, res2, 0)

        self.assertEqual([0,1,2,3,4,5], res2[:l])

    def GemaltoSample(self):
        try:
            rsa = javacardx.crypto.Cipher.getInstance( javacardx.crypto.Cipher.ALG_RSA_NOPAD , False )
            pubkey = javacard.security.KeyBuilder.buildKey(TYPE_RSA_PUBLIC, LENGTH_RSA_512, False )
        except javacardx.crypto.CryptoException as e:
            #... RSA crypto engine not supported by this card
            pass

        pubkey.setModulus( modulus, 0, modulus_len)
        pubkey.setExponent( exponent, 0, expo_len)


        rsa.init(pubkey, MODE_ENCRYPT)

        rsa.doFinal(buffer2encrypt, 0, 64, output_buffer, 0)

    def testDES(self):

        KeyArray = [1,2,3,4,5,6,7,8]
        bytBuffer = [0 for i in range(8)]
        MyBuffer = [7,5,6,8]

        MyDesKey = KeyBuilder.buildKey(KeyBuilder.TYPE_DES, KeyBuilder.LENGTH_DES, False)
        crypt_des = Cipher.getInstance(Cipher.ALG_DES_ECB_PKCS5, False)

        MyDesKey.setKey(KeyArray, 0)
        crypt_des.init(MyDesKey, Cipher.MODE_ENCRYPT)
        length = crypt_des.doFinal(MyBuffer, 0, len(MyBuffer), bytBuffer, 0)
        crypt_des.init(MyDesKey, Cipher.MODE_DECRYPT)
        crypt_des.doFinal(bytBuffer, 0, length, MyBuffer, 0)

        self.assertEqual([7,5,6,8], MyBuffer)
