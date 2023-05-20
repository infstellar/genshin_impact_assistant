import os, sys
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if sys.path[0] != ROOT_PATH:
    sys.path.insert(0, ROOT_PATH)
from source.util import *
from source.ui.ui import ui_control
from source.ui import page as UIPage
from source.interaction.interaction_core import itt
from source.interaction.capture import CustomCapture
from source.map.map import genshin_map
from source.flow.path_recorder_flow import PathRecorderController
from source.funclib.combat_lib import CSDL
from source.common.timer_module import Timer

CSDL.pause_threading()
CSDL.stop_threading()
cc = CustomCapture()
itt.capture_obj = cc
class VideoNotFoundError(Exception):pass

video_path = r"" # 填写你的视频路径
frameToStart = 0 # 填写视频播放开始帧
pn = "GlazeLily" # 填写TLPP文件名开头
coll_name = "琉璃百合" # 填写采集物名称

fcap = cv2.VideoCapture(video_path)
fcap.set(cv2.CAP_PROP_POS_FRAMES, frameToStart)
try:
    success, frame = fcap.read()
except Exception as e:
    logger.exception(e)
if not success:
    raise VideoNotFoundError(video_path)
cc.set_cap(frame)
genshin_map.init_position(tuple(genshin_map.convert_cvAutoTrack_to_GIMAP([1170.8503, -3181.4194])))
genshin_map.small_map_init_flag = True


PRF = PathRecorderController()
PRF.flow_connector.path_name = pn
PRF.flow_connector.is_pickup_mode = True
PRF.flow_connector.coll_name = coll_name
logger.info(f"Load over.")
logger.info(f"ready to start.")
# press `\` to start
fps = 30
i=frameToStart
pt = Timer()
while success:
    
    success, frame = fcap.read()
    cc.set_cap(frame)
    # do something in here
    cv2.imshow('video',frame)
    # print()
    if ui_control.verify_page(UIPage.page_main):
        pass
        # print(genshin_map.get_position(), genshin_map.position_similarity)
    dt = pt.get_diff_time()-(1/fps)
    if dt<-0.001:
        k = cv2.waitKey(int((-dt)*1000))
    else:
        if i%20==0:
            logger.info(f"fps low:{round(1/(dt+(1/fps)),2)}")
        k = cv2.waitKey(1)
    pt.reset()
    if k & 0xFF == ord(' '):
        cv2.waitKey(0)
    elif k & 0xFF == ord('a'):
        rlist, rd = genshin_map.get_smallmap_from_teleporter(area=['Liyue','Mondstadt'])
        iii=0
        for tper in rlist:
            logger.info(f"id {iii} position {tper.position} {tper.name} {tper.region}, d={rd[iii]}")
            iii+=1
        while 1:
            iii = input("please input id.")
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
        posi = input("please input GIMAP posi")
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
    elif k & 0xFF == ord(']'):
        PRF.pc._start_stop_recording()
        logger.info(f"press any key to continue.")
        cv2.waitKey(0)
        
    i+=1
    PRF.loop()
    if i%120==0:
        logger.info(f"frame: {i}")
    # print()
    