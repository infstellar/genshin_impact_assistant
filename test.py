from tastic import Tastic
from character import Character
import time

ss='e?e:a;'
a = Tastic(ss,Character('test name','test posi',18,8,1,ss))
a.run()
time.sleep(1)
a.run()
#print(ss[0:2])