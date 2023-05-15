from source.mission.mission.util import *
from source.mission.mission.base import MissionBase
from source.flow import collector_flow_upgrad

class MissionCollector():
    def __init__(self) -> None:
        self.CFCF = collector_flow_upgrad.CollectorFlowController()
        self._add_sub_threading(self.CFCF, start=False)
        self.CFCF_initialized = True
        self.CFCF.start()