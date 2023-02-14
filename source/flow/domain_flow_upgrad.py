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
    
    def state_before(self):
        if global_itt.get_text_existence(asset.LEYLINEDISORDER):
            global_itt.move_and_click([PosiM.posi_domain['CLLD'][0], PosiM.posi_domain['CLLD'][1]], delay=1)
        time.sleep(0.5)
        movement.reset_view()
        time.sleep(2)
        movement.view_to_angle_domain(-90, self.upper.checkup_stop_func)
        self.rfc = FC.IN
        if self.upper.fast_mode:
            global_itt.key_down('w')
    
    def state_in(self):
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
    
    def state_after(self):
        
        global_itt.key_up('w')
        self._next_rfc()



class CHALLENGE(FlowTemplate):
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
        self._next_rfc()
    
    def state_in(self):
        super().state_in()

        if global_itt.get_text_existence(asset.LEAVINGIN):
            self.rfc = FC.AFTER
        else:
            self.rfc = FC.IN
    
    def state_after(self):
        super().state_after()
        logger.info(t2t('正在停止战斗'))
        self.upper.combat_loop.pause_threading()
        time.sleep(5)
        logger.info(t2t('等待岩造物消失'))
        time.sleep(5)
        self._next_rfc()

class FindingTree(FlowTemplate):
    def __init__(self, upper):
        super().__init__(upper)
        self.flow_id = ST.INIT_CHALLENGE
        self.key_id = FC.INIT
        self.return_flow_id = self.flow_id

    def align_to_tree(self):
        movement.view_to_angle_domain(-90, self.upper.checkup_stop_func)
        t_posi = self.upper.get_tree_posi()
        if t_posi:
            tx, ty = global_itt.get_mouse_point()
            dx = int(t_posi[0] - tx)
            logger.debug(dx)

            if dx >= 0:
                movement.move(movement.RIGHT, self.move_num)
            else:
                movement.move(movement.LEFT, self.move_num)
            if abs(dx) <= 20:
                self.upper.lockOnFlag += 1
                self.move_num = 1
            return True
        else:
            self.move_num = 4
            return False
    
    def state_init(self):
        logger.info(t2t('正在激活石化古树'))
        self.upper.lockOnFlag = 0
        self._next_rfc()

    def state_in(self):
        if self.upper.lockOnFlag <= 5:
            is_tree = self.align_to_tree()
            self.upper.ahead_timer.reset()
            if not is_tree:
                movement.view_to_angle_domain(-90, self.upper.checkup_stop_func)

                if self.isLiYue:  # barrier treatment
                    if self.upper.move_timer.get_diff_time() >= 20:
                        direc = not direc
                        self.upper.move_timer.reset()
                    if direc:
                        movement.move(movement.LEFT, distance=4)
                    else:
                        movement.move(movement.RIGHT, distance=4)

                else:  # maybe can't look at tree
                    logger.debug('can not find tree. moving back.')
                    movement.move(movement.BACK, distance=2)
        else:
            self._next_rfc()

class MoveToTree(FlowTemplate):
    def __init__(self, upper):
        super().__init__(upper)
        self.flow_id = ST.INIT_CHALLENGE
        self.key_id = FC.INIT
        self.return_flow_id = self.flow_id

    def state_before(self):
        global_itt.key_down('w')
        self._next_rfc()

    def state_in(self):
        
        if self.upper.ahead_timer.get_diff_time() >= 5:
            global_itt.key_press('spacebar')
            self.upper.ahead_timer.reset()

        movement.view_to_angle_domain(-90, self.upper.checkup_stop_func)
        if generic_lib.f_recognition(global_itt):
            self._next_rfc()

class AttainReaward(FlowTemplate):
    def __init__(self, upper):
        super().__init__(upper)
        self.flow_id = ST.INIT_CHALLENGE
        self.key_id = FC.INIT
        self.return_flow_id = self.flow_id

    def state_before(self):
        self.itt.key_press('f')
        time.sleep(0.2)
        if not generic_lib.f_recognition():
            self._next_rfc()

    def state_in(self):
        if self.upper.resin_mode == '40':
            global_itt.appear_then_click(asset.USE_20X2RESIN_DOBLE_CHOICES)
        elif self.upper.resin_mode == '20':
            global_itt.appear_then_click(asset.USE_20RESIN_DOBLE_CHOICES)

        if global_itt.get_text_existence(asset.domain_obtain):
            self._next_rfc()



class DomainFlowController(FlowController):
    def __init__(self):
        super().__init__()
        self.flow_connector = FlowConnector()


        
    