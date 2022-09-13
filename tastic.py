from character import Character


class Tastic():
    def __init__(self,tastic_group:str,character:Character):
        self.tastic_group=tastic_group
        self.character = character
    def _tastic_group_former(self):
        tastic = self.tastic_group.split(';')
        return tastic
    
    def run(self):
        a=self._tastic_group_former()
        self.execute_tastic(a)
    
    def execute_tastic(self,tastic_list):
        
        for tastic in tastic_list:
            tastic = tastic.split('.')
            for tas in tastic:
                if tas == 'a':
                    print('press a')
                if tas == 'q':
                    print('press q')
                if tas == 'e':
                    print('press e')
                    self.character.used_E()
                
                if tas[0:2] == 'e?':
                    is_ready = self.character.is_E_ready()
                    ta = tas[2:]
                    ta = ta.split(':')
                    if is_ready:
                        ta[0].replace(',','.')
                        self.execute_tastic([ta[0]])
                    else:
                        ta[1].replace(',','.')
                        self.execute_tastic([ta[1]])
                
                
                
                
                    