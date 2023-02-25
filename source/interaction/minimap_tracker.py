from source.util import *
from source.interaction.interaction_core import itt
from source.common.base_threading import BaseThreading
from source.funclib import static_lib
from common.timer_module import Timer

global tracker, cvAutoTrackerLoop

if True:
    logger.debug("import cvAutoTrack")
    from source.api import cvAutoTrack
    cvAutoTrackerLoop = cvAutoTrack.AutoTrackerLoop()
    cvAutoTrackerLoop.setDaemon(True)
    cvAutoTrackerLoop.start()
    time.sleep(1)
    
    tracker = cvAutoTrackerLoop
    
