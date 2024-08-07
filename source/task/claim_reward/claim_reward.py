from source.task.claim_reward.util import *
from source.mission.mission_template import MissionExecutor, STOP_RULE_F
from source.task.task_template import TaskTemplate
from source.talk.talk import Talk
from source.manager import asset
from source.assets.claim_rewards import *
from source.ui import page as UIPage
    

class ClaimRewardMission(MissionExecutor, Talk):
    """这个类以MissionExecutor的方式执行任务，因为Mission中已有许多适合该任务的函数可以直接调用。
    
    有关更多这样的Mission型任务的信息，可以参考source.task.ley_line_outcrop，该文件下有更多注释。

    Args:
        MissionExecutor (_type_): _description_

    Returns:
        _type_: _description_
    """
    def __init__(self):
        MissionExecutor.__init__(self, is_TMCF=True)
        Talk.__init__(self)
        
    def get_available_reward(self):
        ui_control.ensure_page(UIPage.page_bigmap)
        cap = itt.capture(jpgmode=NORMAL_CHANNELS, posi=asset.AreaClaimRewardAvailableReward.position)
        img = extract_white_letters(cap)
        res = ocr.get_all_texts(img)
        rewards = []
        for text in res:
            if ExpeditionReward.text in text:
                rewards.append("Expedition")
            if "每日委托" in text:
                rewards.append("Commission")
        logger.info(rewards)
        return rewards

    def claim_battle_path(self):
        itt.key_press('F4')
        itt.delay('2animation')
        itt.appear_then_click(ButtonSwitchToBattlePathDailyMission)
        itt.delay('2animation')
        itt.appear_then_click(ButtonClaimBattlePathDailyMission)
        itt.delay('2animation')
        while not ui_control.verify_page(UIPage.page_main):
            itt.key_press('esc')
            itt.delay('2animation')

    def _exec_dispatch(self):
        itt.delay(3)
        itt.appear_then_click(ButtonExpeditionClaimAll)
        itt.delay(1)
        itt.appear_then_click(ButtonExpeditionRestart)
        itt.delay(1)
        # def reset_character():
        #     while 1:
        #         cap = itt.capture(jpgmode=NORMAL_CHANNELS)
        #         complete_posi = match_multiple_img(cap, IconExpeditionComplete.image, ignore_close=True)
        #         complete_posi += match_multiple_img(cap, IconExpeditionComplete2.image, ignore_close=True)
        #         if len(complete_posi)==0:
        #             return
        #         chara_head_posi = np.array(complete_posi)+np.array([80,80])
        #         for posi in chara_head_posi:
        #             itt.move_and_click(posi)
        #             itt.delay("2animation")
        #             r1 = itt.appear_then_click(ButtonExpeditionClaim)
        #             itt.delay("2animation")
        #             itt.move_and_click(ButtonExpeditionClaim.click_position())
        #             itt.delay("2animation")
        #             itt.appear_then_click(ButtonExpeditionSelectCharacters)
        #             itt.delay("2animation")
        #             i=0
        #             while 1:
        #                 cp = ButtonExpeditionFirstCharacter.click_position()
        #                 itt.move_and_click([cp[0],cp[1]+i])
        #                 itt.delay("2animation")
        #                 if itt.get_img_existence(IconClaimRewardExpedition):
        #                     break
        #                 i+=80
        # for area in [ButtonExpeditionMD, ButtonExpeditionLY, ButtonExpeditionDQ, ButtonExpeditionXM]:
        #     r = itt.appear_then_click(area)
        #     if not r: continue
        #     itt.delay("2animation")
        #     reset_character()

    def exec_mission(self):
        ui_control.ui_goto(UIPage.page_main)
        itt.key_press('F1')
        ui_control.wait_until_stable()
        while 1:
            itt.appear_then_click(ButtonCommissionSwitchToCommissionPage)
            ui_control.wait_until_stable()
            siw()
            if self.checkup_stop_func(): return
            if itt.appear(IconCommissionDetailPage):
                break

        if itt.appear(ButtonCommissionUsePoints):
            while 1:
                r = itt.appear_then_click(ButtonCommissionUsePoints)
                ui_control.wait_until_stable()
                if r: break
                siw()
                if self.checkup_stop_func(): return

        while 1:
            itt.key_press('esc')
            ui_control.wait_until_stable()
            siw()
            if self.checkup_stop_func(): return
            if ui_control.verify_page(UIPage.page_main): break


        self.available_rewards = self.get_available_reward()

        if "Expedition" in self.available_rewards or "Commission" in self.available_rewards:
            self.move_along(MOVE_PATH, is_precise_arrival=True, stop_rule = STOP_RULE_F)
            if "Commission" in self.available_rewards:
                self.talk_with_npc()
                self.talk_until_switch(self.checkup_stop_func)
                self.talk_switch(ClaimDailyCommissionReward)
                self.exit_talk()
            if "Expedition" in self.available_rewards:
                self.talk_with_npc()
                self.talk_until_switch(self.checkup_stop_func)
                self.talk_switch(DispatchCharacterOnExpedition)
                self._exec_dispatch()
                self.exit_talk()
        ui_control.ensure_page(UIPage.page_main)
        if itt.appear(IconBattlePathExclamation):
            self.claim_battle_path()
        
class ClaimRewardTask(TaskTemplate):
    def __init__(self):
        super().__init__()
        self.CRM = ClaimRewardMission()
        self._add_sub_threading(self.CRM, start=False)
    
    def task_run(self):
        self.blocking_startup(self.CRM)


MOVE_PATH = {'name': '', 'time': '', 'start_position': [2525.677199999999, -5804.90955], 'break_position': [[2525.677, -5804.91], [2525.28, -5804.8], [2537.968, -5793.131], [2583.288, -5738.081], [2587.129, -5734.24], [2594.555, -5729.375], [2599.164, -5726.814], [2614.27, -5717.34], [2619.135, -5714.012], [2620.672, -5708.379]], 'end_position': [2620.6717500000004, -5707.8666], 'position_list': [{'position': [2525.677, -5804.91], 'motion': 'WALKING', 'id': 1}, {'position': [2527.214, -5804.654], 'motion': 'WALKING', 'id': 2}, {'position': [2529.006, -5801.581], 'motion': 'WALKING', 'id': 3}, {'position': [2529.774, -5799.789], 'motion': 'WALKING', 'id': 4}, {'position': [2531.566, -5798.252], 'motion': 'WALKING', 'id': 5}, {'position': [2533.871, -5796.46], 'motion': 'WALKING', 'id': 6}, {'position': [2535.407, -5794.668], 'motion': 'WALKING', 'id': 7}, {'position': [2537.968, -5793.131], 'motion': 'WALKING', 'id': 8}, {'position': [2540.016, -5790.571], 'motion': 'WALKING', 'id': 9}, {'position': [2542.064, -5788.778], 'motion': 'WALKING', 'id': 10}, {'position': [2543.857, -5787.242], 'motion': 'WALKING', 'id': 11}, {'position': [2544.369, -5786.474], 'motion': 'WALKING', 'id': 12}, {'position': [2545.137, -5784.938], 'motion': 'WALKING', 'id': 13}, {'position': [2546.929, -5783.401], 'motion': 'WALKING', 'id': 14}, {'position': [2549.234, -5781.865], 'motion': 'WALKING', 'id': 15}, {'position': [2550.258, -5780.841], 'motion': 'WALKING', 'id': 16}, {'position': [2551.538, -5778.536], 'motion': 'WALKING', 'id': 17}, {'position': [2553.331, -5778.024], 'motion': 'WALKING', 'id': 18}, {'position': [2555.123, -5775.72], 'motion': 'WALKING', 'id': 19}, {'position': [2556.659, -5773.671], 'motion': 'WALKING', 'id': 20}, {'position': [2558.708, -5772.903], 'motion': 'WALKING', 'id': 21}, {'position': [2559.988, -5771.367], 'motion': 'WALKING', 'id': 22}, {'position': [2560.244, -5771.367], 'motion': 'WALKING', 'id': 23}, {'position': [2560.756, -5769.319], 'motion': 'WALKING', 'id': 24}, {'position': [2562.548, -5766.502], 'motion': 'WALKING', 'id': 25}, {'position': [2564.085, -5764.71], 'motion': 'WALKING', 'id': 26}, {'position': [2565.365, -5762.661], 'motion': 'WALKING', 'id': 27}, {'position': [2566.389, -5760.357], 'motion': 'WALKING', 'id': 28}, {'position': [2567.669, -5758.564], 'motion': 'WALKING', 'id': 29}, {'position': [2569.206, -5757.284], 'motion': 'WALKING', 'id': 30}, {'position': [2570.486, -5754.98], 'motion': 'WALKING', 'id': 31}, {'position': [2570.998, -5753.444], 'motion': 'WALKING', 'id': 32}, {'position': [2573.303, -5751.395], 'motion': 'WALKING', 'id': 33}, {'position': [2574.583, -5749.603], 'motion': 'WALKING', 'id': 34}, {'position': [2575.607, -5747.042], 'motion': 'WALKING', 'id': 35}, {'position': [2577.655, -5744.226], 'motion': 'WALKING', 'id': 36}, {'position': [2579.448, -5741.921], 'motion': 'WALKING', 'id': 37}, {'position': [2579.704, -5741.665], 'motion': 'WALKING', 'id': 38}, {'position': [2580.984, -5739.105], 'motion': 'WALKING', 'id': 39}, {'position': [2583.288, -5738.081], 'motion': 'WALKING', 'id': 40}, {'position': [2585.081, -5737.056], 'motion': 'WALKING', 'id': 41}, {'position': [2585.849, -5735.52], 'motion': 'WALKING', 'id': 42}, {'position': [2585.849, -5735.52], 'motion': 'WALKING', 'id': 43}, {'position': [2587.129, -5734.24], 'motion': 'WALKING', 'id': 44}, {'position': [2589.178, -5733.984], 'motion': 'WALKING', 'id': 45}, {'position': [2590.714, -5732.96], 'motion': 'WALKING', 'id': 46}, {'position': [2592.25, -5731.679], 'motion': 'WALKING', 'id': 47}, {'position': [2594.555, -5729.375], 'motion': 'WALKING', 'id': 48}, {'position': [2596.603, -5728.095], 'motion': 'WALKING', 'id': 49}, {'position': [2599.164, -5726.814], 'motion': 'WALKING', 'id': 50}, {'position': [2600.956, -5725.278], 'motion': 'WALKING', 'id': 51}, {'position': [2602.492, -5723.742], 'motion': 'WALKING', 'id': 52}, {'position': [2604.797, -5723.23], 'motion': 'WALKING', 'id': 53}, {'position': [2606.589, -5722.461], 'motion': 'WALKING', 'id': 54}, {'position': [2607.613, -5720.925], 'motion': 'WALKING', 'id': 55}, {'position': [2610.43, -5719.901], 'motion': 'WALKING', 'id': 56}, {'position': [2611.966, -5718.877], 'motion': 'WALKING', 'id': 57}, {'position': [2614.27, -5717.34], 'motion': 'WALKING', 'id': 58}, {'position': [2616.575, -5715.548], 'motion': 'WALKING', 'id': 59}, {'position': [2618.367, -5714.524], 'motion': 'WALKING', 'id': 60}, {'position': [2618.623, -5714.524], 'motion': 'WALKING', 'id': 61}, {'position': [2620.672, -5712.732], 'motion': 'WALKING', 'id': 62}, {'position': [2620.672, -5712.732], 'motion': 'WALKING', 'id': 63}, {'position': [2620.672, -5710.171], 'motion': 'WALKING', 'id': 64}, {'position': [2620.672, -5708.379], 'motion': 'WALKING', 'id': 65}, {'position': [2620.672, -5707.867], 'motion': 'WALKING', 'id': 66}], 'additional_info': {'pickup_points': [1]}, 'adsorptive_position': [], 'generate_from': 'path recorder 1.0'}

if __name__ == '__main__':
    # crm = ClaimRewardMission()
    # r = crm._exec_dispatch()
    # print()
    crt = ClaimRewardTask()
    crt.start()