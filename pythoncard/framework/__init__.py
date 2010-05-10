"""
Make something like that to be able to import the class like in Java:

replace 

import javacard.framework.Applet;

with

from pythoncard.framework import Applet

"""

class CardRuntimeException(Exception):
    def __init__(self, reason):
        self._reason = reason

    def getReason(self):
        return self._reason

    def setReason(self, reason):
        self._reason = reason

    @classmethod
    def throwIt(classs, reason):
        raise classs(reason)

class ISOException(CardRuntimeException):
    pass

class PINException(CardRuntimeException):
    pass

from pythoncard.framework import applet, aid, apdu, ownerpin

Applet = applet.Applet
AID = aid.AID
APDU = apdu.APDU
OwnerPIN = ownerpin.OwnerPIN

