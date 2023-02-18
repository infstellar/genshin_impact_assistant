from source.util import *
from source.flow.domain_flow_upgrad import DomainFlowController
from source.flow.teyvat_move_flow_upgrad import TeyvatMoveFlowController
from source.task.task_template import TaskTemplate
from source.funclib.collector_lib import load_items_position
from source.interaction.interaction_core import itt
from source.manager import asset, text_manager
from common import flow_state as ST
from source.task import task_id as TI
from source.funclib.err_code_lib import ERR_NONE, ERR_STUCK, ERR_PASS


class DomainTask(TaskTemplate):
    def __init__(self):
        super().__init__()
        self.dfc = DomainFlowController()
        self.tmc = TeyvatMoveFlowController()
        self.flow_mode = TI.DT_MOVE_TO_DOMAIN
        
        self._add_sub_threading(self.dfc)
        self._add_sub_threading(self.tmc)
        
        self.domain_name = "孤云凌霄之处"
        self.domain_type = "VI"
        self.domain_posi = load_items_position(self.domain_name,mode=1, ret_mode=1)[0]
        self.tmc.set_stop_rule(1)
        self.tmc.set_target_posi(self.domain_posi)
        self.last_domain_times = 2
    
    def _enter_domain(self):
        itt.key_press('f')
        domain_text = text_manager.TextTemplate({
            GLOBAL_LANG: self.domain_type
        }, cap_area=asset.switch_domain_area.position)
        
        while not itt.appear_then_click(domain_text):
            time.sleep(0.2)
            
        while 1:
            time.sleep(0.2)
            
            
            itt.appear_then_click(asset.solo_challenge)
            
            itt.appear_then_click(asset.start_challenge)

            if itt.get_img_existence(asset.IN_DOMAIN):
                break
            if itt.get_text_existence(asset.LEYLINEDISORDER):
                break
    
    def _end_domain(self):
        time.sleep(0.5)
        cap = itt.capture()
        cap = itt.png2jpg(cap, channel='ui')
        if self.last_domain_times >= 1:
            logger.info(t2t('开始下一次秘境'))
            # logger.info('start next domain.')
            self.last_domain_times -= 1
            while 1:
                r = itt.appear_then_click(asset.conti_challenge)
                if r:
                    break
            self.flow_mode = TI.DT_IN_DOMAIN
            self.dfc.reset()
            
        else:
            logger.info(t2t('次数结束。退出秘境'))
            # logger.info('no more times. exit domain.')
            while 1:
                r = itt.appear_then_click(asset.exit_challenge)
                if r:
                    break
            # exit all threads
            self.stop_threading()
            time.sleep(10)
            
    def run(self) -> None:
        '''if you're using this class, copy this'''
        while 1:
            time.sleep(self.while_sleep)
            if self.stop_threading_flag:
                return 0

            if self.pause_threading_flag:
                if self.working_flag:
                    self.working_flag = False
                time.sleep(1)
                continue

            if not self.working_flag:
                self.working_flag = True
                
            if self.checkup_stop_func():
                self.pause_threading_flag = True
                continue
            '''write your code below'''

            if self.flow_mode == TI.DT_MOVE_TO_DOMAIN:
                self.tmc.continue_threading()
                while 1:
                    time.sleep(self.while_sleep)
                    if self.tmc.get_last_err_code() == ERR_PASS:
                        break
                self.tmc.pause_threading()
                
                self._enter_domain()
                
                self.flow_mode = TI.DT_IN_DOMAIN
            
            
            
            
            if self.flow_mode == TI.DT_IN_DOMAIN:
                self.dfc.continue_threading()
                while 1:
                    time.sleep(self.while_sleep)
                    if self.dfc.get_last_err_code() == ERR_PASS:
                        break
                
                self._end_domain()
                    
            
            
