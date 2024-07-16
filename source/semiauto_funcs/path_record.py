import keyboard

from source.flow.path_recorder_flow import PathRecorderController as PRC
from source.common.base_threading import AdvanceThreading
import source.flow.utils.flow_code as FC, source.flow.utils.flow_state as ST
from source.util import *
from source.ingame_ui.ingame_ui import set_notice

class PathRecord(PRC):
    def __init__(self):
        # MISC
        self.start_record_flag = False
        self.pause_record_flag = False
        super().__init__()
        self.current_flow_id = ST.NULL
        self.flow_dict[ST.PATH_RECORDER].rfc = FC.INIT
        keyboard.add_hotkey('k', self.start_stop_record)
        keyboard.add_hotkey('p', self.pause_resume_record)
        self.flow_connector.start_as_ingame_func = True

    def start_stop_record(self):
        if not self.start_record_flag:
            self.start_record()
            self.start_record_flag = True
        else:
            self.stop_record()
            self.start_record_flag = False

    def pause_resume_record(self):
        if not self.start_record_flag:
            return
        if not self.pause_record_flag:
            self.pause_record()
            self.pause_record_flag = True
        else:
            self.continue_record()
            self.pause_record_flag = False

    def start_record(self):
        set_notice(t2t("ready to start recording"), timeout=3)
        self.reset()
        self.current_flow_id = ST.PATH_RECORDER
        self.flow_dict[ST.PATH_RECORDER].set_rfc_force(FC.BEFORE)


    def pause_record(self):
        set_notice(t2t("pausing recording..."), timeout=3)
        self.current_flow_id = ST.NULL


    def continue_record(self):
        set_notice(t2t("restarting recording..."), timeout=3)
        self.flow_dict[ST.PATH_RECORDER]._reinit_smallmap()
        self.current_flow_id = ST.PATH_RECORDER
        self.flow_dict[ST.PATH_RECORDER].set_rfc_force(FC.IN)


    def stop_record(self):
        set_notice(t2t("ready to stop recording"), timeout=3)
        self.flow_dict[ST.PATH_RECORDER].set_rfc_force(FC.AFTER)


    def reset(self):
        super().reset()
        self.flow_connector.start_as_ingame_func = True
        self.flow_connector.path_name = 'record_'
        self.flow_connector.generator = 'path recorder 1.0'
        self.flow_connector.coll_name = GIAconfig.Dev_RecordPath_CollectionName


if __name__ == '__main__':
    PR = PathRecord()
    PR.start()
    print('pr started')
    from source.ingame_ui.ingame_ui import run_ingame_ui

    run_ingame_ui()
    while 1:
        time.sleep(1)