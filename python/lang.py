class Object(object):
    pass

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

class ClassCastException(RuntimeException):
    pass
