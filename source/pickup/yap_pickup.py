import datetime
import os

from source.util import *
import giayap as yap
import pydantic
from threading import Thread

class PickupResult(pydantic.BaseModel):
    pk_time:datetime.datetime
    pk_name:str


class YapPickupper(Thread):
    def __init__(self):
        super().__init__()
        self.rust_path = os.environ["PYO_YAP_PATH"]
        self.yaper = yap.PickupC()
        self.file_reader = open(f"{self.rust_path}\\logs\\log.log", 'r', encoding='utf-8')
        self.pickup_result = []
        self.pickup_result:t.List[PickupResult]
        self._load_collect_result()

        self.start_count = 0
        self.stop_count = 0

        if GIAconfig.Dev_DisableF:
            self.yaper.pausef()


    def start_pickup(self):
        if not GIAconfig.Dev_DisableF:
            self.yaper.startf()

        self.start_count += 1

    def stop_pickup(self):
        self.stop_count += 1
        if self.start_count <= self.stop_count:
            self.yaper.pausef()
        else:
            logger.debug(f"start {self.start_count} > stop {self.stop_count}, will not stop.")

    def _load_collect_result(self):
        _ = self.file_reader.read().split('\n')
        if len(_)>0:
            for i in _:
                if "ITEM_PICKUPED" in i:
                    pk = i.split('|')
                    pkt_str = list(map(int, pk[0].split('-')))
                    pkt = datetime.datetime(pkt_str[0], pkt_str[1], pkt_str[2], pkt_str[3], pkt_str[4], pkt_str[5])

                    pkn = pk[2].replace("ITEM_PICKUPED: ", "")
                    self.pickup_result.append(PickupResult(pk_time=pkt, pk_name=pkn))

    def get_last_picked_item(self) -> PickupResult:
        if len(self.pickup_result)>0:
            return self.pickup_result[-1]
        else:
            return PickupResult(pk_time='NULL', pk_name='NULL')

    def run(self):
        while 1:
            time.sleep(1)
            self._load_collect_result()

yap_pickupper = YapPickupper()
yap_pickupper.start()

if __name__ == '__main__':

    print(yap_pickupper.pickup_result)
    while 1:
        time.sleep(1)

        # print(yap_pickupper.pickup_result[-1])