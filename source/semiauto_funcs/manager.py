from source.util import *



class SemiautoFuncManager():
    def __init__(self) -> None:
        self.SEMIAUTO_COMBAT = None
        self.last_d = "idle"
    
    def apply_change(self, d:str):
        logger.info(t2t("Apply semi-auto function: ") + d)
        if 'semiauto_combat' == d:
            from source.combat.combat_controller import CombatController
            self.SEMIAUTO_COMBAT = CombatController()
            self.SEMIAUTO_COMBAT.start()
            self.SEMIAUTO_COMBAT.continue_threading()
        else:
            if self.SEMIAUTO_COMBAT is not None:
                self.SEMIAUTO_COMBAT.stop_threading()
