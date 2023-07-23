from source.talk.talk import Talk
from source.common.base_threading import AdvanceThreading

class StorySkip(AdvanceThreading, Talk):
    def __init__(self, thread_name=None):
        super().__init__(thread_name)
        self.while_sleep = 0.5
    
    def loop(self):
        if self._is_in_talking():
            self.talk_skip(self.checkup_stop_func)