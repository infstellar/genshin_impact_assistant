from source.task.ley_line_outcrop.assets import *
from source.task.ley_line_outcrop.util import *
from source.mission.mission_template import MissionExecutor
from source.task.task_template import TaskTemplate
from source.map.position.position import *
from source.funclib import movement
from source.funclib.generic_lib import f_recognition

BlossomOfWealth=""

class LeyLineOutcropMission(MissionExecutor):
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
                                 TianLiPosition([3328.027552, -5106.932452])]
    def __init__(self):
        super().__init__(is_TMCF=True, is_CFCF=True)

    def traverse_mondstant(self):
        ui_control.ensure_page(UIPage.page_bigmap)
        for posi in self.TRAVERSE_MONDSTADT_POSITION:
            genshin_map.get_bigmap_posi()
            genshin_map._move_bigmap(posi.tianli, force_center = True)
            cap_posi = [220,240,1920-200,1080-150]
            img = itt.capture(jpgmode=0)
            img = crop(img, cap_posi)
            img = recorp(img,cap_posi)
            positions = itt.match_multiple_img(img, template=IconBlossomOfRevelation.image)
            if len(positions)>0:
                curr_posi = genshin_map.get_bigmap_posi()
                posi = positions[0]
                target_px_posi = np.array(list(posi))+np.array([20,19])
                delta_posi = genshin_map.convert_InGenshinMapPX_to_GIMAP(target_px_posi-np.array([SCREEN_CENTER_X,SCREEN_CENTER_Y]))
                target_gimap_posi = curr_posi.gimap + delta_posi
                target_tianli_posi = GIMAPPosition(target_gimap_posi).tianli
                return target_tianli_posi
    
    def touch_the_ley_line_blossom(self):
        while 1:
            if self.checkup_stop_func():
                itt.key_up('w')
                return
            cap = itt.capture(jpgmode=0)
            dist = movement.view_to_imgicon(cap, IconReward)
            if dist<15:
                itt.key_down('w')
            else:
                itt.key_up('w')
            if f_recognition():
                itt.key_up('w')
                return True
            
    
    def exec_mission(self):
        # target_posi = self.traverse_mondstant()
        # self.move(MODE='AUTO', stop_rule=1, target_posi=list(target_posi), is_tp=True)
        # self.collect(is_combat=True)
        r = self.touch_the_ley_line_blossom()
        if r:
            itt.key_press('f')
        itt.delay("2animation")
        while 1:
            if self.checkup_stop_func():return
            if ui_control.verify_page(UIPage.page_main):
                break
            itt.appear_then_click(ButtonUseOriginResin)
        
        
class LeyLineOutcropTask(TaskTemplate):
    def __init__(self):
        super().__init__()
        self.LLOM = LeyLineOutcropMission()
        self._add_sub_threading(self.LLOM, start=False)
        
    def loop(self):
        self.blocking_startup(self.LLOM)
        self.pause_threading()
        
if __name__ == '__main__':
    # llom = LeyLineOutcropMission()
    # r = llom.touch_the_ley_line_blossom() # 3800 -6790 [ 3817.3453 -6775.5386]
    # print(r)
    llot = LeyLineOutcropTask()
    llot.start()
    while 1: time.sleep(1)