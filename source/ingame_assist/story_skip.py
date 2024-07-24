from source.talk.talk import Talk
from source.common.base_threading import AdvanceThreading

class StorySkip(AdvanceThreading, Talk):
    def __init__(self, thread_name=None):
        super().__init__(thread_name)
        self.while_sleep = 0.5

    def stop_rule(self):
        return self.checkup_stop_func() or (not self._is_in_talking())

    def loop(self):
        if self._is_in_talking():
            self.talk_skip(self.stop_rule)