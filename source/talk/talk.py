from source.util import *
from source.interaction.interaction_core import itt
from source.manager import asset
from source.talk.assets import *
from source.funclib.generic_lib import f_recognition
from source.ui.ui import ui_control
from source.ui import page as UIPage
from source.api.pdocr_complete import ocr
from source.common.timer_module import AdvanceTimer
from source.pickup.util import get_all_colls_name, pickup_specific_item

class Talk():
    def __init__(self) -> None:
        pass
    
    def _delay6(self):
        logger.debug(f"Talk: delay 0.6")
        itt.delay(0.6)
    
    def _is_in_talking(self) -> bool:
        """Detect whether in a conversation.

        Returns:
            bool: whether in a conversation.
        """
        return itt.get_img_existence(IconTalkTalking1) or itt.get_img_existence(IconTalkTalking2) or itt.get_img_existence(ButtonTalkSkip)
    
    def talk_wait(self, x):
        logger.debug(f"Talk: wait {x}")
        itt.delay(x)
    
    def talk_skip(self, stop_func):
        logger.info(f"Talk: Skip")
        while 1:
            time.sleep(0.1)
            if stop_func():return
            itt.move_and_click(ButtonTalkSkip.click_position())
            # itt.move_to(-120,0,relative=True)
            if itt.get_img_existence(IconUIEmergencyFood): return True
            
    def talk_switch(self, textobj:asset.Text) -> bool:
        logger.info(f"Talk: Switch: {textobj.text}")
        cap = itt.capture(posi=AreaTalkSelects.position, jpgmode=0)
        cap = recorp(cap,area=AreaTalkSelects.position)
        posi = ocr.get_text_position(cap, textobj.text)
        if posi != -1:
            itt.move_and_click(posi)
            return True
        else:
            logger.warning(f"Cannot Find Text: {textobj.text}")
            return False
    
    def talk_until_switch(self, stop_func=lambda:False):
        logger.info(f"Talk: Until Switch")
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
        logger.info(f"Finding NPC")
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
        logger.warning(f"Find NPC Fail")
        return False
    
    def talk_with_npc(self, npc_name:asset.Text = None) -> bool:
        if ui_control.verify_page(UIPage.page_main):
            for move_key in ['w','a','s','d']:
                itt.key_press(move_key)
                itt.delay("2animation")
                if not f_recognition(): continue
                if npc_name is None:
                    itt.key_press('f')
                    logger.info("Talk with npc succ.")
                    return True
                logger.info(f"Talk: with NPC: {npc_name.text}")
                npc_names = get_all_colls_name()
                flag1 = False
                for i in npc_names:
                    if npc_name.text in i: flag1 = True
                if flag1:
                    pickup_specific_item(npc_name.text)
                    logger.info("Talk with npc succ.")
                    return True
            if npc_name != None:
                logger.warning(f"Cannot find NPC: {npc_name.text}")
            return False
        else:
            logger.warning(f"Cannot find any NPC")
            return False
    
    def exit_talk(self) -> bool:
        logger.info(f"Talk: Exit")
        esc_timer = AdvanceTimer(2).start()
        while 1:
            if ui_control.verify_page(UIPage.page_main): return True
            itt.move_and_click(ButtonTalkSkip.click_position())
            if esc_timer.reached_and_reset():
                itt.key_press('esc')
            itt.delay(0.2)
        return False
    
if __name__ == '__main__':
    t = Talk()
    # t.talk_with_npc()
    # t.talk_until_switch()
    # t.talk_switch(Expedition)
    
    print(t.talk_with_npc(asset.Text(zh="Flora", en="Flora")))
    
    t.exit_talk()