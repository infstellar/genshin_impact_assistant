from source.util import *
from source.assets.ley_line_outcrop import *
from source.task.ley_line_outcrop.util import *
from source.mission.mission_template import MissionExecutor, EXCEPTION_RAISE
from source.task.task_template import TaskTemplate
from source.map.position.position import *
from source.funclib import movement
from source.funclib.generic_lib import f_recognition
from source.funclib.collector_lib import load_items_position



class LeyLineOutcropMission(MissionExecutor):
    """这个类以MissionExecutor的方式执行任务，因为Mission中已有许多适合该任务的函数可以直接调用。
        （如果你愿意，可以将这个类修改为符合自定义任务规范的格式，打包成自定义任务（当然没有必要））

    Args:
        MissionExecutor (_type_): _description_

    Returns:
        _type_: _description_
    """
    TRAVERSE_MONDSTADT_POSITION=[TianLiPosition([783.450352, -6943.497652]),
                                 TianLiPosition([2489.331552, -6101.094052]),
                                 TianLiPosition([3101.988752, -6431.458452]),
                                 TianLiPosition([2860.607952, -5526.280452]),
                                 TianLiPosition([2289.885552, -5515.029652]),
                                 TianLiPosition([1698.707152, -5273.648852]),
                                 TianLiPosition([2224.426352, -4798.046852]),
                                 TianLiPosition([2156.921552, -3923.552852]),
                                 TianLiPosition([2423.872352, -3427.494852]),
                                 TianLiPosition([3367.916752, -4196.640452]),
                                 TianLiPosition([3328.027552, -5106.932452]),
                                 TianLiPosition([3328.027552, -5106.932452])]
    def __init__(self):
        super().__init__(is_TMCF=True, is_CFCF=True, is_PUO=True)
        self.setName("LeyLineOutcropMission")
        self.collection_times = GIAconfig.LeyLineOutcrop_CollectionTimes
        self.type = GIAconfig.LeyLineOutcrop_BlossomType
        self.target_posi = None

    def traverse_mondstant(self):
        """
        遍历蒙德，获得地脉衍出的位置。
        Returns: TianLi坐标

        """
        ui_control.ensure_page(UIPage.page_bigmap)
        for posi in self.TRAVERSE_MONDSTADT_POSITION:
            genshin_map.get_bigmap_posi()
            cap_posi = [220,240,1920-200,1080-150]
            img = itt.capture(jpgmode=NORMAL_CHANNELS)
            img = crop(img, cap_posi)
            img = recorp(img,cap_posi)
            if self.type == "Wealth":
                template_img = IconLeyLineOutcropBlossomOfWealth.image
            elif self.type == "Revelation":
                template_img = IconLeyLindOutcropBlossomOfRevelation.image
            positions = match_multiple_img(img, template=template_img)
            if len(positions)>0:
                curr_posi = genshin_map.get_bigmap_posi()
                posi = positions[0]
                if self.type == "Wealth":
                    target_px_posi = np.array(list(posi))+np.array([17,17])
                elif self.type == "Revelation":
                    target_px_posi = np.array(list(posi))+np.array([20,19])
                delta_posi = genshin_map.convert_InGenshinMapPX_to_GIMAP(target_px_posi-np.array([SCREEN_CENTER_X,SCREEN_CENTER_Y]))
                target_gimap_posi = curr_posi.gimap + delta_posi
                target_tianli_posi = GIMAPPosition(target_gimap_posi).tianli
                return target_tianli_posi
            genshin_map.get_bigmap_posi()
            genshin_map._move_bigmap(posi.tianli, force_center = True)
    
    def touch_the_ley_line_blossom(self):
        """
        识别宝箱图片，接近并领取地脉之花。
        Returns:是否成功。

        """
        if not itt.get_img_existence(IconLeyLineOutcropReward):
            movement.move_to_position(list(self.target_posi), stop_func=self.checkup_stop_func)
        while 1:
            if self.checkup_stop_func():
                itt.key_up('w')
                return
            cap = itt.capture(jpgmode=NORMAL_CHANNELS)
            dist = movement.view_to_imgicon(cap, IconLeyLineOutcropReward)
            
            if dist<15:
                itt.key_down('w')
            else:
                itt.key_up('w')
            if f_recognition():
                itt.key_up('w')
                itt.delay("2animation")
                if "接触地脉之花" in self.PUO.get_pickup_item_names(extra_white=True):
                    itt.key_up('w')
                    return True
                else:
                    self.PUO.pickup_recognize()
            
    
    def exec_mission(self):
        for i in range(self.collection_times):
            try:
                self.target_posi = self.traverse_mondstant() # 获得坐标
                # 从数据库获得所有地脉衍出坐标，如果当前坐标与数据库坐标差值小于阈值，使用数据库坐标修正。
                ley_line_opt_position = load_items_position(marker_title="地脉衍出", ret_mode=1, match_mode=1)
                distances = euclidean_distance_plist(self.target_posi, ley_line_opt_position)
                logger.debug(f"min distances: {min(distances)}")
                min_index = np.argmin(distances)
                if min(distances) >= 30:
                    logger.info(t2t('redirect to the nearest ley line outcrop position fail.'))
                else:
                    self.target_posi = ley_line_opt_position[min_index]
                    logger.info(t2t('redirect to the nearest ley line outcrop position succ: ')+
                                f"{self.target_posi}")
                # 移动到位置
                r = self.move(MODE='AUTO', stop_rule=STOP_RULE_ARRIVE, target_posi=list(self.target_posi), is_tp=True, is_precise_arrival=False)
                self.handle_tmf_stuck_then_raise(r)
                while 1:
                    self.circle_search(self.target_posi)
                    itt.delay(0.6)
                    if f_recognition():
                        itt.key_press('f')
                        break
                # self.collect(is_combat=True)
                # 开打
                self.start_combat()
                while 1:
                    time.sleep(1)
                    if itt.get_img_existence(IconGeneralChallengeSuccess):break
                    if self.checkup_stop_func():break
                self.stop_combat()
                r = self.touch_the_ley_line_blossom()
                if r:
                    itt.key_press('f')
                itt.delay("2animation")
                while 1:
                    if self.checkup_stop_func():return
                    if ui_control.verify_page(UIPage.page_main):
                        break
                    itt.appear_then_click(ButtonGeneralUseOriginResin)
            except HandleExceptionInMission as e:
                logger.error(t2t("HandleExceptionInMission")+f": {e}")
                logger.error(str(e))
        
class LeyLineOutcropTask(TaskTemplate):
    """这个类将一个MissionExecutor类套壳成为TaskTemplate类。

    Args:
        TaskTemplate (_type_): _description_
    """
    def __init__(self):
        super().__init__()
        self.LLOM = LeyLineOutcropMission()
        self._add_sub_threading(self.LLOM, start=False)
    
    def task_run(self):
        # 阻塞式执行子线程。
        self.blocking_startup(self.LLOM)
        
if __name__ == '__main__':
    # llom = LeyLineOutcropMission()
    # r = llom.touch_the_ley_line_blossom() # 3800 -6790 [ 3817.3453 -6775.5386]
    # print(r)
    llot = LeyLineOutcropTask()
    llot.start()
    while 1: time.sleep(1)