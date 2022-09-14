from tastic import Tastic
from character import Character
import time

ss='e;#@e?a:q;'
a = Tastic(ss,Character('test name','test posi',18,4,1,ss))
for i in range(10):
    a.run()
    time.sleep(1)

#print(ss[0:2])