"""
Make something like that to be able to import the class like in Java:

replace 

import javacard.crypto.Cipher;

with

from pythoncard.crypto import Cipher

"""

from pythoncard.crypto import cipher

Cipher = cipher.Cipher
