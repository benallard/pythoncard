class Object(object):
    def equals(self, obj):
        return self is obj

class RuntimeException(Exception):
    pass

class IndexOutOfBoundsException(RuntimeException):
    pass

class ArrayIndexOutOfBoundsException(IndexOutOfBoundsException):
    pass

class SecurityException(RuntimeException):
    pass

class NullPointerException(RuntimeException):
    pass

class ArithmeticException(RuntimeException):
    pass

class ClassCastException(RuntimeException):
    pass
