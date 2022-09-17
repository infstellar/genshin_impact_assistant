from socket import errorTab
from character import Character
import time

#from interaction import *
from interaction_background import Interaction_BGD
def stop_func_example():#True:continue;False:stop
    return True


class Tastic():
    def __init__(self):
        self.hp_charalist_green=[34,215,150,255]#BGR
        self.hp_charalist_red=[102,102,255,255]#BGR
        self.hp_charalist_posi=[[283,1698],[379,1698],[475,1698],[571,1698]]
        self.chara_num=4
        self.itt=Interaction_BGD()
      
    def _tastic_group_former(self):
        tastic = self.tastic_group.split(';')
        return tastic
    
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
        self.execute_tastic(a)
    
    def do_attack(self):
        while self.get_character_busy():
            time.sleep(0.1)
        #print('press a')
        self.itt.leftClick()
        time.sleep(0.2)
        
    def do_use_e(self):
        while self.get_character_busy():
            time.sleep(0.1)
        print('press e')
        self.itt.keyPress('e')
        self.character.used_E()
        #time.sleep(1)
        time.sleep(0.2)
        
        
    def do_use_longe(self):
        while self.get_character_busy():
            time.sleep(0.1)
        print('press long e')
        self.itt.keyDown('e')
        self.itt.delay(2)
        self.itt.keyUp('e')
        self.character.used_longE()
        time.sleep(0.5)
        
    def do_use_q(self):
        while self.get_character_busy():
            time.sleep(0.1)
        self.itt.keyDown('q')
        time.sleep(0.2)
    
    def do_long_a(self):
        self.itt.leftDown()
        time.sleep(2)
        self.itt.leftUp
    
    def do_jump(self):
        self.itt.keyPress('space')
        
    def do_jump_attack(self):
        self.itt.keyPress('space')
        time.sleep(0.3)
        self.itt.leftClick()
    
    def do_sprint(self):
        self.itt.rightClick()
    
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
                    self.do_long_a()
                elif tas == 'j':
                    self.do_jump()
                elif tas == 'ja':
                    self.do_jump_attack()
                    
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
        a=tastic.get_character_busy()       
        print(tastic.get_character_busy())
        time.sleep(0.2)
    print()
                    
                
                
                    