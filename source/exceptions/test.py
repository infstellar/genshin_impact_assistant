from source.exceptions.util import *
from source.interaction.interaction_core import itt

if __name__ == "__main__":
    try:
        raise SnapshotException('123')
    except GIABaseException as e:
        if isinstance(e, SnapshotException):
            e.save_snapshot(itt.capture())