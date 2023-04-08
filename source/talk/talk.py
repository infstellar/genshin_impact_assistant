from source.util import *
from source.interaction.interaction_core import itt
from source.manager import asset
from source.talk.assets import *
from source.funclib.generic_lib import f_recognition
from source.ui.ui import ui_control
from source.ui import page as UIPage
from source.api.pdocr_complete import ocr
from source.common.timer_module import AdvanceTimer

class Talk():
    def __init__(self) -> None:
        pass
    
    def _delay6(self):
        itt.delay(0.6)
    
    def talk_skip(self, stop_func):
        while 1:
            time.sleep(0.1)
            if stop_func():return
            itt.move_and_click(ButtonTalkSkip.click_position())
            # itt.move_to(-120,0,relative=True)
            if itt.get_img_existence(asset.ui_main_win): return True
            
    def talk_switch(self, textobj:asset.TextTemplate):
        cap = itt.capture(posi=AreaTalkSelects.position, jpgmode=0)
        cap = recorp(cap,area=AreaTalkSelects.position)
        posi = ocr.get_text_position(cap, textobj.text)
        if posi != -1:
            itt.move_and_click(posi)
    
    def talk_until_switch(self, stop_func=lambda:False):
        while 1:
            time.sleep(0.1)
            if stop_func():return
            if itt.get_img_existence(ButtonTalkSkip, is_log=True):
                logger.info("talk_until_switch succ")
                return True
            else:
                itt.move_and_click(ButtonTalkSkip_Force.click_position())
                # self._delay6()
    
    def talk_with_options(self, options:list):
        for text_obj in options:
            itt.appear_then_click(text_obj)
    
    def find_npc(self):
        if f_recognition():return True
        itt.key_press('w')
        self._delay6()
        if f_recognition():return True
        itt.key_press('a')
        self._delay6()
        if f_recognition():return True
        itt.key_press('s')
        self._delay6()
        if f_recognition():return True
        itt.key_press('d')
        self._delay6()
        if f_recognition():return True
        return False
     
    def talk_with_npc(self,npc_name = None):
        if ui_control.verify_page(UIPage.page_main):
            if self.find_npc():
                itt.key_press('f')
                return True
            return False
        else:
            return True
    
    def exit_talk(self):
        esc_timer = AdvanceTimer(2)
        while 1:
            if ui_control.verify_page(UIPage.page_main): return True
            itt.move_and_click(ButtonTalkSkip.click_position())
            if esc_timer.reached_and_reset():
                itt.key_press('esc')
            itt.delay(0.2)
    
if __name__ == '__main__':
    t = Talk()
    # t.talk_with_npc()
    # t.talk_until_switch()
    # t.talk_switch(Expedition)
    t.exit_talk()