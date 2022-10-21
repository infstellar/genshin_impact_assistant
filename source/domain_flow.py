import pyautogui

from base_threading import Base_Threading
from unit import *

import combat_loop, get_domain_reward, pdocr_api, text_manager as textM, interaction_background, posi_manager as PosiM, movement, config
import flow_state as ST
import threading, img_manager

class Domain_Flow_Control(Base_Threading):
    @logger.catch
    def __init__(self):
        threading.Thread.__init__(self)
        self.current_state=ST.INIT_MOVETO_CHALLENGE
        self.itt=interaction_background.Interaction_BGD()
        chara_list=combat_loop.get_chara_list()
        self.stop_threading_flag=False
        self.combatloop=combat_loop.Combat_Loop(chara_list,super_stop_func=self.get_stop_flag)
        self.gdr=get_domain_reward.Get_Reward()
        self.gdr.setDaemon(True)
        self.combatloop.setDaemon(True)
        # self.domaininitflag=False
        # self.automatic_start=False
        self.combatloop.pause_threading()
        self.combatloop.start()
        self.gdr.pause_thread()
        self.gdr.start()
        domain_times=configjson["domain_times"]
        self.last_domain_times=domain_times-1
        logger.info('秘境次数：' + str(domain_times))
    
    def stop_threading(self):
        logger.info('停止自动秘境')
        self.gdr.stop_thread()
        self.combatloop.stop_threading()
        self.stop_threading_flag=True
    
    def checkup_stop_func(self):
        if self.stop_threading_flag:
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
        if pdocr_api.ocr.getTextPosition(self.itt.crop_image(cap,PosiM.posi_domain['Start']),
                                         textM.text(textM.start_challenge))!=-1:
            return True
        else:
            return False
    
    def _Trigger_AFTER_CHALLENGE(self,cap=None):
        if cap==None:
            cap = self.itt.capture()
            cap = self.itt.png2jpg(cap, channel='ui')
        if pdocr_api.ocr.getTextPosition(self.itt.crop_image(cap,PosiM.posi_domain['LeavingIn']), 
                                         textM.text(textM.LeavingIn))!=-1:
            return True
        else:
            return False
        
    
    def _Trigger_GETTING_REAWARD(self,cap): # Not in using
        if pdocr_api.ocr.getTextPosition(self.itt.crop_image(cap,PosiM.posi_domain['ClaimRewards']), 
                                         textM.text(textM.claim_rewards))!=-1:
            return True
        else:
            return False
        
    @logger.catch 
    def run(self):
        cap=self.itt.capture()
        cap=self.itt.png2jpg(cap,channel='ui')
        while(1):
            
            if self.checkup_stop_threading():
                self.stop_threading()
                time.sleep(10)
                break
            
            # if self.domaininitflag==False:
                
            #     continue
            # self._state_check()
            
            if self.current_state==ST.INIT_MOVETO_CHALLENGE:
                logger.info('正在开始挑战秘境')
                movement.reset_view()
                while(1):
                    if self.checkup_stop_func():
                        break
                    if pdocr_api.ocr.getTextPosition(cap, textM.text(textM.clld)) != -1:
                        break
                    if self.itt.get_img_existence(imgname=img_manager.IN_DOMAIN):
                        break
                    time.sleep(1)
                    cap=self.itt.capture(jpgmode=2)
                
                cap=self.itt.capture(jpgmode=2)
                if pdocr_api.ocr.getTextPosition(cap, textM.text(textM.clld)) != -1:
                    self.itt.move_to(PosiM.posi_domain['CLLD'][0],PosiM.posi_domain['CLLD'][1])
                    time.sleep(1)
                    pyautogui.leftClick()
                time.sleep(5)
                movement.view_to_angle(-90)
            
                self.current_state=ST.BEFORE_MOVETO_CHALLENGE
            
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
                movement.move(movement.AHEAD,4)
                time.sleep(0.08)
                
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
                self.current_state=ST.INIT_GETTING_REAWARD
            
            elif self.current_state==ST.INIT_GETTING_REAWARD:
                # self.gdr.reset_flag()
                self.gdr.continue_threading()
                logger.info('正在激活石化古树')
                self.current_state=ST.IN_GETTING_REAWARD
                    
            elif self.current_state==ST.IN_GETTING_REAWARD:
                time.sleep(3)
                if self.gdr.get_working_statement()==False:
                    self.current_state=ST.END_GETTING_REAWARD
            
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
                    
                    posi=pdocr_api.ocr.getTextPosition(cap, textM.text(textM.conti_challenge))
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
                    posi=pdocr_api.ocr.getTextPosition(cap, textM.text(textM.exit_challenge))
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
                


if __name__=='__main__':
    
    # domain_times=configjson["domain_times"]
    dfc=Domain_Flow_Control()
    dfc.start()
    while(1):
        time.sleep(1)
                