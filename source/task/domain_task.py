from source.util import *
from source.flow.domain_flow_upgrad import DomainFlowController
from source.flow.teyvat_move_flow_upgrad import TeyvatMoveFlowController
from source.task.task_template import TaskTemplate
from source.funclib.collector_lib import load_items_position
from source.funclib.generic_lib import f_recognition
from source.interaction.interaction_core import itt
from source.manager import asset, text_manager
from source.task import task_id as TI
from source.funclib.err_code_lib import ERR_NONE, ERR_STUCK, ERR_PASS
from source.common import timer_module


class DomainTask(TaskTemplate):
    def __init__(self):
        super().__init__()
        self.dfc = DomainFlowController()
        self.tmfc = TeyvatMoveFlowController()
        self.flow_mode = TI.DT_MOVE_TO_DOMAIN
        
        self._add_sub_threading(self.dfc)
        self._add_sub_threading(self.tmfc)
        
        self.domain_name = "山脊守望"
        self.domain_type_name = "不移II"
        self.domain_posi = load_items_position(self.domain_name,mode=1, ret_mode=1)[0]
        self.tmfc.set_parameter(stop_rule = 1, MODE = "Automatic", target_posi = self.domain_posi)
        self.tmfc.set_target_posi(self.domain_posi)
        self.last_domain_times = 3
    
    def _domain_text_process(self, text:str):
        text = text.replace('：', ':')
        text = text.replace(' ', '')
        text = text.replace("Ⅱ", "I")
        if ":" in text:
            text = text[text.index(':')+1:]
        return text
    
    def _enter_domain(self):
        while 1:
            itt.key_press('f')
            if not f_recognition():
                break
        while not itt.get_img_existence(asset.solo_challenge): itt.delay("animation")
        from source.api.pdocr_complete import ocr
        cap_area = asset.switch_domain_area.position
        p1 = ocr.get_text_position(itt.capture(jpgmode=0, posi=cap_area), self.domain_type_name, cap_posi_leftup=cap_area[:2], text_process = self._domain_text_process)
        if p1 != -1:
            itt.move_and_click([p1[0] + 5, p1[1] + 5], delay=1)
        
        # itt.delay(1, comment="too fast TAT")
        ctimer = timer_module.TimeoutTimer(5)
        while 1:
            time.sleep(0.2)
            
            
            itt.appear_then_click(asset.solo_challenge)
            
            itt.appear_then_click(asset.start_challenge)

            if itt.get_img_existence(asset.IN_DOMAIN):
                break
            if ctimer.istimeout():
                if itt.get_text_existence(asset.LEYLINEDISORDER):
                    break
    
    def _end_domain(self):
        time.sleep(0.5)
        cap = itt.capture()
        cap = itt.png2jpg(cap, channel='ui')
        if self.last_domain_times > 1:
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
                return

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
                self.tmfc.continue_threading()
                while 1:
                    time.sleep(self.while_sleep)
                    if self.tmfc.get_last_err_code() == ERR_PASS:
                        break
                self.tmfc.pause_threading()
                
                self._enter_domain()
                
                self.flow_mode = TI.DT_IN_DOMAIN
            
            
            
            
            if self.flow_mode == TI.DT_IN_DOMAIN:
                self.dfc.continue_threading()
                while 1:
                    time.sleep(self.while_sleep)
                    if self.dfc.get_last_err_code() == ERR_PASS:
                        break
                
                self._end_domain()
                    
            
            
if __name__ == '__main__':
    dmt = DomainTask()
    # dmt._enter_domain()
    # dmt.flow_mode = TI.DT_IN_DOMAIN
    dmt.start()