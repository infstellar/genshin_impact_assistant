from source.exceptions.util import *

class ScriptError(Exception):
    # This is likely to be a mistake of developers, but sometimes a random issue
    pass
class SearchImagePathError(Exception):
    pass

class ThreadTerminated(Exception): pass