from source.util import *
import winsound
from source.ingame_ui.ingame_ui import set_notice


class SemiautoFuncManager():
    def __init__(self) -> None:
        self.SEMIAUTO_COMBAT = None
        self.COLLECT_IMAGE = None
        self.RECORD_PATH = None
        self.last_d = "idle"
        self.started = False
    def apply_change(self):
        d = self.last_d
        if d == 'idle': return
        logger.info(t2t("Apply semi-auto function: ") + d)
        if not self.started:
            winsound.Beep(400, 200)
            set_notice(t2t("Starting semi-auto function: ") + d + '...')
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
            elif 'record_path' == d:
                if self.RECORD_PATH is None:
                    from source.semiauto_funcs.path_record import PathRecord
                    self.RECORD_PATH = PathRecord()
                    self.RECORD_PATH.start()
                self.RECORD_PATH.continue_threading()

            self.started = not self.started
            set_notice(t2t("Start semi-auto function: ") + d, timeout=2)

        else:
            set_notice(t2t("Stopping Semi-auto function..."))
            winsound.Beep(800, 200)
            if self.SEMIAUTO_COMBAT is not None:
                self.SEMIAUTO_COMBAT.stop_threading()
                while 1:
                    siw()
                    if not self.SEMIAUTO_COMBAT.is_alive(): break
                self.SEMIAUTO_COMBAT = None

            if self.COLLECT_IMAGE is not None:
                self.COLLECT_IMAGE.stop_threading()
                while 1:
                    siw()
                    if not self.COLLECT_IMAGE.is_alive(): break
                self.COLLECT_IMAGE = None

            if self.RECORD_PATH is not None:
                self.RECORD_PATH.stop_threading()
                while 1:
                    siw()
                    if not self.RECORD_PATH.is_alive(): break
                self.RECORD_PATH = None

            self.started = not self.started
            set_notice(t2t("Stop semi-auto function: ") + d, timeout=2)

