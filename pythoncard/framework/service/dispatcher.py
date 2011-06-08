from pythoncard.framework.service import ServiceException

class Dispatcher(object):
    PROCESS_COMMAND = 2
    PROCESS_INPUT_DATA = 1
    PROCESS_NONE = 0
    PROCESS_OUTPUT_DATA = 3

    def __init__(self, maxServices):
        if maxServices < 0:
            raise ServiceException(ServiceException.ILLEGAL_PARAM)
        self.services = {Dispatcher.PROCESS_INPUT_DATA : [],
                         Dispatcher.PROCESS_COMMAND : [],
                         Dispatcher.PROCESS_OUTPUT_DATA : [],
                         Dispatcher.PROCESS_NONE: []}

    def addService(self, service, phase):
        if service is None:
            raise ServiceException(ServiceException.ILLEGAL_PARAM)
        try:
            self.services[phase].append(service)
        except KeyError:
            raise ServiceException(ServiceException.ILLEGAL_PARAM)
            
