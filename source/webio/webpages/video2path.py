from source.common.base_threading import FunctionThreading
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
    INPUT_VIDEO_SIZE = 'VIDEO_SIZE'
    SCOPE_PREVIEW_IMG = 'PREVIEW_IMG'
    SCOPE_LOG = 'log_scope'
    SCOPE_LOG_AREA = 'LogArea'
    SCOPE_PR_STATE = "PR_STATE"
    SCOPE_FPS_STATE = "FPS_STATE"
    PROCESSBAR_VIDEO = "PROCESSBAR_VIDEO"
    
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
        self.video_t = None
        self.play_video_flag = False
        self.pause_video_flag = False
        self.prc_flag = False
        self.first_enter_flag = True
        self.start_stop_prc_flag = False
    
    def _onclick_load_video(self):
        if self._validate_file_path(pin.pin[self.INPUT_VIDEO_PATH]):
            self._load_video()
        else:
            output.popup(t2t("Path does not exist!"))
        
    def _onclick_play_video(self):
        self._play_video()
    
    def _onclick_cancel_video(self):
        self._show_log('还没写')
        # self._cancel_video()
        
    def _onclick_analyze_position(self):
        self._show_log(t2t("Please waiting..."))
        self.analyze_position()
    
    def _onclick_show_result(self):
        index = int(pin.pin[self.INPUT_INIT_POSITION_ID])
        img = cv2.cvtColor(genshin_map.get_img_near_posi(itt.capture(), self.analysis_result[index].position), cv2.COLOR_BGR2RGB)
        
        output.clear_scope(self.SCOPE_PREVIEW_IMG)
        output.put_image(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).convert('RGB'), title='preview', scope=self.SCOPE_PREVIEW_IMG)
    
    def _pause_video(self, print_log = True):
        self.pause_video_flag = True
        if print_log:
            self._show_log(t2t('press any key in GIA PathToVideo window to continue.'))
    
    def _onclick_confirm_result(self):
        index = int(pin.pin[self.INPUT_INIT_POSITION_ID])
        genshin_map.init_position(self.analysis_result[index].position)
        self._show_log(f"init position set to {self.analysis_result[index].position}")
        self._pause_video()
    
    def _onclick_start_stop_prc(self):
        if not self.prc_flag:
            output.toast(t2t("Path Recorder start!"))
        else:
            output.toast(t2t("Path Recorder stop!"))
        self.prc_flag = not self.prc_flag
        self.start_stop_prc()
    
    def _validate_file_path(self, x):
        return os.path.exists(x)

            
    
    def _load(self):
        # put buttons
        output.popup(t2t("警告：您已经切换到开发模式页面，所有主页功能均不可用。如需使用，请重启程序。"))
        self._load_modules()
        logger.warning(t2t("DEV MODE ENABLED."))
        
        with output.use_scope(self.main_scope):
            output.put_collapse(
                title=t2t("Tutorial"),
                content=[output.put_markdown(t2t(
                "## 食用教程：\n"
                "1. 输入视频路径\n"
                "2. 加载视频\n"
                "3. 加载完成后点击播放视频\n"
                "4. 等待视频播放到你要开始记录的位置时，(暂停)点击分析坐标按钮\n"
                "5. 等待分析完成，日志区将显示可能的坐标id，坐标位置，区域，名称，匹配度， 选择你认为可能的**坐标id**输入初始化坐标输入框\n"
                "6. 点击预览初始坐标按钮，将显示该坐标的区域预览图\n"
                "7. 重复5-6步骤，确认无误后，点击确认初始坐标按钮\n"
                "8. 点击启停路径记录器按钮，开始记录\n"
                "9. 等待视频播放到你要结束记录的位置时， 点击启停路径记录器按钮，停止记录\n"
                "10. 重复4-9步骤，直到完成。\n"
                "11. TLPP文件将储存在dev_assets/tlpp目录下\n"
                "## 快捷键\n"
                "快捷键只能在GIA VideoToPath窗口使用\n"
                "|快捷键|用法|\n"
                "|----|----|\n"
                "| 空格 | 暂停/播放 |\n"
                "| `,` | 减小播放速度,记录路径时必须为现实速度 |\n"
                "| `.` | 增大播放速度,记录路径时必须为现实速度 |\n"
                "| `[` | 启动/停止记录 |\n"
                "| `a` | 分析初始坐标 |\n"
                "## 注意\n"
                "**必须在加载视频前填写所有参数！(除初始坐标id外)**\n"

                ))]
                )
            
            output.put_row(
                [
                    output.put_scope(name=self.SCOPE_PREVIEW_IMG),
                    output.put_scope(name=self.SCOPE_LOG)
                ], size='auto'
            )
            
            output.put_processbar(self.PROCESSBAR_VIDEO, init=0)
            
            output.put_row(
                [
                    output.put_scope(name=self.SCOPE_FPS_STATE),
                    output.put_scope(name=self.SCOPE_PR_STATE)
                ], size='auto'
            )
            
            output.put_row(
                [
                    output.put_column([
                        output.put_button(t2t('load/reload video'), onclick=self._onclick_load_video),
                        output.put_button(t2t('Play video'), onclick=self._onclick_play_video),
                        output.put_button(t2t('Analyze init position'), onclick=self._onclick_analyze_position),
                        output.put_button(t2t('Preview init position'), onclick=self._onclick_show_result),
                        output.put_button(t2t('Confirm init position'), onclick=self._onclick_confirm_result),
                        output.put_button(t2t('Start/Stop path recorder'), onclick=self._onclick_start_stop_prc),
                        output.put_button(t2t('Cancel video'), onclick=self._onclick_cancel_video)
                    ], size='auto'),
                    output.put_column([
                        pin.put_input(self.INPUT_VIDEO_PATH, label=t2t("Video path")),
                        pin.put_input(self.INPUT_INIT_POSITION_ID, label=t2t("init position id")),
                        pin.put_input(self.INPUT_PATH_FILE_HEAD_NAME, label=t2t("File head name")),
                        pin.put_select(self.INPUT_IS_PICKUP_MODE,[{"label": 'True', "value": True}, {"label": 'False', "value": False}], value=True,label=t2t('is pickup mode')),
                        pin.put_input(self.INPUT_COLL_NAME, label=t2t("Collection name")),
                        pin.put_input(self.INPUT_FRAME_TO_START, label=t2t("Frame to start"), type=input.NUMBER, value=0),
                        pin.put_input(self.INPUT_COLL_AREA, label=t2t("Collect area"), value='Liyue|Mondstadt|Inazuma'),
                        pin.put_input(self.INPUT_VIDEO_SIZE, label=t2t("Video size"), value='1280x720')
                    ], size='auto')
                ]
            )
            
        output.put_scrollable(output.put_scope(self.SCOPE_LOG_AREA), height=200, keep_bottom=True, scope=self.SCOPE_LOG)   

    
    def _show_log(self,x):
        output.put_text(x, scope=self.SCOPE_LOG_AREA)
        logger.info(x)
         
    def _load_video(self):
        self.PRF = PathRecorderController()
        self.PRF.flow_connector.path_name = pin.pin[self.INPUT_PATH_FILE_HEAD_NAME]
        self.PRF.flow_connector.is_pickup_mode = bool(pin.pin[self.INPUT_IS_PICKUP_MODE])
        self.PRF.flow_connector.coll_name = pin.pin[self.INPUT_PATH_FILE_HEAD_NAME]
        self.frame_index = int(pin.pin[self.INPUT_FRAME_TO_START])
        self.target_fps = 30
        
        self.fcap = cv2.VideoCapture(pin.pin[self.INPUT_VIDEO_PATH])
        self.fcap.set(cv2.CAP_PROP_POS_FRAMES, pin.pin[self.INPUT_FRAME_TO_START])
        self.total_frames = self.fcap.get(cv2.CAP_PROP_FRAME_COUNT)
        try:
            success, frame = self.fcap.read()
        except Exception as e:
            logger.exception(e)
        if not success:
            self._show_log(t2t("Video is not available"))
            logger.error(f"Video is not available")
        CC.set_cap(frame)
        genshin_map.init_position(tuple(genshin_map.convert_cvAutoTrack_to_GIMAP([1170.8503, -3181.4194])))
        genshin_map.small_map_init_flag = True
        self._show_log(t2t("Load over."))
        self._show_log(t2t("ready to start."))
        
        # cv2.imshow('GIA VideoToPath',frame)
        
        return CC.capture()
    
    def _play_video(self):
        self.play_video_flag = True
        
        # self.video_t = FunctionThreading(self.run_once)
        # self.video_t.start()
    
    def _cancel_video(self):
        self.play_video_flag = False
        # self.video_t.stop_threading()
    
    def analyze_position(self):
        self._pause_video(print_log=False)
        if not ui_control.verify_page(UIPage.page_main):
            self._show_log(t2t("不在主界面/画质过低/错误的视频大小/不完整的录屏"))
            logger.error(f"不在主界面/画质过低/错误的视频大小/不完整的录屏")
        else:
            self.analysis_result, rdistance = genshin_map.get_smallmap_from_teleporter(area=pin.pin[self.INPUT_COLL_AREA].split('|'))
            iii=0
            self._show_log(t2t("Analysis completion: "))
            for tper in self.analysis_result:
                self._show_log(f"ID {iii} position {tper.position} {tper.name} {tper.region}, d={round(rdistance[iii],2)}")
                iii+=1
            self._show_log(t2t("Please enter the possible ID into `init position id`, then press `Preview init position` button or `Confirm init position` button."))
                
    def pause_video(self):
        self._pause_video()
    
    def start_stop_prc(self):
        self.start_stop_prc_flag = True
    
    def set_init_position(self):
        pass
        # posi = input("please input GIMAP posi")
        # p = genshin_map.convert_GIMAP_to_cvAutoTrack(list(map(int,posi.split(','))))
        # pp = tuple(list(map(int,genshin_map._find_closest_teleporter(p).position)))
        # genshin_map.init_position(pp)
        # logger.info(f"position init as {pp}, press any key to continue.")
        # cv2.waitKey(0)
    
    def run_once(self):
        if self.first_enter_flag:
            cv2.namedWindow('GIA VideoToPath', cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
            width, height = pin.pin[self.INPUT_VIDEO_SIZE].split('x')
            cv2.resizeWindow("GIA VideoToPath", int(width), int(height))
            self.first_enter_flag = False
        if self.pause_video_flag:
            cv2.waitKey(0)
            self.pause_video_flag = False
        success, frame = self.fcap.read()
        CC.set_cap(frame)
        if self.frame_index%10==0:
            pass
        # do something in here
        cv2.imshow('GIA VideoToPath',frame)
        # print()
        if ui_control.verify_page(UIPage.page_main):
            pass
        dt = self.pt.get_diff_time()-(1/self.target_fps)
        t = (dt+(1/self.target_fps))
        if abs(t)<=0.01:
            t=self.target_fps
        curr_fps = round(1/t,2)
        if self.frame_index%12==0:
            output.clear_scope(self.SCOPE_FPS_STATE)
            output.put_text(f"FPS: {min(curr_fps, self.target_fps)}", scope=self.SCOPE_FPS_STATE)
        if dt<-0.001:
            # time.sleep(-dt)
            k = cv2.waitKey(int((-dt)*1000))
        else:
            if self.frame_index%20==0:
                self._show_log(f"FPS low:{round(1/(dt+(1/self.target_fps)),2)}")
            k = cv2.waitKey(1)
        self.pt.reset()
        if k & 0xFF == ord('a'):
            self.analyze_position()
        elif k & 0xFF == ord(' '):
            cv2.waitKey(0)
        elif k & 0xFF == ord('b'):
            self.set_init_position()
        elif k & 0xFF == ord('.'):
            fps+=5
            self._show_log(f"fps set as {fps}")
        elif k & 0xFF == ord(','):
            fps-=5
            if fps <= 0:
                fps = 1
            self._show_log(f"fps set as {fps}")
        elif k & 0xFF == ord(']'):
            self.PRF.pc._start_stop_recording()
            self._show_log(f"press any key to continue.")
            cv2.waitKey(0)
            
        self.frame_index+=1
        if self.start_stop_prc_flag:
            self.PRF.pc._start_stop_recording()
            self.PRF.loop()
            self._show_log(f"press any key to continue.")
            cv2.waitKey(0)
            self.start_stop_prc_flag = False
        if self.frame_index%61==0:
            output.clear_scope(self.SCOPE_PR_STATE)
            if str(self.PRF.pc.rfc) == '2':
                pr_state = 'Running'
            else:
                pr_state = 'Idle'
            output.put_text(f"{t2t('Path Recorder')}: {pr_state}", scope=self.SCOPE_PR_STATE)
        self.PRF.loop()
        if self.frame_index%120==0:
            self._show_log(f"frame: {self.frame_index}")
        if self.frame_index%11==0:
            output.set_processbar(self.PROCESSBAR_VIDEO, self.frame_index/self.total_frames)

    def _load_modules(self):
        from source.funclib.combat_lib import CSDL
        CSDL.pause_threading()
        CSDL.stop_threading()
        itt.capture_obj = CC

    def _event_thread(self):
        while 1:
            if self.play_video_flag:
                self.run_once()
            else:
                time.sleep(0.1)

    