class Key(object):

    def __init__(self):
        self.initialized = False

    def isInitialized(self):
        return self.initialized

    def _setInitialized(self):
        self.initialized = True

    def clearKey(self):
        pass
    
    def getType(self):
        pass
