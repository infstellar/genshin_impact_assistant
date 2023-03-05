from source.util import *

global tracker, cvAutoTrackerLoop


logger.debug("import cvAutoTrack")
from source.api import cvAutoTrack
cvAutoTrackerLoop = cvAutoTrack.AutoTrackerLoop()
cvAutoTrackerLoop.setDaemon(True)
cvAutoTrackerLoop.start()
time.sleep(1)

tracker = cvAutoTrackerLoop
    
