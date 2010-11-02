from pythoncard.framework import Applet, APDU, ISOException, ISO7816
from pythoncard.security import KeyPair, KeyBuilder

from pythoncardx.crypto import Cipher

class HandsonRSA2048EncryptDecrypt (Applet):
    """ actually 1024 ... we are testing not waiting ... """
    rsa_PrivateKey = None
    rsa_PublicKey = None
    rsa_KeyPair = None
    cipherRSA = None

    dataOffset = ISO7816.OFFSET_CDATA

    def __init__(self, bArray, bOffset, bLength):
        self.rsa_KeyPair = KeyPair( KeyPair.ALG_RSA, KeyBuilder.LENGTH_RSA_1024 )
        self.rsa_KeyPair.genKeyPair();
        self.rsa_PublicKey = self.rsa_KeyPair.getPublic();
        self.rsa_PrivateKey = self.rsa_KeyPair.getPrivate();
        self.cipherRSA = Cipher.getInstance(Cipher.ALG_RSA_PKCS1, False);
        self.register(bArray, bOffset + 1, bArray[bOffset]);

    @staticmethod
    def install(self, bArray, bOffset, bLength):
        HandsonRSA2048EncryptDecrypt(bArray, bOffset, bLength);

    def process(self, apdu):
        if self.selectingApplet():
            return

        buf = apdu.getBuffer();

        if buf[ISO7816.OFFSET_CLA] != 0:
            ISOException.throwIt(framework.ISO7816.SW_CLA_NOT_SUPPORTED)

        if buf[ISO7816.OFFSET_INS] != 0xAA:
            ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED)

        try:
            action = {0x01: self.encryptRSA,
                      0x02: self.decryptRSA}
            action[buf[ISO7816.OFFSET_P1]](apdu)
            return
        except KeyError:
            ISOException.throwIt(ISO7816.SW_WRONG_P1P2)

    def encryptRSA(self, apdu):
        a = apdu.getBuffer()
        byteRead = apdu.setIncomingAndReceive()
        assert(self.rsa_PrivateKey.isInitialized())
        self.cipherRSA.init(self.rsa_PublicKey, Cipher.MODE_ENCRYPT)
        cyphertext = self.cipherRSA.doFinal(a, self.dataOffset, byteRead, a, self.dataOffset)

        apdu.setOutgoing();
        apdu.setOutgoingLength(cyphertext);
        apdu.sendBytesLong(a, self.dataOffset, cyphertext);

    def decryptRSA(self, apdu):
        a = apdu.getBuffer()
        byteRead = apdu.setIncomingAndReceive()
        self.cipherRSA.init(self.rsa_PrivateKey, Cipher.MODE_DECRYPT)
        textlength = self.cipherRSA.doFinal(a, self.dataOffset, byteRead, a, self.dataOffset)

        apdu.setOutgoing()
        apdu.setOutgoingLength(textlength )
        apdu.sendBytesLong(a, self.dataOffset, textlength )

