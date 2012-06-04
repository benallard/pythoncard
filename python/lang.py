class Object(object):
    def equals(self, obj):
        return self is obj

class IndexOutOfBoundsException(Exception):
    pass

class ArrayIndexOutOfBoundsException(IndexOutOfBoundsException):
    pass

class RuntimeException(Exception):
    pass

class SecurityException(RuntimeException):
    pass

class NullPointerException(RuntimeException):
    pass

class ArithmeticException(RuntimeException):
    pass

class ClassCastException(RuntimeException):
    pass
