from source.task.claim_reward.util import *
from source.mission.mission_template import MissionExecutor
from source.task.task_template import TaskTemplate
from source.talk.talk import Talk
from source.manager import asset
from source.task.claim_reward.assets import *
    

class ClaimRewardMission(MissionExecutor, Talk):
    def __init__(self):
        MissionExecutor.__init__(self, is_TMCF=True)
        Talk.__init__(self)
        
    def get_available_reward(self):
        ui_control.ensure_page(UIPage.page_bigmap)
        cap = itt.capture(jpgmode=0, posi=asset.AreaClaimRewardAvailableReward.position)
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
    
    def _exec_dispatch(self):
        def reset_character():
            while 1:
                cap = itt.capture(jpgmode=0)
                complete_posi = itt.match_multiple_img(cap, IconExpeditionComplete.image, ignore_close=True)
                complete_posi += itt.match_multiple_img(cap, IconExpeditionComplete2.image, ignore_close=True)
                if len(complete_posi)==0:
                    return
                chara_head_posi = np.array(complete_posi)+np.array([80,80])
                for posi in chara_head_posi:
                    itt.move_and_click(posi)
                    itt.delay("2animation")
                    r1 = itt.appear_then_click(ButtonExpeditionClaim)
                    itt.delay("2animation")
                    itt.move_and_click(ButtonExpeditionClaim.click_position())
                    itt.delay("2animation")
                    itt.appear_then_click(ButtonExpeditionSelectCharacters)
                    itt.delay("2animation")
                    i=0
                    while 1:
                        cp = ButtonExpeditionFirstCharacter.click_position()
                        itt.move_and_click([cp[0],cp[1]+i])
                        itt.delay("2animation")
                        if itt.get_img_existence(IconClaimRewardExpedition):
                            break
                        i+=80
        for area in [ButtonExpeditionMD, ButtonExpeditionLY, ButtonExpeditionDQ, ButtonExpeditionXM]:   
            r = itt.appear_then_click(area)
            if not r: continue
            itt.delay("2animation")
            reset_character()

    def exec_mission(self):
        self.available_rewards = self.get_available_reward()
        if "Expedition" in self.available_rewards or "Commission" in self.available_rewards:
            self.move_along("Katheryne20230408124320i0", is_precise_arrival=True)
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
        
class ClaimRewardTask(TaskTemplate):
    def __init__(self):
        super().__init__()
        self.CRM = ClaimRewardMission()
        self._add_sub_threading(self.CRM, start=False)
        
    def loop(self):
        self.blocking_startup(self.CRM)
        self.pause_threading()
        
if __name__ == '__main__':
    crm = ClaimRewardMission()
    r = crm._exec_dispatch()
    print()
    crt = ClaimRewardTask()
    crt.start()