import pyautogui
from source import img_manager
from unit import *

import combat_loop, get_domain_reward, pdocr_api, text_manager as textM, interaction_background, posi_manager as PosiM, movement, config
import flow_state as ST
import threading

class Domain_Flow_Control(threading.Thread):
    @logger.catch
    def __init__(self):
        threading.Thread.__init__(self)
        self.current_state=ST.STATE_BEFORE_CHALLENGE
        self.itt=interaction_background.Interaction_BGD()
        chara_list=combat_loop.get_chara_list()
        self.stop_flag=False
        self.combatloop=combat_loop.Combat_Loop(chara_list,super_stop_func=self.get_stop_flag)
        self.gdr=get_domain_reward.Get_Reward()
        self.domaininitflag=False
        self.automatic_start=False
        self.combatloop.pause_threading()
        self.combatloop.start()
        self.gdr.pause_thread()
        self.gdr.start()
        domain_times=configjson["domain_times"]
        self.last_domain_times=domain_times-1
        logger.info('秘境次数：' + str(domain_times))
    
    def stop_thread(self):
        self.stop_flag=True
    
    def checkupstop(self):
        if self.stop_flag:
            logger.info('停止自动秘境')
            self.gdr.stop_thread()
            self.combatloop.stop_threading()
            return True
    
    def get_stop_flag(self):
        return self.stop_flag
    
    def autostartinit(self):
        self.current_state=ST.STATE_BEFORE_CHALLENGE
        self.domaininitflag=False
        self.automatic_start=True
    
    def _state_check(self):
        cap=self.itt.capture()
        cap=self.itt.png2jpg(cap, channel='ui')
        if self.current_state == ST.STATE_BEFORE_CHALLENGE:
            for funcitem in [self._Trigger_READY_CHALLENGE]:
                if funcitem(cap):
                    self.current_state=ST.READY_CHALLENGE
                    
        elif self.current_state == ST.STATE_IN_CHALLENGE:
            for funcitem in [self._Trigger_END_CHALLENGE]:
                if funcitem(cap):
                    self.current_state=ST.END_CHALLENGE
            
        elif self.current_state == ST.STATE_GETTING_REAWARD:
            for funcitem in [self._Trigger_GETTING_REAWARD]:
                if funcitem(cap):
                    self.current_state=ST.READY_GETTING_REAWARD
            
        elif self.current_state == ST.STATE_END_COPY:
            pass
        
    
    def _Trigger_READY_CHALLENGE(self,cap):
        
        if pdocr_api.ocr.getTextPosition(self.itt.crop_image(cap,PosiM.posi_domain['Start']),
                                         textM.text(textM.start_challenge))!=-1:
            return True
        else:
            return False
    
    def _Trigger_END_CHALLENGE(self,cap):
        if pdocr_api.ocr.getTextPosition(self.itt.crop_image(cap,PosiM.posi_domain['LeavingIn']), 
                                         textM.text(textM.LeavingIn))!=-1:
            return True
        else:
            return False
        
    
    def _Trigger_GETTING_REAWARD(self,cap):
        if pdocr_api.ocr.getTextPosition(self.itt.crop_image(cap,PosiM.posi_domain['ClaimRewards']), 
                                         textM.text(textM.claim_rewards))!=-1:
            return True
        else:
            return False
        
    @logger.catch 
    def run(self):
        cap=self.itt.capture()
        cap=self.itt.png2jpg(cap,channel='ui')
        # self.current_state=ST.STATE_GETTING_REAWARD
        # self.domaininitflag=True
        while(1):
            
            if self.checkupstop():
                break
            # if self.domaininitflag==False:
                
            #     continue
            self._state_check()
            if self.current_state==ST.STATE_BEFORE_CHALLENGE:
                
                if self.domaininitflag==False:
                    logger.info('正在开始挑战秘境')
                    movement.reset_view()
                    
                    while(1):
                        if self.checkupstop():
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
                    if self.checkupstop():
                        break
                    # time.sleep(2)
                    if self.checkupstop():
                        break

                    self.domaininitflag=True
                    self.itt.keyDown('w')
                    if self.checkupstop():
                        break
                    time.sleep(5)
                    if self.checkupstop():
                        break
                    
                    
                movement.view_to_angle(-90)
                movement.move(movement.AHEAD,3)
                time.sleep(0.08)
                
            
            elif self.current_state==ST.READY_CHALLENGE:
                self.itt.keyUp('w')
                # self.itt.keyDown('s')
                # time.sleep(0.5)
                # self.itt.keyUp('s')
                # time.sleep(2)
                
                if self.combatloop.pause_threading_flag==True:
                    logger.info('正在开始战斗')
                    self.combatloop.continue_threading()
                
                self.itt.keyPress('f')
                time.sleep(0.1)
                self.current_state=ST.STATE_IN_CHALLENGE
                
            elif self.current_state==ST.STATE_IN_CHALLENGE:
                
                if self.combatloop.pause_threading_flag==True:
                    logger.info('正在开始战斗')
                    self.combatloop.continue_threading()
                time.sleep(3)
                    
            elif self.current_state==ST.END_CHALLENGE:
                logger.info('正在停止战斗')
                self.combatloop.pause_threading()
                time.sleep(5)
                logger.info('等待岩造物消失')
                time.sleep(20)
                self.current_state=ST.STATE_GETTING_REAWARD
                
            elif self.current_state==ST.STATE_GETTING_REAWARD:
                self.gdr.reset_flag()
                self.gdr.continue_thread()
                logger.info('正在激活石化古树')
                while(1):
                    if self.checkupstop():
                        break
                    time.sleep(1)
                    if self.gdr.get_statement()==False:
                        self.current_state=ST.STATE_END_COPY
                        break
            
            elif self.current_state==ST.STATE_END_COPY:
                logger.info('秘境结束。')
                # logger.info('domain over. restart next domain in 5 sec.')
                if self.checkupstop():
                    break
                time.sleep(5)
                if self.checkupstop():
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
                    if self.checkupstop():
                        break
                    time.sleep(5)
                    if self.checkupstop():
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
                    
                    break
                


if __name__=='__main__':
    
    # domain_times=configjson["domain_times"]
    dfc=Domain_Flow_Control()
    dfc.start()
    while(1):
        time.sleep(1)
                