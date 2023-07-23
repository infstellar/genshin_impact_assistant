from source.util import *



class IngameAssistManager():
    def __init__(self) -> None:
        self.PUO = None
        self.SS = None
        pass
    
    def apply_change(self, d:list):
        if 'pickup_assist' in d:
            from source.pickup.pickup_operator import PickupOperator
            self.PUO = PickupOperator()
            self.PUO.start()
            self.PUO.continue_threading()
            self.PUO.while_sleep = 0.05
        else:
            if self.PUO is not None:
                self.PUO.stop_threading()
        
        if 'story_skip_assist' in d:
            from source.ingame_assist.story_skip import StorySkip
            self.SS = StorySkip()
            self.SS.start()
            self.SS.continue_threading()
            
        else:
            if self.SS is not None:
                self.SS.stop_threading()