class SCIRuntimeError(ValueError):
    pass


class ActionHandlerNotFound(ValueError):
    pass


class ActionNotSupported(ValueError):
    pass


class SCI_AppError(ValueError):
    pass 


class SCI_ResponseError(ValueError):
    pass


class SendResponseError(ValueError):
    pass


class EcsaddoStructureError(ValueError):
    pass


class DestinationError(ValueError):
    pass


class WaitWhenAnyTimerIsReadyError(ValueError):
    pass