from integration_json.utils import *
from source.task.task_template import TaskTemplate
from integration_json.convert_json_to_mission import convert_collect_json
from integration_json.reader import JsonIntegrationApi



class AutoCollector(TaskTemplate):
    def __init__(self):
        super().__init__()
        self.name = "AutoCollector"
        self.prefix = 'Liyue'
        self.api = JsonIntegrationApi(prefix=self.prefix)

    def _load_json(self) -> PositionJson:
        for i in self.api.data.values():
            yield i

    def task_run(self):
        if True:
            for i in self._load_json():
                runner = convert_collect_json(i)
                runner.start()
                runner.continue_threading()
                while 1:
                    siw()
                    if runner.pause_threading_flag:
                        break
                    if self.checkup_stop_func():
                        break

if __name__ == '__main__':
    AutoCollector().task_run()