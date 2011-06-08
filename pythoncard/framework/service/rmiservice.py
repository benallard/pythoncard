from pythoncard.framework.service import BasicService

class RMIService(BasicService):
    def __init__(self, initialObject):
        self.initialObject = initialObject
