import warnings

class Applet(object):

    def __init__(self):
        pass

    @property
    def RID(self):
        pass

    @property
    def PIX(self):
        pass

    @property
    def AID(self):
        pass

    def deselect(self):
        pass

    def select(self):
        return True

    def selectingApplet(self):
        """ that's weird ..."""
        return self._selectingApplet

    def reSelectingApplet(self):
        return False

    @staticmethod
    def install(bArray, bOffset, bLength):
        """
        To create an instance of the Applet subclass, the Java Card runtime
        environment will call this static method first.
        To be implemented by the subclass
        """
        raise NotImplementedError()

    def process (self, apdu):
        raise NotImplementedError()

    def getShareableInterfaceObject(self, client_aid, byte):
        raise NotImplementedError()

    def register(self, bArray=[], bOffset=0, bLength=0):
        """
        This one is to be implemented by the surrounding system
        """
        warnings.warn("Applet.register should be implemented by the underlying system", RuntimeWarning)
