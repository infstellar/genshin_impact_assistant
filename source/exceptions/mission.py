from source.exceptions.util import *

class MissionException(GIABaseException): pass

class MissionEnd(MissionException):pass
class CollectError(MissionException):pass
class TeyvatMoveError(MissionException):pass
class PickUpOperatorError(MissionException):pass
class HandleExceptionInMission(MissionException):pass
class CharacterNotFound(MissionException):pass