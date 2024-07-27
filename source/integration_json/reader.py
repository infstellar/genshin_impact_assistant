# coding: utf-8

import os.path
import re
import time
import typing

from cached_property import cached_property
from source.integration_json.utils import *
from source.device.alas.config_utils import *


class JsonIntegrationApi():
    def __init__(self, path=None, lang=GLOBAL_LANG, prefix: str = ''):
        """
        Args:
            path (str): Path to json_integration/zh_CN
        """
        if path is None:
            path = f'./assets/json_integration/{lang}'
        path = r"M:\ProgramData\Json_Integration"
        self.path = path
        self.lang = lang
        self.prefix = prefix
        self.data_classified = {}
        self.preprocessing_data = {}
        # self.preprocessing_data = load_json(all_path="{ROOT_PATH}\\assets\\POI_JSON_API\\integration_json\\preprocessing_integration_json.json")
        self.read_times = 0

    @classmethod
    def read_json(cls, data, model, attr: str, coll_name: str, coll_type: str, path: str):
        out = {}
        if isinstance(data, str):
            data = read_file(data)

        # for row in data:
        row = data
        row['collection_name'] = coll_name
        row['collection_type'] = coll_type
        row['path'] = path
        row['location'] = LOCA_TEYVAT
        row = model(**row)
        key = row.__getattribute__(attr)
        out[key] = row
        return out

    @cached_property
    def data(self) -> t.Dict[str, t.List[PositionJson]]:
        data = {}
        row: dict
        row = read_file(f"{ROOT_PATH}\\assets\\POI_JSON_API\\integration_json\\preprocessing_integration_json.json")
        for k in row.keys():
            data[k] = []
            for i in row[k]:
                data[k].append(PositionJson(**i))

        return data

    def read_folder(self, rel_path: str = "", collection_type: str = COLL_TYPE_ANY):
        pt = time.time()
        for root, dirs, files in os.walk(self.path + f"\\{rel_path}"):
            for f in files:
                complete_file_path = os.path.join(root, f)
                if not f[-5:] == '.json':
                    continue
                if collection_type == COLL_TYPE_PLANT:

                    if "渊下宫" in complete_file_path or r"层岩巨渊·地下矿区" in complete_file_path or "金苹果群岛" in complete_file_path or "一次性" in complete_file_path:
                        continue
                j = [i for i in complete_file_path.split('\\')]
                coll_name = j[j.index("Json_Integration") + 2]
                if "锚点&神像" in complete_file_path:
                    coll_name = "传送点"
                elif "狗粮" in complete_file_path:
                    coll_name = "圣遗物"
                # os.path.dirname(os.path.dirname(complete_file_path)).split('\\')[-1]
                json_content = read_file(complete_file_path, is_print=False)
                row = {}
                row['name'] = f[:-5]

                row['position'] = round_list(json_content['position'],3)
                row['collection_name'] = coll_name
                row['collection_type'] = collection_type
                row['path'] = self.get_rel_path(complete_file_path)
                row['location'] = LOCA_TEYVAT

                if coll_name not in self.preprocessing_data.keys():
                    self.preprocessing_data[coll_name] = []
                self.preprocessing_data[coll_name].append(row)

                self.read_times += 1
                if self.read_times % 500 == 0:
                    logger.info(f'load data: {self.read_times}/11792+')
        logger.info(t2t("data loaded. cost") + f'{round(time.time() - pt, 2)}')
        logger.info(f'load {self.read_times} data')

    def get_rel_path(self, completet_file_path, addi=1):
        j = [i for i in completet_file_path.split('\\')]
        relative_path = j[j.index("Json_Integration") + addi:]
        p = ''
        for k in relative_path:
            p = os.path.join(p, k)
        return p

    def preprocess_data(self, save_in=f"{ROOT_PATH}\\assets\\POI_JSON_API\\integration_json"):
        logger.info(t2t("loading data"))
        pt = time.time()
        times = 0

        for i in [r"锚点&神像\3.4沙漠锚点神像",
                  r"锚点&神像\蒙德&璃月锚点神像",
                  r"锚点&神像\稻妻锚点神像-不含渊-下-宫",
                  r"锚点&神像\4.6枫丹",
                  r"锚点&神像\4.4传送锚点",
                  r"锚点&神像\4.2锚点",
                  r"锚点&神像\4.1锚点神像",
                  r"锚点&神像\4.0枫丹锚点神像",
                  r"锚点&神像\3.6沙漠新锚点神像",
                  r"锚点&神像\3.4沙漠锚点神像"]:
            self.read_folder(i, collection_type=COLL_TYPE_TELEPORTER)
        self.read_folder(r"圣遗物狗粮\AB线狗粮全部", collection_type=COLL_TYPE_ARTIFACT)
        self.read_folder("植物", collection_type=COLL_TYPE_PLANT)
        save_json(self.preprocessing_data, json_name='preprocessing_integration_json.json', default_path=save_in)

        # for root, dirs, files in os.walk(self.path):
        #     for f in files:
        #         complete_file_path = os.path.join(root, f)
        #         if not f[-5:] == '.json':
        #             continue
        #         if "植物" in complete_file_path:
        #             relative_path = self.get_rel_path(complete_file_path)
        #             coll_type = COLL_TYPE_PLANT
        #         else:
        #             continue
        #         if coll_type == COLL_TYPE_PLANT:
        #             if not "提瓦特" in complete_file_path:
        #                 continue
        #         coll_name = os.path.dirname(os.path.dirname(complete_file_path)).split('\\')[-1]
        #         json_content = read_file(complete_file_path, is_print=False)
        #         row = {}
        #         row['name'] = f[:-5]
        #         row['position'] = json_content['position']
        #         row['collection_name'] = coll_name
        #         row['collection_type'] = coll_type
        #         row['path'] = relative_path
        #         row['location'] = LOCA_TEYVAT
        #         if coll_name not in self.preprocessing_data.keys():
        #             self.preprocessing_data[coll_name] = []
        #         self.preprocessing_data[coll_name].append(row)


JIApi = JsonIntegrationApi()

if __name__ == '__main__':
    jia = JIApi
    a = jia.preprocess_data()
    a = jia.data
    print(jia.get_rel_path(r"M:\ProgramData\Json_Integration\锚点&神像\蒙德&璃月锚点神像\112.json"))
