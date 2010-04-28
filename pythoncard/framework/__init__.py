"""
Make something like that to be able to import the class like in Java:

replace 

import javacard.framework.Applet;

with

from pythoncard.framework import Applet

"""

from pythoncard.framework import applet, aid, apdu, ownerpin

Applet = applet.Applet
AID = aid.AID
APDU = apdu.APDU
OwnerPIN = ownerpin.OwnerPIN
