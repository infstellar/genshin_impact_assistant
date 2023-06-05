

from source.webio.util import *
from pywebio import *
from source.webio.advance_page import AdvancePage
from source.config.cvars import *
from source.ui.ui import ui_control
from source.ui import page as UIPage
from source.interaction.interaction_core import itt
from source.interaction.capture import CustomCapture
from source.map.map import genshin_map
from source.flow.path_recorder_flow import PathRecorderController
from source.common.timer_module import Timer
CC = CustomCapture()





class VideoToPathPage(AdvancePage):
    INPUT_PATH_FILE_HEAD_NAME = 'INPUT_PATH_FILE_HEAD_NAME'
    INPUT_IS_PICKUP_MODE = 'IS_PICKUP_MODE'
    INPUT_COLL_NAME = 'COLL_NAME'
    INPUT_FRAME_TO_START = 'FRAME_TO_START'
    INPUT_IS_PICKUP_MODE = 'IS_PICKUP_MODE'
    INPUT_VIDEO_PATH = 'VIDEO_PATH'
    INPUT_COLL_AREA = 'COLL_AREA'
    INPUT_INIT_POSITION_ID = 'INIT_POSITION_ID'
    
    
    
    def __init__(self) -> None:
        super().__init__()
        """_summary_

        Args:
            PATH_FILE_HEAD_NAME (_type_): 填写TLPP文件名开头。保存时会以该字符串作为文件名的开头。
            IS_PICKUP_MODE (_type_): 是否为采集路径模式
            COLL_NAME (_type_): 填写采集物名称。务必填写正确的名称，否则生成的TLPP文件中的adsorptive_position可能为空列表。
            VIDEO_PATH (_type_): 填写你的视频路径
            COLL_AREA (_type_): 填写采集区域
            FRAME_TO_START (int, optional): 填写视频播放开始帧，控制台会输出 frame:xxx来提示当前帧. Defaults to 0.
        """
        self.pt = Timer()
    
    def _load(self):
        # put buttons
        output.popup(t2t("警告：您已经切换到开发模式页面，所有主页功能均不可用。如需使用，请重启程序。"))
        self._load_modules()
        logger.warning(t2t("DEV MODE ENABLED."))
        
        with output.use_scope(self.main_scope):
            output.put_row(
                [
                    output.put_column([
                        output.put_button('123', onclick=lambda x:1)
                    ]),
                    output.put_column([
                        pin.put_input(self.INPUT_PATH_FILE_HEAD_NAME, label=t2t("")),
                        pin.put_input(self.INPUT_IS_PICKUP_MODE, label=t2t("")),
                        pin.put_input(self.INPUT_COLL_NAME, label=t2t("")),
                        pin.put_input(self.INPUT_FRAME_TO_START, label=t2t("")),
                        pin.put_input(self.INPUT_VIDEO_PATH, label=t2t("")),
                        pin.put_input(self.INPUT_COLL_AREA, label=t2t(""))
                    ])
                ]
            )
            
            

    
    
         
    def _load_video(self):
        self.PRF.flow_connector.path_name = pin.pin[self.INPUT_PATH_FILE_HEAD_NAME]
        self.PRF.flow_connector.is_pickup_mode = bool(pin.pin[self.INPUT_IS_PICKUP_MODE])
        self.PRF.flow_connector.coll_name = pin.pin[self.INPUT_PATH_FILE_HEAD_NAME]
        self.frame_index = pin.pin[self.INPUT_PATH_FILE_HEAD_NAME]
        self.target_fps = 30
        
        self.fcap = cv2.VideoCapture(pin.pin[self.INPUT_VIDEO_PATH])
        self.fcap.set(cv2.CAP_PROP_POS_FRAMES, pin.pin[self.INPUT_FRAME_TO_START])
        try:
            success, frame = self.fcap.read()
        except Exception as e:
            logger.exception(e)
        if not success:
            logger.error(f"Video is not available")
        CC.set_cap(frame)
        genshin_map.init_position(tuple(genshin_map.convert_cvAutoTrack_to_GIMAP([1170.8503, -3181.4194])))
        genshin_map.small_map_init_flag = True
        logger.info(f"Load over.")
        logger.info(f"ready to start.")
        self.PRF = PathRecorderController()
        return CC.capture()
    
    def analyze_position(self):
        if not ui_control.verify_page(UIPage.page_main):
            logger.error(f"不在主界面/画质过低/错误的视频大小/不完整的录屏")
        else:
            rlist, rd = genshin_map.get_smallmap_from_teleporter(area=self.COLL_AREA)
            iii=0
            for tper in rlist:
                logger.info(f"id {iii} position {tper.position} {tper.name} {tper.region}, d={rd[iii]}")
                iii+=1
            while 1:
                iii = pin.pin[self.INPUT_INIT_POSITION_ID]
                if iii == '':
                    break
                else:
                    iii = int(iii)
                cv2.imshow(f'tper{iii}', genshin_map.get_img_near_posi(itt.capture(), rlist[iii].position))
                cv2.waitKey(1)
                genshin_map.init_position(rlist[iii].position)
            logger.info(f"press any key to continue.")
            cv2.waitKey(0)
    
    def pause_video(self):
        cv2.waitKey(0)
        logger.info(f"press any key to continue.")
    
    def start_stop_prc(self):
        cv2.waitKey(0)
        self.PRF.pc._start_stop_recording()
        logger.info(f"Path Recorder has been started.")
        logger.info(f"press any key to continue.")
    
    def set_init_position(self):
        pass
        # posi = input("please input GIMAP posi")
        # p = genshin_map.convert_GIMAP_to_cvAutoTrack(list(map(int,posi.split(','))))
        # pp = tuple(list(map(int,genshin_map._find_closest_teleporter(p).position)))
        # genshin_map.init_position(pp)
        # logger.info(f"position init as {pp}, press any key to continue.")
        # cv2.waitKey(0)
    
    def run_once(self):
        success, frame = self.fcap.read()
        CC.set_cap(frame)
        # do something in here
        cv2.imshow('GIA VideoToPath',frame)
        # print()
        if ui_control.verify_page(UIPage.page_main):
            pass
        dt = self.pt.get_diff_time()-(1/self.target_fps)
        if dt<-0.001:
            # time.sleep(-dt)
            k = cv2.waitKey(int((-dt)*1000))
        else:
            if self.frame_index%20==0:
                logger.info(f"fps low:{round(1/(dt+(1/self.target_fps)),2)}")
            k = cv2.waitKey(1)
        self.pt.reset()
        if k & 0xFF == ord('a'):
            self.analyze_position()
        elif k & 0xFF == ord('b'):
            self.set_init_position()
        elif k & 0xFF == ord('.'):
            fps+=5
            logger.info(f"fps set as {fps}")
        elif k & 0xFF == ord(','):
            fps-=5
            if fps <= 0:
                fps = 1
            logger.info(f"fps set as {fps}")
        elif k & 0xFF == ord(']'):
            self.PRF.pc._start_stop_recording()
            logger.info(f"press any key to continue.")
            cv2.waitKey(0)
            
        self.frame_index+=1
        self.PRF.loop()
        if self.frame_index%120==0:
            logger.info(f"frame: {i}")

    def _load_modules(self):
        from source.funclib.combat_lib import CSDL
        CSDL.pause_threading()
        CSDL.stop_threading()
        itt.capture_obj = CC

    def _event_thread(self):
        time.sleep(0.1)

    