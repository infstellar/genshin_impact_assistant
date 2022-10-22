import pyautogui
import character,tastic,threading, img_manager, posi_manager, pdocr_api
from unit import *
from timer_module import Timer
from interaction_background import Interaction_BGD
from base_threading import Base_Threading
from character import Character

E_STRICT_MODE=True # may cause more performance overhead
def stop_func_example():#True:stop;False:continue
    return False

class Tastic_Operator(Base_Threading):
    def __init__(self):
        super().__init__()
        self.setName('Tastic_Operator')
        self.hp_charalist_green=[34,215,150,255]#BGR
        self.hp_charalist_red=[102,102,255,255]#BGR
        self.hp_charalist_posi=[[283,1698],[379,1698],[475,1698],[571,1698]]
        self.chara_num=4
        self.enter_timer=Timer()
        self.itt=Interaction_BGD()
        
        self.formered_tastic = None
        self.tastic_group = None
        self.character = None
    
    def run(self):
        while(1):
            time.sleep(0.2)
            if self.stop_threading_flag:
                return 0
            
            if self.pause_threading_flag:
                if self.working_flag == True:
                    self.working_flag = False
                time.sleep(1)
                continue
            
            # print('5')
            
            self.working_flag = True
            if self.formered_tastic == None:
                self.working_flag = False
                continue
            self.execute_tastic(self.formered_tastic)
            self.working_flag = False
            time.sleep(0.1)
            
            
    def set_parameter(self,tastic_group:str,character:Character):
        self.tastic_group = tastic_group
        self.character = character
        self.formered_tastic = self._tastic_group_former()
        self.enter_timer.reset()
                
            
            
    def _tastic_group_former(self):
        tastic = self.tastic_group.split(';')
        return tastic
    
    def is_E_available(self): # 被击飞时不可用
        cap = self.itt.capture(posi=posi_manager.posi_chara_smaller_e,jpgmode=2)
        if cap.max()<10:
            return False
        else:
            return True
    
    def _is_E_release(self):
        cap = self.itt.capture(posi=posi_manager.posi_chara_e)
        cap = self.itt.png2jpg(cap,channel='ui',alpha_num=100)
        ret = pdocr_api.ocr.is_img_num_plus(cap)
        
        if ret[0]!=False:
            return True
        else:
            cap = self.itt.capture(posi=posi_manager.posi_chara_e)
            cap = self.itt.png2jpg(cap,channel='ui',alpha_num=100)
            ret = pdocr_api.ocr.is_img_num_plus(cap)
            if ret[0]!=False:
                return True
            else:
                return False
    
    def unconventionality_situlation_detection(self, autoDispose = True): # unconventionality situlation detection
        # situlation 1: coming_out_by_space
        
        situlation_code=-1
        
        while self.itt.get_img_existence(img_manager.COMING_OUT_BY_SPACE, jpgmode=2, min_rate=0.8):
            if self.checkup_stop_func():
                return 0
            situlation_code=1
            self.itt.keyPress('spacebar')
            logger.debug('Unconventionality Situlation: COMING_OUT_BY_SPACE')
            time.sleep(0.1)

        return situlation_code
        
    def chara_waiting(self,mode=0):
        self.unconventionality_situlation_detection()
        if (mode==0) and (self.is_E_available() == True) and (self.enter_timer.getDiffTime() <= 1):
            logger.debug('skip waiting')
            return 0
        while self.get_character_busy() and (not self.checkup_stop_func()):
            if self.checkup_stop_func():
                logger.debug('chara_waiting stop')
                return 0
            logger.debug('waiting  ')
            self.itt.delay(0.1)
    
    
        
    def get_current_chara_num(self):
        cap=self.itt.capture(jpgmode=2)
        for i in range(4):
            if self.checkup_stop_func():
                return 0
            p=posi_manager.chara_num_list_point[i]
            
            if min(cap[p[0],p[1]])>240:
                continue
            else:
                return i+1
            
    
    def QEtactic_1(self,s,n): # not using
        s = s[n:]
        s = s.split(':')
        return s
    
    def get_character_busy(self):
        cap = self.itt.capture()
        cap = self.itt.png2jpg(cap, channel='ui')
        t=0
        for i in range(self.chara_num):
            if self.checkup_stop_func():
                return 0
            p=posi_manager.chara_head_list_point[i]
            if cap[p[0],p[1]][0]>0 and cap[p[0],p[1]][1]>0 and cap[p[0],p[1]][2]>0:
                t+=1
        if t>=3:
            return False
        else:
            return True
        
    
    
    
    def do_attack(self):
        self.chara_waiting()
        self.itt.leftClick()
        self.itt.delay(0.1)

    def do_down_attack(self):
        self.itt.leftClick()
        self.itt.delay(0.1)

    def do_use_e(self,times=0):
        if self.checkup_stop_func():
            return 0
        if times>=2:
            return -1
        
        if self.character.Ecd_float_time>0:
            if self._is_E_release()==True:
                self.itt.delay(self.character.get_Ecd_time()+0.1)
        
        self.chara_waiting()
        logger.debug('do_use_e')
        self.itt.keyPress('e')
        self.itt.delay(0.2)
        if self._is_E_release()==False and E_STRICT_MODE:
            self.do_use_e(times=times+1)
        self.character.used_E()
        
        
    def do_use_longe(self,times=0):
        if self.checkup_stop_func():
            return 0
        if times>=2:
            return -1
        
        if self.character.Ecd_float_time>0:
            self.itt.delay(self.character.get_Ecd_time()+0.1)
                
        self.chara_waiting()
        pyautogui.click(button='middle')
        logger.debug('do_use_longe')
        self.itt.keyPress('s')
        self.itt.keyDown('e')
        self.itt.delay(self.character.Epress_time)
        self.itt.keyUp('e')
        if self.checkup_stop_func():
            return 0
        self.itt.keyPress('w')
        self.itt.delay(0.2)
        if self._is_E_release()==False and E_STRICT_MODE:
            self.do_use_longe(times=times+1)
        self.character.used_longE()
        
    def do_use_q(self,times=0):
        if self.checkup_stop_func():
            return 0
        if times>=2:
            return -1
        
        self.chara_waiting()
        self.itt.keyPress('q')
        self.itt.delay(0.2)
        self.chara_waiting()
        if self.is_Q_ready()==True and E_STRICT_MODE:
            logger.debug('没q到')
            self.do_use_q(times=times+1)
        self.character.used_Q()
    
    def do_long_attack(self):
        if self.checkup_stop_func():
            return 0
        self.chara_waiting(mode=1)
        self.itt.leftDown()
        self.itt.delay(2.5)
        self.itt.leftUp()
    
    def do_jump(self):
        self.chara_waiting(mode=1)
        self.itt.keyPress('spacebar')
        
    def do_jump_attack(self):
        self.chara_waiting(mode=1)
        self.itt.keyPress('spacebar')
        self.itt.delay(0.3)
        self.itt.leftClick()
    
    def do_sprint(self):
        self.itt.rightClick()
    
    def do_aim(self):
        if self.checkup_stop_func():
            return 0
        self.chara_waiting(mode=1)
        self.itt.keyPress('r')
    
    def do_unaim(self):
        if self.checkup_stop_func():
            return 0
        self.itt.keyPress('r')
    
    def is_Q_ready(self):
        cap = self.itt.capture(jpgmode=2)
        p=posi_manager.posi_chara_q_point
        if cap[p[0],p[1]].max()>0:
            return True
        else:
            return False
    
    def estimate_e_ready(self,tastic):
        is_ready = self.character.is_E_ready()
        tas = tastic[tastic.index('?')+1:]
        tas = tas.split(':')
        if is_ready:
            self.execute_tastic([tas[0].replace('.',',')])
        else:
            self.execute_tastic([tas[1].replace('.',',')])
            
    def estimate_q_ready(self,tastic):
        is_ready = self.is_Q_ready()
        tas = tastic[tastic.index('?')+1:]
        tas = tas.split(':')
        if is_ready:
            self.execute_tastic([tas[0].replace('.',',')])
        else:
            self.execute_tastic([tas[1].replace('.',',')])
    
    def estimate_lock_e_ready(self,tastic): # #@e?
        is_ready = not self.character.is_E_pass()
        tas = tastic[4:]
        tas = tas.split(':')
        if is_ready:
            tas[0].replace('.',',')
            while (not self.character.is_E_pass()) and (not self.checkup_stop_func()):
                if self.checkup_stop_func():
                    return 0
                self.unconventionality_situlation_detection()
                self.execute_tastic([tas[0]])
        else:
            tas[1].replace('.',',')
            self.execute_tastic([tas[1]])
            
    def estimate_lock_q_ready(self,tastic): # #@q?
        is_ready = not self.character.is_Q_pass()
        tas = tastic[4:]
        tas = tas.split(':')
        if is_ready:
            tas[0].replace('.',',')
            if self.checkup_stop_func():
                logger.debug('lock stop')
            while (not self.character.is_Q_pass()) and (not self.checkup_stop_func()):
                if self.checkup_stop_func():
                    return 0
                self.unconventionality_situlation_detection()
                self.execute_tastic([tas[0]])
        else:
            tas[1].replace('.',',')
            self.execute_tastic([tas[1]])
    
    def execute_tastic(self,tastic_list):
        
        self.unconventionality_situlation_detection()
        
        for tastic in tastic_list:
            if self.checkup_stop_func():
                return 0
            tastic = tastic.split(',')
            for tas in tastic:
                if self.checkup_stop_func():
                    return 0
                if tas == 'a':
                    self.do_attack()
                elif tas == 'da':
                    self.do_down_attack()
                elif tas == 'q':
                    self.do_use_q()
                elif tas == 'e':
                    self.do_use_e()
                elif tas == 'e~':
                    self.do_use_longe()
                elif tas == 'a~':
                    self.do_long_attack()
                elif tas == 'j':
                    self.do_jump()
                elif tas == 'ja':
                    self.do_jump_attack()
                elif tas == 'sp':
                    self.do_sprint()
                elif tas == 'r':
                    self.do_aim()
                elif tas == 'rr':
                    self.do_unaim()
                elif isint(tas):
                    self.itt.delay(int(tas)/1000)
                elif tas == '>':
                    break
                    
                if '?' in tas:
                    tas1=tas[0:tas.index('?')+1]    
                    if tas1 =='e?':
                        self.estimate_e_ready(tas)
                    elif tas1 == '#@e?':
                        self.estimate_lock_e_ready(tas)
                    elif tas1 == 'q?':
                        self.estimate_q_ready(tas)
                    elif tas1 == '#@q?':
                        self.estimate_lock_q_ready(tas)
                        
if __name__=='__main__':
    import combat_loop
    to=Tastic_Operator()
    chara=combat_loop.get_chara_list()[1]
    to.set_parameter(chara.tastic_group,chara)
    # to.setDaemon(True)
    to.start()