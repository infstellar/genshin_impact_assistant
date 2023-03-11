from source.util import *
from source.task.task_template import TaskTemplate

from source.flow.path_recorder_flow import PathRecorderController
from source.flow.collector_flow_upgrad import CollectorFlowController
from source.map.map import genshin_map

"""
json格式:
{
    "Name":str
    "Type":str
    "Sha1":str
    "Author":str
    "Time":str
    "Comment":str

    "Tasks":[
        *{
            "TaskType":str,"TeyvatMoveTask"|"CollectorTask"|"AutoCombat"|"ConversationTask"
            "TaskArguments":{
                *"ArgumentsName":"Arguments",
                *"ArgumentsName":"Arguments",
                ...
            }
        },
        *{
            "TaskType":str,"TeyvatMoveTask"|"CollectorTask"|"AutoCombat"|"ConversationTask"
            "TaskArguments":{
                *"ArgumentsName":"Arguments",
                *"ArgumentsName":"Arguments",
                ...
            }
        },
        ...
        
    ]
}

记录:
    [: start/end mission recording

    num1: start/end path recording
    num2: start collection recording:
        num4: add a pickup point flag
        num2: stop collection recording
    num3: add an auto combat flag


执行:
    1. 按顺序执行每个Task:
        1.1 按照Task Type传入参数,执行
        1.2 等待结束

"""


class MissionGenerateTask(TaskTemplate):
    def __init__(self):
        super().__init__()

        self.mission_json = {
            "Name":"",
            "Type":"",
            "Sha1":"",
            "Author":"",
            "Time":str(time.time()),
            "Comment":"",
            "Tasks":[]
        }
        
        self.PRCF = PathRecorderController()
        self.CFCF = CollectorFlowController()

        self._add_sub_threading(self.PRCF)
        self._add_sub_threading(self.CFCF)

        self.PRCF_flag = False
        self.CFCF_flag = False

        self.CFCF_content = {
            
        }

    def _addjson_PRCF(self, PRCF_content):
        self.mission_json["Tasks"].append(
            {
                "TaskType":"TeyvatMoveTask",
                "TaskArguments":PRCF_content
            }
        )

    def _addjson_CFCF(self):
        self.mission_json["Tasks"].append(
            {
                "TaskType":"TeyvatMoveTask",
                "TaskArguments":self.CFCF_content
            }
        
        )

    def _start_stop_path_recording(self):
        if not self.PRCF_flag:
            # start PRCF
            self.PRCF.reset()
            self.PRCF.continue_threading()
        else:
            self.PRCF.pause_threading()
            self._addjson_PRCF(self.PRCF.flow_connector.total_collection_list)

    def _start_stop_CollectorTask(self):
        if not self.CFCF_flag:
            self.CFCF_content={}
        else:
            self._addjson_CFCF()

    def _add_collection_point(self):
        curr_posi = genshin_map.get_position()
        self.CFCF_content[""].append()

    def exec_task(self):
        pass
    

    