import unittest

from pythoncard.security import KeyBuilder

class testKeyBuilder(unittest.TestCase):

    def testLength(self):
        key = KeyBuilder.buildKey(KeyBuilder.TYPE_RSA_PUBLIC, KeyBuilder.LENGTH_RSA_768, False)
        self.assertEqual(768, key.getSize())
