from socket import errorTab
from timer import Timer
from character import Character
from unit import *
import time, cv2
import posi_manager

#from interaction import *
from interaction_background import Interaction_BGD
def stop_func_example():#True:stop;False:continue
    return False


class Tastic():
    def __init__(self):
        self.hp_charalist_green=[34,215,150,255]#BGR
        self.hp_charalist_red=[102,102,255,255]#BGR
        self.hp_charalist_posi=[[283,1698],[379,1698],[475,1698],[571,1698]]
        self.chara_num=4
        self.enter_timer=Timer()
        self.itt=Interaction_BGD()
      
    def _tastic_group_former(self):
        tastic = self.tastic_group.split(';')
        return tastic
    
    def _is_E_release(self):
        name = self.character.name
        filename='imgs/'+name+'_e.png'
        if os.path.exists(filename):
            #img = cv2.imread(filename)
            mr = self.itt.similar_img(name+'_e.png',posi_manager.posi_chara_e,is_gray=True)
            print('mr= ',mr)
            if mr<=0.94:
                return 1
            else:
                return 0
        else:
            return -1
        
    def _chara_waiting(self,mode=0):
        
        if mode==0 and self._is_E_release() == 0 and self.enter_timer.getDiffTime() <= 1:
            print('skip waiting')
            return 0
        while self.get_character_busy():
            self.itt.delay(0.1)
    
    def QEtactic_1(self,s,n): # not using
        s = s[n:]
        s = s.split(':')
        return s
    
    def get_character_busy(self):
        cap = self.itt.capture()
        
        t=0
        for i in range(self.chara_num):
            
            # print(min( self.itt.color_SD(self.hp_charalist_green, cap[self.hp_charalist_posi[i][0],self.hp_charalist_posi[i][1]] )  ,
            #            self.itt.color_SD(self.hp_charalist_red  , cap[self.hp_charalist_posi[i][0],self.hp_charalist_posi[i][1]] ) ))
            
            if min( self.itt.color_SD(self.hp_charalist_green, cap[self.hp_charalist_posi[i][0],self.hp_charalist_posi[i][1]] )  ,
                    self.itt.color_SD(self.hp_charalist_red  , cap[self.hp_charalist_posi[i][0],self.hp_charalist_posi[i][1]] ) )<=7:
                t+=1
        if t>=3:
            return False
        else:
            # print(min( self.itt.color_SD(self.hp_charalist_green, cap[self.hp_charalist_posi[i][0],self.hp_charalist_posi[i][1]] )  ,
            #         self.itt.color_SD(self.hp_charalist_red  , cap[self.hp_charalist_posi[i][0],self.hp_charalist_posi[i][1]] ) ) )
            print('waiting  ',end=' ')
            return True
        
    
    def run(self,tastic_group:str,character:Character,stop_func=stop_func_example):
        self.tastic_group=tastic_group
        self.character = character
        self.stop_func=stop_func
        a=self._tastic_group_former()
        self.enter_timer.reset()
        self.execute_tastic(a)
    
    def do_attack(self):
        self._chara_waiting()
        #print('press a')
        self.itt.leftClick()
        self.itt.delay(0.2)
        
    def do_use_e(self):
        self._chara_waiting()
        print('press e')
        self.itt.keyPress('e')
        self.character.used_E()
        #self.itt.delay(1)
        self.itt.delay(0.2)
        
        
    def do_use_longe(self):
        self._chara_waiting()
        print('press long e')
        self.itt.keyDown('e')
        self.itt.delay(2)
        self.itt.keyUp('e')
        self.character.used_longE()
        self.itt.delay(0.5)
        
    def do_use_q(self):
        self._chara_waiting()
        self.itt.keyPress('q')
        self.itt.delay(0.2)
    
    def do_long_attack(self):
        self._chara_waiting(mode=1)
        self.itt.leftDown()
        self.itt.delay(2.5)
        self.itt.leftUp()
    
    def do_jump(self):
        self.itt.keyPress('spacebar')
        
    def do_jump_attack(self):
        self.itt.keyPress('spacebar')
        self.itt.delay(0.3)
        self._chara_waiting(mode=1)
        self.itt.leftClick()
    
    def do_sprint(self):
        self.itt.rightClick()
    
    def do_aim(self):
        self._chara_waiting(mode=1)
        self.itt.keyPress('r')
    
    def do_unaim(self):
        self.itt.keyPress('r')
    
    def estimate_e_ready(self,tastic):
        is_ready = self.character.is_E_ready()
        tas = tastic[tastic.index('?')+1:]
        tas = tas.split(':')
        if is_ready:
            self.execute_tastic([tas[0].replace('.',',')])
        else:
            self.execute_tastic([tas[1].replace('.',',')])
            
    def estimate_q_ready(self,tastic):
        is_ready = self.character.is_Q_ready()
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
            if self.stop_func():
                print('lock stop')
            while (not self.character.is_E_pass()) and (not self.stop_func()):
                self.execute_tastic([tas[0]])
        else:
            tas[1].replace('.',',')
            self.execute_tastic([tas[1]])
    
    def execute_tastic(self,tastic_list):
        
        for tastic in tastic_list:
            tastic = tastic.split(',')
            for tas in tastic:
                if tas == 'a':
                    self.do_attack()
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
                    
                    
                        
if __name__=='__main__':
    tastic=Tastic()
    while(1):
        tastic.do_long_attack()
        time.sleep(5)
    print()
                    
                
                
                    