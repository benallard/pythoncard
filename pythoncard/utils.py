class NotAlwaysStatic(object):
    """ This makes a function both static and not static
    credits goes there (in decreasing order of importance).
    http://users.rcn.com/python/download/Descriptor.htm
    and there:
    http://stackoverflow.com/questions/114214/class-method-differences-in-python-bound-unbound-and-static/114289#114289
    and here:
    http://code.activestate.com/recipes/52304-static-methods-aka-class-methods-in-python/

    For examples of uses see pythoncardx/framework/tlv/bertag.py
    
    """
    def __init__(self, boundname, staticname):
        self.boundname = boundname
        self.staticname = staticname

    def __get__(self, obj, objtype=None):
        if obj is not None:
            return getattr(obj, self.boundname)
        else:
            return getattr(objtype, self.staticname)
