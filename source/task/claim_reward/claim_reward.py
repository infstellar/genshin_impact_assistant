from source.task.claim_reward.util import *
from source.mission.mission_template import MissionExecutor, STOP_RULE_F
from source.task.task_template import TaskTemplate
from source.talk.talk import Talk
from source.manager import asset
from source.assets.claim_rewards import *
import os
    

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
        itt.delay(1)
        cmd = "start AutoHotkey64.exe OneFiledispatch.ahk"
        os.system(cmd)

    def exec_mission(self):
        self.available_rewards = self.get_available_reward()
        if "Expedition" in self.available_rewards or "Commission" in self.available_rewards:
            self.move_along("Katheryne20230408124320i0", is_precise_arrival=True, stop_rule = STOP_RULE_F)
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
        
class ClaimRewardTask(TaskTemplate):
    def __init__(self):
        super().__init__()
        self.CRM = ClaimRewardMission()
        self._add_sub_threading(self.CRM, start=False)
    
    def task_run(self):
        self.blocking_startup(self.CRM)
        
if __name__ == '__main__':
    crm = ClaimRewardMission()
    r = crm._exec_dispatch()
    print()
    crt = ClaimRewardTask()
    crt.start()