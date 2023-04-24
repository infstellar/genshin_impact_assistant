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

fcap = cv2.VideoCapture(r'F:/videos/video1.mp4')
genshin_map.init_position(tuple([5040, 1384]))
genshin_map.small_map_init_flag = True

success, frame = fcap.read()
cc.set_cap(frame)
pn = input("input your path name")
prc = PathRecorderController()
prc.flow_connector.path_name = pn
prc.start()
logger.info(f"Load over.")
logger.info(f"ready to start.")

while success:
    success, frame = fcap.read()
    cc.set_cap(frame)
    # do something in here
    cv2.imshow('video',frame)
    # print()
    if ui_control.verify_page(UIPage.page_main):
        pass
        # print(genshin_map.get_position(), genshin_map.position_similarity)
    cv2.waitKey(1)
    # print()
    