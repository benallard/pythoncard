"""
Make something like that to be able to import the class like in Java:

replace 

import javacard.framework.Applet;

with

from pythoncard.framework import Applet

"""

class CardException(Exception):
    pass

class UserException(Exception):
    pass

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
    ILLEGAL_VALUE = 0

class APDUException(CardRuntimeException):
    BAD_LENGTH = 0
    BUFFER_BOUNDS = 1
    ILLEGAL_USE = 2
    IO_ERROR = 3
    NO_T0_GETRESPONSE = 4
    NO_T0_REISSUE = 5
    T1_IFD_ABORT = 6

class SystemException(CardRuntimeException):
    ILLEGAL_AID	= 4
    ILLEGAL_TRANSIENT = 3
    ILLEGAL_USE = 6
    ILLEGAL_VALUE = 1
    NO_RESOURCE = 5
    NO_TRANSIENT_SPACE = 2

class TransactionException(CardRuntimeException):
    BUFFER_FULL = 3
    IN_PROGRESS = 1
    INTERNAL_FAILURE = 4
    NOT_IN_PROGRESS = 2


from pythoncard.framework import applet, aid, apdu, ownerpin

Applet = applet.Applet
AID = aid.AID
APDU = apdu.APDU
OwnerPIN = ownerpin.OwnerPIN

from pythoncard.framework import jcsystem as JCSystem

from pythoncard.framework import util as Util


