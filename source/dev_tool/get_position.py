from source.map.map import genshin_map
from source.util import *

genshin_map.reinit_smallmap()
while 1:
    time.sleep(0.5)
    print(genshin_map.get_position())