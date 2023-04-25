from source.commission.util import *
from source.task.task_template import TaskTemplate
from source.commission.commission_parser import CommissionParser
from source.commission.commission_acquisition import get_commission_object

class CommissionExecutor(TaskTemplate, CommissionParser):
    def __init__(self):
        super().__init__()
        self.setName("CommissionExecutor")
            
        self._set_and_save_and_load_commission_dicts()
        
    def loop(self):
        for i in self.commission_dicts:
            co = get_commission_object(i["type"], i["position"])
            if not co:
                continue
            if i["done"]:
                logger.info(f"{i['type']} has been done.")
                continue
            self._add_sub_threading(co)
            co.continue_threading()
            while 1:
                time.sleep(2)
                if self.checkup_stop_func():return
                if co.pause_threading_flag: break
            self._clean_sub_threading()
            if co.is_commission_succ:
                j = load_json(json_name="commission_dict.json", default_path=rf"{CONFIG_PATH}\commission")
                j[self.commission_dicts.index(i)]["done"]=True
                save_json(j ,json_name="commission_dict.json", default_path=rf"{CONFIG_PATH}\commission")
        r = self._set_and_save_and_load_commission_dicts()
        if not r:
            self.pause_threading()
        if len(self.commission_dicts)==0:
            self.pause_threading()

if __name__ == '__main__':
    ce = CommissionExecutor()
    ce.start()
    ce.continue_threading()
    while 1:
        time.sleep(1)