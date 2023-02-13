from source.util import *
from source.flow.flow_template import FlowController, FlowTemplate, FlowConnector
import source.flow.flow_code as FC
from source.controller import combat_loop
from source.constant import flow_state as ST
from source.base import timer_module
from source.funclib import generic_lib, movement
from source.manager import posi_manager as PosiM, asset
from source.interaction.interaction_core import global_itt
from source.api import yolox_api
from source.common.base_threading import BaseThreading

class DomainFlowConnector(FlowConnector):
    def __init__(self):
        global_itt = global_itt
    
    

class MoveToChallenge(FlowTemplate):
    def __init__(self, upper):
        super().__init__(upper)
        self.flow_id = ST.INIT_MOVETO_CHALLENGE
        self.key_id = FC.INIT
        self.return_flow_id = self.flow_id
        
    def state_init(self):
        super().state_init()
        logger.info(t2t('正在开始挑战秘境'))
        movement.reset_view()
        if global_itt.get_text_existence(asset.LEYLINEDISORDER):
            self.rfc = FC.BEFORE
        if global_itt.get_img_existence(asset.IN_DOMAIN):
            self.rfc = FC.BEFORE
        time.sleep(1)

        self.rfc = FC.INIT
        
        return self.rfc
    
    def state_before(self):
        super().state_before()
        if global_itt.get_text_existence(asset.LEYLINEDISORDER):
            global_itt.move_and_click([PosiM.posi_domain['CLLD'][0], PosiM.posi_domain['CLLD'][1]], delay=1)
        time.sleep(0.5)
        movement.reset_view()
        time.sleep(2)
        movement.view_to_angle_domain(-90, self.upper.checkup_stop_func)
        self.rfc = FC.IN
        if self.upper.fast_mode:
            global_itt.key_down('w')
        return self.rfc
    
    def state_in(self):
        super().state_in()
        movement.view_to_angle_domain(-90, self.checkup_stop_func)
        if self.upper.fast_mode:
            pass
        else:
            movement.move(movement.AHEAD, 4)

        if generic_lib.f_recognition(global_itt):
            self.while_sleep = 0.2
            self.rfc = FC.BEFORE

        t = self.upper.fast_move_timer.loop_time()  # max check up speed: 1/10 second
        if t <= 1 / 10:
            time.sleep(1 / 10 - t)
        else:
            pass
        return self.rfc
    
    def state_after(self):
        super().state_after()
        
        global_itt.key_up('w')
        self.rfc = FC.END
        
        return self.rfc
    
    def state_end(self):
        super().state_end()
        self.rfc = FC.OVER
        return self.rfc

class TAAA(FlowTemplate):
    def __init__(self, upper):
        super().__init__(upper)
        self.flow_id = ST.INIT_CHALLENGE
        self.key_id = FC.INIT
        self.return_flow_id = self.flow_id
        
    def state_init(self):
        super().state_init()
        logger.info(t2t('正在开始战斗'))
        self.upper.combat_loop.continue_threading()
        global_itt.key_press('f')
        time.sleep(0.1)
        self.rfc = FC.BEFORE
        return self.rfc
    
    def state_before(self):
        super().state_before()

        self.rfc = FC.IN
        return self.rfc
    
    def state_in(self):
        super().state_in()

        if global_itt.get_text_existence(asset.LEAVINGIN):
            self.rfc = FC.AFTER
        else:
            self.rfc = FC.IN
        return self.rfc
    
    def state_after(self):
        super().state_after()
        logger.info(t2t('正在停止战斗'))
        self.upper.combat_loop.pause_threading()
        time.sleep(5)
        logger.info(t2t('等待岩造物消失'))
        time.sleep(5)
        self.rfc = FC.END
        
        return self.rfc
    
    def state_end(self):
        super().state_end()
        
        self.rfc = FC.OVER
        return self.rfc

class DomainFlowController(FlowController):
    def __init__(self):
        super().__init__()
        self.flow_connector = FlowConnector()
        
    