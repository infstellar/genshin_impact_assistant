from source.exceptions.util import *
from source.interaction.interaction_core import itt

class TestException(GIABaseException):
    POSSIBLE_REASONS = [
        'test1',
        'test2'
    ]

if __name__ == "__main__":
    
    try:
        raise TestException('123')
    except GIABaseException as e:
        logger.exception(e)
    
    # try:
    #     raise SnapshotException('123')
    # except GIABaseException as e:
    #     if isinstance(e, SnapshotException):
    #         e.save_snapshot(itt.capture())