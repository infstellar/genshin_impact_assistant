from source.util import *



class IngameAssistManager():
    def __init__(self) -> None:
        self.PUO = None
        self.SS = None
        pass
    
    def apply_change(self, d:list):
        if 'pickup_assist' in d:
            if self.PUO is None:
                from source.pickup.pickup_operator import PickupOperator
                self.PUO = PickupOperator()
                self.PUO.start()
            self.PUO.continue_threading()
        else:
            if self.PUO is not None:
                self.PUO.pause_threading()
        
        if 'story_skip_assist' in d:
            from source.ingame_assist.story_skip import StorySkip
            self.SS = StorySkip()
            self.SS.start()
            self.SS.continue_threading()
            
        else:
            if self.SS is not None:
                self.SS.stop_threading()
