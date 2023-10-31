from source.util import *
from source.task.domain.domain_flow_upgrade import DomainFlowController
from source.teyvat_move.teyvat_move_flow_upgrade import TeyvatMoveFlowController
from source.task.task_template import TaskTemplate
from source.funclib.collector_lib import load_items_position
from source.funclib.generic_lib import f_recognition
from source.ui.ui import ui_control
import source.ui.page as UIPage
from source.interaction.interaction_core import itt
from source.manager import asset
from source.task import task_id as TI
from source.funclib.err_code_lib import ERR_NONE, ERR_STUCK, ERR_PASS
from source.common import timer_module
from source.flow.utils.cvars import *


class DomainTask(TaskTemplate):
    def __init__(self):
        super().__init__()
        self.dfc = DomainFlowController()
        self.TMFCF = TeyvatMoveFlowController()
        self.flow_mode = TI.DT_INIT
        
        self._add_sub_threading(self.dfc)
        self._add_sub_threading(self.TMFCF)
        
        self.domain_name = GIAconfig.Domain_DomainName
        self.domain_stage_name = GIAconfig.Domain_DomainStageName
        self.domain_posi = load_items_position(self.domain_name,mode=1, ret_mode=1)[0]
        self.TMFCF.set_parameter(stop_rule = STOP_RULE_F, MODE = "AUTO", target_posi = self.domain_posi, is_tp=True, tp_type=["Domain"])
        self.TMFCF.set_target_posi(self.domain_posi)
        self.last_domain_times = int(GIAconfig.Domain_ChallengeTimes)

        logger.info(f"domain_name: {self.domain_name} domain_stage_name {self.domain_stage_name} domain times {self.last_domain_times}")
    
    def _domain_text_process(self, text:str):
        text = text.replace('：', ':')
        text = text.replace(' ', '')
        text = text.replace("Ⅱ", "I")
        replace_dict = {
            "惊垫":"惊蛰"
        }
        if ":" in text:
            text = text[text.index(':')+1:]
        for i in replace_dict:
            if i in text:
                text = text.replace(i, replace_dict[i])
        return text
    
    def _enter_domain(self):
        while 1:
            if self.checkup_stop_func():return
            itt.key_press('f')
            if not f_recognition():
                break
        while not itt.get_img_existence(asset.ButtonDomainSoloChallenge):
            if self.checkup_stop_func():return
            itt.delay("animation")
        itt.delay(1,comment="genshin animation")
        from source.api.pdocr_complete import ocr
        from source.api.pdocr_api import SHAPE_MATCHING, ACCURATE_MATCHING, CONTAIN_MATCHING
        cap_area = asset.AreaDomainSwitchChallenge.position
        itt.delay(1,comment="genshin animation")
        self.domain_stage_name = self._domain_text_process(self.domain_stage_name)
        retry_count = 0
        while retry_count < 3:
            p1 = ocr.get_text_position(itt.capture(jpgmode=NORMAL_CHANNELS, posi=cap_area), self.domain_stage_name,
                                       cap_posi_leftup=cap_area[:2],
                                       text_process = self._domain_text_process,
                                       mode=CONTAIN_MATCHING)
            logger.info(f"domain_stage_name:{self.domain_stage_name}, p1:{p1}, cap_area:{cap_area}")
            if p1 != -1:
                itt.move_and_click([p1[0] + 5, p1[1] + 5], delay=1)
                break
            else:
                texts = ocr.get_all_texts(itt.capture(jpgmode=NORMAL_CHANNELS, posi=cap_area))
                logger.warning(t2t("找不到秘境名称，重试中。"))
                logger.info(f"all texts: {list(map(self._domain_text_process, texts))}")
                itt.delay(1.5)
                retry_count += 1
        
        # itt.delay(1, comment="too fast TAT")
        ctimer = timer_module.TimeoutTimer(5)
        while 1:
            if self.checkup_stop_func():return
            time.sleep(0.2)

            itt.appear_then_click(asset.ButtonDomainSoloChallenge)
            
            itt.appear_then_click(asset.ButtonDomainStartChallenge)

            if itt.get_img_existence(asset.IconUIInDomain):
                break
            if ctimer.istimeout():
                if itt.get_text_existence(asset.LEY_LINE_DISORDER):
                    break
    
    def _end_domain(self):
        time.sleep(0.5)
        cap = itt.capture(jpgmode=FOUR_CHANNELS)
        cap = itt.png2jpg(cap, channel='ui')
        if self.last_domain_times > 1:
            logger.info(t2t('开始下一次秘境'))
            # logger.info('start next domain.')
            self.last_domain_times -= 1
            while 1:
                if self.checkup_stop_func():return
                r = itt.appear_then_nothing(asset.conti_challenge)
                if r:
                    from source.api.pdocr_complete import ocr
                    from source.api.pdocr_api import SHAPE_MATCHING, ACCURATE_MATCHING, CONTAIN_MATCHING
                    resin_mode = GIAconfig.Domain_Resin
                    if str(resin_mode) == '40':
                        area = asset.AreaDomainResidue.position
                        text = ocr.get_all_texts(itt.capture(jpgmode=NORMAL_CHANNELS, posi=area),extract_white_threshold=255)
                        print(text)
                        if len(text) > 0 and text[0].isdigit() and int(text[0]) >= 1:
                            logger.info(t2t('有足够的树脂，继续下一次'))
                        else:
                            logger.info(t2t('树脂不足，提前退出'))
                            self._exit_domain()
                            return
                    elif str(resin_mode) == '20':
                        area = asset.AreaDomainResidue1.position
                        text = ocr.get_all_texts(itt.capture(jpgmode=NORMAL_CHANNELS, posi=area),extract_white_threshold=255)
                        print(text)
                        if len(text) > 0 and text[0].isdigit() and int(text[0]) >= 20:
                            logger.info(t2t('有足够的树脂，继续下一次'))
                        else:
                            logger.info(t2t('树脂不足，提前退出'))
                            self._exit_domain()
                            return

                    r = itt.appear_then_click(asset.conti_challenge)
                    if r:
                        break

            self.flow_mode = TI.DT_IN_DOMAIN
            self.dfc.reset()
            
        else:
            logger.info(t2t('次数结束。退出秘境'))
            # logger.info('no more times. exit domain.')
            self._exit_domain()


    def _exit_domain(self):
        while 1:
            if self.checkup_stop_func():return
            r = itt.appear_then_click(asset.exit_challenge)
            if r:
                break

        # exit all threads
        self.pause_threading()
        time.sleep(10)

    def _check_state(self):
        
        if itt.get_img_existence(asset.IconUIInDomain) or itt.get_text_existence(asset.LEY_LINE_DISORDER):
            self.flow_mode = TI.DT_IN_DOMAIN
        elif itt.get_img_existence(asset.IconUIEmergencyFood):
            self.flow_mode = TI.DT_MOVE_TO_DOMAIN
        else:
            logger.info(t2t("Unknown UI page"))
            ui_control.ui_goto(UIPage.page_main)

    def loop(self):
        if self.flow_mode == TI.DT_INIT:
            self._check_state()
            # self.flow_mode = TI.DT_MOVE_TO_DOMAIN

        if self.flow_mode == TI.DT_MOVE_TO_DOMAIN:
            self.TMFCF.start_flow()
            while 1:
                if self.checkup_stop_func():return
                time.sleep(0.2)
                if self.TMFCF.pause_threading_flag:
                    break
            self.TMFCF.pause_threading()
            
            self._enter_domain()
            
            self.flow_mode = TI.DT_IN_DOMAIN
            
        if self.flow_mode == TI.DT_IN_DOMAIN:
            self.dfc.start_flow()
            # time.sleep(1)
            while 1:
                if self.checkup_stop_func():return
                time.sleep(0.2)
                if self.dfc.pause_threading_flag:
                    break
            
            self._end_domain()
            
            
if __name__ == '__main__':
    dmt = DomainTask()
    dmt._enter_domain()
    # dmt.flow_mode = TI.DT_IN_DOMAIN
    while 1:
        time.sleep(0.2)
        dmt.start()