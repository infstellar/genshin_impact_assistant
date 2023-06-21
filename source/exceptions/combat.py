from source.exceptions.util import *

class RecognizeCharacterNameError(SnapshotException):
    POSSIBLE_REASONS = [
        t2t("The character name is incorrectly identified. Please submit the log.")
    ]