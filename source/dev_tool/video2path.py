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

fcap = cv2.VideoCapture(r'M:/Downkyi/video2.mp4')
success, frame = fcap.read()
if not success:
    raise VideoNotFoundError
cc.set_cap(frame)

genshin_map.init_position(tuple(genshin_map.convert_cvAutoTrack_to_GIMAP([ 1170.8503, -3181.4194])))
genshin_map.small_map_init_flag = True

pn = "LLDV2P1"
prc = PathRecorderController()
prc.flow_connector.path_name = pn
prc.start()
logger.info(f"Load over.")
logger.info(f"ready to start.")
# press `\` to start
while success:
    success, frame = fcap.read()
    cc.set_cap(frame)
    # do something in here
    cv2.imshow('video',frame)
    # print()
    if ui_control.verify_page(UIPage.page_main):
        pass
        # print(genshin_map.get_position(), genshin_map.position_similarity)
    cv2.waitKey(1/30)
    # print()
    