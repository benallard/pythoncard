class KeyPair(object):
    ALG_DSA = 0
    ALG_EC_F2M = 1
    ALG_EC_FP = 2
    ALG_RSA = 3
    ALG_RSA_CRT = 4

    def __init__(self, param1, param2):
        if isinstance(param1, int):
            algorithm = param1
            keylength = param2
            self._algorithm = algorithm
            self._keylength = keylength
            self._publicKey = None
            self._privateKey = None
        else:
            publicKey = param1
            privateKey = param2
            self._publicKey = publicKey
            self._privateKey = privateKey

    def genKeyPair(self):
        pass

    def getPrivate(self):
        return self._privateKey
    
    def getPublic(self):
        return self._publicKey
