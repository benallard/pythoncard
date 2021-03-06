"""
from javacard:

ISO7816 encapsulates constants related to ISO 7816-3 and ISO 7816-4. ISO7816 interface contains only static fields.

The static fields with SW_ prefixes define constants for the ISO 7816-4 defined response status word. The fields which use the _00 suffix require the low order byte to be customized appropriately e.g (ISO7816.SW_CORRECT_LENGTH_00 + (0x0025 & 0xFF)).

The static fields with OFFSET_ prefixes define constants to be used to index into the APDU buffer byte array to access ISO 7816-4 defined header information.
"""

CLA_ISO7816 = 0x00

INS_EXTERNAL_AUTHENTICATE = 0x82
INS_SELECT = 0xA4

OFFSET_CDATA = 5
OFFSET_CLA = 0
OFFSET_EXT_CDATA = 7
OFFSET_INS = 1
OFFSET_LC = 4
OFFSET_P1 = 2
OFFSET_P2 = 3

SW_APPLET_SELECT_FAILED = 0x6999;
SW_BYTES_REMAINING_00 = 0x6100
SW_CLA_NOT_SUPPORTED = 0x6E00
SW_COMMAND_CHAINING_NOT_SUPPORTED  = 0x6884
SW_COMMAND_NOT_ALLOWED = 0x6986
SW_CONDITIONS_NOT_SATISFIED = 0x6985
SW_CORRECT_LENGTH_00 = 0x6C00
SW_DATA_INVALID = 0x6984
SW_FILE_FULL = 0x6A84
SW_FILE_INVALID = 0x6983
SW_FILE_NOT_FOUND = 0x6A82
SW_FUNC_NOT_SUPPORTED = 0x6A81
SW_INCORRECT_P1P2 = 0x6A86
SW_INS_NOT_SUPPORTED = 0x6D00
SW_LAST_COMMAND_EXPECTED = 0x6883
SW_LOGICAL_CHANNEL_NOT_SUPPORTED = 0x6881
SW_NO_ERROR = 0x9000
SW_RECORD_NOT_FOUND = 0x6A83
SW_SECURE_MESSAGING_NOT_SUPPORTED = 0x6882
SW_SECURITY_STATUS_NOT_SATISFIED = 0x6982
SW_UNKNOWN = 0x6F00
SW_WARNING_STATE_UNCHANGED = 0x6200
SW_WRONG_DATA = 0x6A80
SW_WRONG_LENGTH = 0x6700
SW_WRONG_P1P2 = 0x6B00
