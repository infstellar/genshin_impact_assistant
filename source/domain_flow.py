import pyautogui

from base_threading import BaseThreading
from unit import *

import combat_loop, get_domain_reward, pdocr_api, text_manager as textM, interaction_background, posi_manager as PosiM, movement
import timer_module
import flow_state as ST
import img_manager
import yolox_api
import inspect

class Domain_Flow(BaseThreading):
    @logger.catch
    def __init__(self):
        super().__init__()
        self.setName('Domain_Flow')
        
        self.current_state = ST.INIT_MOVETO_CHALLENGE
        # self.current_state = ST.END_ATTAIN_REAWARD
        
        self.itt=interaction_background.Interaction_BGD()
        chara_list=combat_loop.get_chara_list()
        self.combatloop = combat_loop.Combat_Controller(chara_list)
        self.gdr = get_domain_reward.Get_Reward_Flow()
        self.gdr.setDaemon(True)
        self.combatloop.setDaemon(True)
        
        self.combatloop.pause_threading()
        self.combatloop.start()
        self.gdr.pause_thread()
        self.gdr.start()

        domain_times=config_json["domain_times"]
        self.lockOnFlag=0
        self.movenum=2.5
        
        reflash_config()
        self.isLiYue=config_json["isLiYueDomain"]
        self.resin_mode=config_json["resin"]
        self.move_timer=timer_module.Timer()
        self.ahead_timer=timer_module.Timer()
        
        self.last_domain_times=domain_times-1
        logger.info('秘境次数：' + str(domain_times))
    
    def stop_threading(self):
        logger.info('停止自动秘境')
        self.gdr.stop_thread()
        self.combatloop.stop_threading()
        self.stop_threading_flag=True
    
    def checkup_stop_func(self):
        if self.stop_threading_flag or self.pause_threading_flag:
            return True
    
    def get_stop_flag(self):
        return self.stop_threading_flag
    
    def autostartinit(self):
        self.current_state=ST.INIT_MOVETO_CHALLENGE
        # self.domaininitflag=False
        # self.automatic_start=True
    
    def _state_check(self): # Not in using
        cap=self.itt.capture()
        cap=self.itt.png2jpg(cap, channel='ui')
        if self.current_state == ST.BEFORE_MOVETO_CHALLENGE:
            for funcitem in [self._Trigger_AFTER_MOVETO_CHALLENGE]:
                if funcitem(cap):
                    self.current_state=ST.AFTER_MOVETO_CHALLENGE
                    
        elif self.current_state == ST.IN_CHALLENGE:
            for funcitem in [self._Trigger_AFTER_CHALLENGE]:
                if funcitem(cap):
                    self.current_state=ST.END_CHALLENGE
            
        elif self.current_state == ST.IN_GETTING_REAWARD:
            for funcitem in [self._Trigger_GETTING_REAWARD]:
                if funcitem(cap):
                    self.current_state=ST.AFTER_GETTING_REAWARD
            
        elif self.current_state == ST.END_DOMAIN:
            pass
        
    
    def _Trigger_AFTER_MOVETO_CHALLENGE(self,cap=None):
        if cap==None:
            cap = self.itt.capture()
            cap = self.itt.png2jpg(cap, channel='ui')
        if pdocr_api.ocr.get_text_position(self.itt.crop_image(cap, PosiM.posi_domain['Start']),
                                           textM.text(textM.start_challenge))!=-1:
            return True
        else:
            return False
    
    def _Trigger_AFTER_CHALLENGE(self,cap=None):
        if cap==None:
            cap = self.itt.capture()
            cap = self.itt.png2jpg(cap, channel='ui')
        if pdocr_api.ocr.get_text_position(self.itt.crop_image(cap, PosiM.posi_domain['LeavingIn']),
                                           textM.text(textM.LeavingIn))!=-1:
            return True
        else:
            return False
        
    
    def _Trigger_GETTING_REAWARD(self,cap): # Not in using
        if pdocr_api.ocr.get_text_position(self.itt.crop_image(cap, PosiM.posi_domain['ClaimRewards']),
                                           textM.text(textM.claim_rewards))!=-1:
            return True
        else:
            return False
    
    def Flow_INIT_MOVETO_CHALLENGE(self):
        logger.info('正在开始挑战秘境')
        movement.reset_view()
        # cap=self.itt.capture(jpgmode=2)
        while(1):
            cap=self.itt.capture(jpgmode=2)
            if self.checkup_stop_func():
                return 0
            
            if pdocr_api.ocr.get_text_position(cap, textM.text(textM.clld)) != -1:
                break
            if self.itt.get_img_existence(imgname=img_manager.IN_DOMAIN):
                break
            time.sleep(1)
            # cap=self.itt.capture(jpgmode=2)
            
        if self.checkup_stop_func():
            return 0
        
        cap=self.itt.capture(jpgmode=2)
        if pdocr_api.ocr.get_text_position(cap, textM.text(textM.clld)) != -1:
            self.itt.move_to(PosiM.posi_domain['CLLD'][0],PosiM.posi_domain['CLLD'][1])
            time.sleep(1)
            pyautogui.leftClick()
            
        if self.checkup_stop_func():
            return 0
        time.sleep(5)
        movement.view_to_angle(-90)
    
        self.current_state=ST.BEFORE_MOVETO_CHALLENGE
        
    def Flow_IN_FINGING_TREE(self):
        if self.lockOnFlag<=5:
            is_tree=self.align_to_tree()
            self.ahead_timer.reset()
            if is_tree==False:
                movement.view_to_angle(-90)
                
                if self.isLiYue: # barrier treatment
                    if self.move_timer.getDiffTime()>=20:
                        direc=not direc
                        self.move_timer.reset()    
                    if direc:
                        movement.move(movement.LEFT,distance=4)
                    else:
                        movement.move(movement.RIGHT,distance=4)
                
                else: # maybe can't look at tree
                    logger.debug('can not find tree. moving back.')
                    movement.move(movement.BACK,distance=2)
        else:
            self.current_state = ST.END_FINGING_TREE
                
    def Flow_IN_MOVETO_TREE(self):
        while(1):
            if self.ahead_timer.getDiffTime()>=5:
                self.itt.keyPress('spacebar')
                self.ahead_timer.reset()
            
            movement.view_to_angle(-90)
            self.itt.keyDown('w')
            time.sleep(0.2)
            
            cap=self.itt.capture(posi=PosiM.posi_domain["ClaimRewards"]) # posi=PosiM.posi_domain["ClaimRewards"]
            cap=self.itt.png2jpg(cap,channel='ui')
            
            if pdocr_api.ocr.get_text_position(cap, textM.text(textM.claim_rewards)) != -1:
                self.current_state = ST.END_MOVETO_TREE
                return 0
                
    def Flow_IN_ATTAIN_REAWARD(self):
        self.itt.keyUp('w')
        
        self.itt.keyPress('f')
        time.sleep(2)
        
        while(1):
            if self.resin_mode=='40':
                self.itt.appear_then_click(imgname=img_manager.USE_20X2RESIN_DOBLE_CHOICES)
            elif self.resin_mode=='20':
                self.itt.appear_then_click(imgname=img_manager.USE_20RESIN_DOBLE_CHOICES)
            
            if pdocr_api.ocr.get_text_position(self.itt.capture(jpgmode=3), textM.text(textM.domain_obtain)) != -1:
                break
            time.sleep(2)
            
        time.sleep(2)
        self.current_state = ST.END_ATTAIN_REAWARD
        return 0
    
        
    @logger.catch 
    def run(self):
        cap=self.itt.capture()
        cap=self.itt.png2jpg(cap,channel='ui')
        while(1):
            time.sleep(0.2)
            if self.checkup_stop_threading():
                self.stop_threading()
                time.sleep(2)
                return 0
            
            # if self.domaininitflag==False:
                
            #     continue
            # self._state_check()
            
            if self.current_state==ST.INIT_MOVETO_CHALLENGE:
                self.Flow_INIT_MOVETO_CHALLENGE()
            
            elif self.current_state==ST.BEFORE_MOVETO_CHALLENGE:
                self.itt.keyDown('w')
                if self.checkup_stop_func():
                    break
                time.sleep(5)
                self.current_state=ST.IN_MOVETO_CHALLENGE
            
            elif self.current_state==ST.IN_MOVETO_CHALLENGE:
                
                if self.checkup_stop_func():
                    break
                movement.view_to_angle(-90)
                movement.move(movement.AHEAD,5)
                # time.sleep(0.08)
                
                if self._Trigger_AFTER_MOVETO_CHALLENGE():
                    self.current_state=ST.INIT_CHALLENGE
                
            elif self.current_state==ST.INIT_CHALLENGE:
                self.itt.keyUp('w')
                logger.info('正在开始战斗')
                self.combatloop.continue_threading()
                self.itt.keyPress('f')
                time.sleep(0.1)
                
                self.current_state=ST.IN_CHALLENGE
                
            elif self.current_state==ST.IN_CHALLENGE:
                
                time.sleep(3)
                if self._Trigger_AFTER_CHALLENGE():
                    self.current_state=ST.AFTER_CHALLENGE
                    
            elif self.current_state==ST.AFTER_CHALLENGE:
                logger.info('正在停止战斗')
                self.combatloop.pause_threading()
                time.sleep(5)
                logger.info('等待岩造物消失')
                time.sleep(20)
                self.current_state=ST.END_CHALLENGE
            
            elif self.current_state==ST.END_CHALLENGE:
                self.current_state=ST.INIT_FINGING_TREE
            
            elif self.current_state==ST.INIT_FINGING_TREE:
                # self.gdr.reset_flag()
                # self.gdr.continue_threading()
                logger.info('正在激活石化古树')
                self.current_state=ST.IN_FINGING_TREE
                    
            elif self.current_state==ST.IN_FINGING_TREE:
                # time.sleep(3)
                # if self.gdr.get_working_statement()==False:
                #     self.current_state=ST.END_GETTING_REAWARD
                
                self.Flow_IN_FINGING_TREE()
            
            elif self.current_state == ST.END_FINGING_TREE:
                self.current_state = ST.INIT_MOVETO_TREE
                
            elif self.current_state == ST.INIT_MOVETO_TREE:
                self.current_state = ST.IN_MOVETO_TREE
                
            elif self.current_state ==  ST.IN_MOVETO_TREE:
                self.Flow_IN_MOVETO_TREE()
                
            elif self.current_state == ST.END_MOVETO_TREE:
                self.current_state = ST.INIT_ATTAIN_REAWARD
                
            elif self.current_state == ST.INIT_ATTAIN_REAWARD:
                self.current_state = ST.IN_ATTAIN_REAWARD
                
            elif self.current_state == ST.IN_ATTAIN_REAWARD:
                self.Flow_IN_ATTAIN_REAWARD()
            
            elif self.current_state == ST.END_ATTAIN_REAWARD:
                self.current_state = ST.END_GETTING_REAWARD
            
            elif self.current_state==ST.END_GETTING_REAWARD:
                logger.info('秘境结束。')
                # logger.info('domain over. restart next domain in 5 sec.')
                self.current_state=ST.END_DOMAIN
                
            elif self.current_state==ST.END_DOMAIN:
                time.sleep(5)
                if self.checkup_stop_func():
                    break
                cap=self.itt.capture()
                cap=self.itt.png2jpg(cap, channel='ui')
                if self.last_domain_times>=1:
                    logger.info('开始下一次秘境')
                    # logger.info('start next domain.')
                    self.last_domain_times-=1
                    
                    posi=pdocr_api.ocr.get_text_position(cap, textM.text(textM.conti_challenge))
                    if posi!=-1:
                        self.itt.move_to(posi[0],posi[1]+30)
                    else:
                        self.itt.move_to(0,0)
                    time.sleep(0.5)
                    self.itt.leftClick()
                    self.autostartinit()
                    if self.checkup_stop_func():
                        break
                    time.sleep(5)
                    if self.checkup_stop_func():
                        break
                else:
                    logger.info('次数结束。退出秘境')
                    # logger.info('no more times. exit domain.')
                    posi=pdocr_api.ocr.get_text_position(cap, textM.text(textM.exit_challenge))
                    if posi!=-1:
                        self.itt.move_to(posi[0],posi[1]+30)
                    else:
                        self.itt.move_to(0,0)
                    time.sleep(0.5)
                    self.itt.leftClick()
                    # exit all threads
                    self.gdr.stop_thread()
                    self.combatloop.stop_threading()
                    self.stop_threading()
                    time.sleep(10)
                    break
    
    
    def get_tree_posi(self):
        cap = self.itt.capture(shape='xy')
        cap = self.itt.png2jpg(cap)
        # cv2.imshow('123',cap)
        # cv2.waitKey(0)
        addition_info,ret2 = yolox_api.yolo_tree.predicte(cap)
        logger.debug(addition_info)
        if addition_info!=None:
            if addition_info[0][1][0]>=0.5:
                treex, treey=yolox_api.yolo_tree.get_center(addition_info)
                return (treex,treey)
        return False
    
    def align_to_tree(self):
        movement.view_to_angle(-90)
        tposi = self.get_tree_posi()
        if tposi != False:
            tx, ty=self.itt.get_mouse_point()
            dx=int(tposi[0]-tx)
            logger.debug(dx)
            
            if dx>=0:
                movement.move(movement.RIGHT,self.movenum)
            else:
                movement.move(movement.LEFT,self.movenum)
            if abs(dx)<=20:
                self.lockOnFlag+=1
                self.movenum=1
            return True
        else:
            self.movenum=4
            return False 
    


if __name__=='__main__':
    
    # domain_times=configjson["domain_times"]
    dfc=Domain_Flow()
    dfc.start()
    while(1):
        time.sleep(1)
                