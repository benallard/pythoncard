from pythoncard.framework import CardRuntimeException

class ServiceException(CardRuntimeException):
    CANNOT_ACCESS_IN_COMMAND = 4
    CANNOT_ACCESS_OUT_COMMAND = 5
    COMMAND_DATA_TOO_LONG = 3
    COMMAND_IS_FINISHED = 6
    DISPATCH_TABLE_FULL = 2
    ILLEGAL_PARAM = 1
    REMOTE_OBJECT_NOT_EXPORTED = 7

class Service(object):
    pass

from pythoncard.framework.service import cardremoteobject
CardRemoteObject = cardremoteobject.CardRemoteObject

from pythoncard.framework.service import dispatcher
Dispatcher = dispatcher.Dispatcher

from pythoncard.framework.service import basicservice
BasicService = basicservice.BasicService

from pythoncard.framework.service import rmiservice
RMIService = rmiservice.RMIService
