from character import Character
import time

def stop_func_example():#True:continue;False:stop
    return True


class Tastic():
    def __init__(self,tastic_group:str,character:Character,stop_func=stop_func_example):
        self.tastic_group=tastic_group
        self.character = character
        self.stop_func=stop_func
        
    def _tastic_group_former(self):
        tastic = self.tastic_group.split(';')
        return tastic
    
    def QEtactic_1(self,s,n): # not using
        s = s[n:]
        s = s.split(':')
        return s
    
    def run(self):
        a=self._tastic_group_former()
        self.execute_tastic(a)
    
    def do_attack(self):
        print('press a')
        time.sleep(0.2)
        
    def do_use_e(self):
        print('press e')
        self.character.used_E()
        
    def do_use_q(self):
        print('press q')
    
    def estimate_e_ready(self,tastic):
        is_ready = self.character.is_E_ready()
        tas = tastic[tastic.index('?')+1:]
        tas = tas.split(':')
        if is_ready:
            self.execute_tastic([tas[0].replace(',','.')])
        else:
            self.execute_tastic([tas[1].replace(',','.')])
    
    def estimate_lock_e_ready(self,tastic):
        is_ready = not self.character.is_E_pass()
        tas = tastic[4:]
        tas = tas.split(':')
        if is_ready:
            tas[0].replace(',','.')
            while (not self.character.is_E_pass()) and self.stop_func():
                self.execute_tastic([tas[0]])
        else:
            tas[1].replace(',','.')
            self.execute_tastic([tas[1]])
    
    def execute_tastic(self,tastic_list):
        
        for tastic in tastic_list:
            tastic = tastic.split('.')
            for tas in tastic:
                if tas == 'a':
                    self.do_attack()
                if tas == 'q':
                    self.do_use_q()
                if tas == 'e':
                    self.do_use_e()
                if '?' in tas:
                    tas1=tas[0:tas.index('?')+1]    
                    if tas1 =='e?':
                        self.estimate_e_ready(tas)
                    elif tas1 == '#@e?':
                        self.estimate_lock_e_ready(tas)
                        
                
                    
                
                
                    