from source.util import *
from source.ui.ui import ui_control
from source.ui import page as UIPage
from source.interaction.interaction_core import itt
from source.interaction.capture import CustomCapture
from source.map.map import genshin_map
from source.flow.path_recorder_flow import PathRecorderController
from source.funclib.combat_lib import CSDL

CSDL.pause_threading()
CSDL.stop_threading()
cc = CustomCapture()
itt.capture_obj = cc

class VideoNotFoundError(Exception):pass

# fcap = cv2.VideoCapture(r'F:/Downkyi/video1.mp4')
fcap = cv2.VideoCapture(r'M:/Downkyi/BV15a411Y7V1.mp4')
frameToStart = 720+240
fcap.set(cv2.CAP_PROP_POS_FRAMES, frameToStart)
success, frame = fcap.read()
if not success:
    raise VideoNotFoundError
cc.set_cap(frame)

genshin_map.init_position(tuple(genshin_map.convert_cvAutoTrack_to_GIMAP([ 1170.8503, -3181.4194])))
genshin_map.small_map_init_flag = True

pn = "V2Ptest11"
prc = PathRecorderController()
prc.flow_connector.path_name = pn
prc.flow_connector.is_pickup_mode = True
prc.start()
logger.info(f"Load over.")
logger.info(f"ready to start.")
# press `\` to start
fps = 30
i=1

while success:
    success, frame = fcap.read()
    cc.set_cap(frame)
    # do something in here
    cv2.imshow('video',frame)
    # print()
    if ui_control.verify_page(UIPage.page_main):
        pass
        # print(genshin_map.get_position(), genshin_map.position_similarity)
    k = cv2.waitKey(int((1/fps)*1000))
    if k & 0xFF == ord(' '):
        cv2.waitKey(0)
    elif k & 0xFF == ord('a'):
        rlist, rd = genshin_map.get_smallmap_from_teleporter(area=['Liyue'])
        iii=0
        for tper in rlist:
            logger.info(f"id {iii} position {tper.position} {tper.name} {tper.region}, d={rd[iii]}")
            iii+=1
        while 1:
            iii = input("pls input id.")
            if iii == '':
                break
            else:
                iii = int(iii)
            cv2.imshow(f'tper{iii}', genshin_map.get_img_near_posi(itt.capture(), rlist[iii].position))
            cv2.waitKey(1)
            genshin_map.init_position(rlist[iii].position)
        logger.info(f"press any key to continue.")
        cv2.waitKey(0)
    elif k & 0xFF == ord('b'):
        posi = input("pls input GIMAP posi")
        p = genshin_map.convert_GIMAP_to_cvAutoTrack(list(map(int,posi.split(','))))
        pp = tuple(list(map(int,genshin_map._find_closest_teleporter(p).position)))
        genshin_map.init_position(pp)
        logger.info(f"position init as {pp}, press any key to continue.")
        cv2.waitKey(0)
    elif k & 0xFF == ord('.'):
        fps+=5
        logger.info(f"fps set as {fps}")
    elif k & 0xFF == ord(','):
        fps-=5
        if fps <= 0:
            fps = 1
        logger.info(f"fps set as {fps}")
        
    i+=1
    prc.loop()
    if i%120==0:
        logger.info(f"frame: {i}")
    # print()
    