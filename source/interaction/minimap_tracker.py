from source.util import *

global tracker, cvAutoTrackerLoop

if False:
    logger.debug("import cvAutoTrack")
    from source.api import cvAutoTrack
    cvAutoTrackerLoop = cvAutoTrack.AutoTrackerLoop()
    cvAutoTrackerLoop.setDaemon(True)
    cvAutoTrackerLoop.start()
    time.sleep(1)

    tracker = cvAutoTrackerLoop
else:
    from source.map.map import genshin_map
    tracker = genshin_map
    
