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
        self._selectingApplet = True
        return True

    def selectingApplet(self):
        return self._selectingApplet

    def install(self, bArray, bOffset, bLength):
        pass

    def process (self, apdu):
        pass

    def getShareableInterfaceObject(self, client_aid, byte):
        return None

    def register(self, bArray=None, bOffset=0, bLength=0):
        pass
