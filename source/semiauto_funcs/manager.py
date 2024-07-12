from source.util import *
import winsound


class SemiautoFuncManager():
    def __init__(self) -> None:
        self.SEMIAUTO_COMBAT = None
        self.COLLECT_IMAGE = None
        self.last_d = "idle"
        self.started = False
    def apply_change(self):
        d = self.last_d
        if d == 'idle': return
        logger.info(t2t("Apply semi-auto function: ") + d)
        if not self.started:
            if 'semiauto_combat' == d:
                if self.SEMIAUTO_COMBAT is None:
                    from source.combat.combat_controller import CombatController
                    self.SEMIAUTO_COMBAT = CombatController()
                    self.SEMIAUTO_COMBAT.start()
                self.SEMIAUTO_COMBAT.continue_threading()
            elif 'collect_image' == d:
                if self.COLLECT_IMAGE is None:
                    from source.task.collect_image.collect_image import CollectImage
                    self.COLLECT_IMAGE = CollectImage()
                    self.COLLECT_IMAGE.start()
                self.COLLECT_IMAGE.continue_threading()
            self.started = not self.started
            logger.info(t2t("Start semi-auto function: ") + d)
            winsound.Beep(400,200)
        else:
            if self.SEMIAUTO_COMBAT is not None:
                if self.SEMIAUTO_COMBAT.pause_threading_flag != False:
                    self.SEMIAUTO_COMBAT.pause_threading()
            if self.COLLECT_IMAGE is not None:
                if self.COLLECT_IMAGE.pause_threading_flag != False:
                    self.COLLECT_IMAGE.pause_threading()
            self.started = not self.started
            logger.info(t2t("Stop semi-auto function: ") + d)
            winsound.Beep(800, 200)
