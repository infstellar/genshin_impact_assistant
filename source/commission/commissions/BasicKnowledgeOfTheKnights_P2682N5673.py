from source.commission.commission_template import CommissionTemplate
from source.talk.talk import Talk
from source.manager import asset

AskDirectly = asset.TextTemplate({"zh_CN":"直接问吧","en_US":""})
Librarian = asset.TextTemplate({"zh_CN":"图书管理员","en_US":"Librarian"})
CavalryCaptain = asset.TextTemplate({"zh_CN":"骑兵队长","en_US":"Cavalry Captain"})
Outrider = asset.TextTemplate({"zh_CN":"侦察骑士","en_US":"Outrider"})

meta = {
    "type":"BasicKnowledgeOfTheKnights",
    "position":[2682,-5673]
}
class BasicKnowledgeOfTheKnights_P2682N5673(CommissionTemplate, Talk):
    def __init__(self):
        CommissionTemplate.__init__(self, meta["type"], meta["position"], is_CFCF=True, is_TMCF=True)
        Talk.__init__(self)
        
    def exec_mission(self):
        self.move_along("BasicKnowledgeOfTheKnights20230409115353i0")
        self.talk_with_npc()
        self.talk_until_switch()
        self.talk_switch(AskDirectly)
        self.talk_with_npc()
        self.talk_until_switch()
        self.talk_switch(Librarian)
        self.talk_until_switch()
        self.talk_switch(CavalryCaptain)
        self.talk_until_switch()
        self.talk_switch(Outrider)
        self.talk_skip(self.checkup_stop_func)
        self.is_commission_succ=True
        
if __name__ == '__main__':
    execc = BasicKnowledgeOfTheKnights_P2682N5673()
    execc.start()
        