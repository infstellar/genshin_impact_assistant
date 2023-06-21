from source.exceptions.util import *

class MissionException(GIABaseException): pass

class MissionEnd(MissionException):pass
class CollectError(MissionException):
    POSSIBLE_REASONS = []
class TeyvatMoveError(MissionException):
    POSSIBLE_REASONS = []
class PickUpOperatorError(MissionException):
    POSSIBLE_REASONS = []
class HandleExceptionInMission(MissionException):
    POSSIBLE_REASONS = []
class CharacterNotFound(MissionException):
    POSSIBLE_REASONS = [
        t2t("The character is not on the team"),
        t2t("The character name is incorrectly identified. Please submit a log.")
    ]