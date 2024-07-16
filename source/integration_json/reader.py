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
        row:dict
        row = read_file(f"{ROOT_PATH}\\assets\\POI_JSON_API\\integration_json\\preprocessing_integration_json.json")
        for k in row.keys():
            data[k]=[]
            for i in row[k]:
                data[k].append(PositionJson(**i))

        return data

    def preprocessing_data(self, save_in=f"{ROOT_PATH}\\assets\\POI_JSON_API\\integration_json"):
        logger.info(t2t("loading data"))
        pt = time.time()
        times = 0
        data = {}
        def get_rel_path(attr:str):
            j = [i for i in file.split('\\')]
            relative_path = j[j.index(attr):]
            p = ''
            for k in relative_path:
                p = os.path.join(p, k)
            return p
        for root, dirs, files in os.walk(self.path):
            for f in files:
                file = os.path.join(root, f)
                if not f[-5:] == '.json':
                    continue
                # if not re.search(fr'{self.prefix}\d+\.json$', file):
                #     continue
                if "植物" in file:
                    relative_path = get_rel_path('植物')
                    coll_type = COLL_TYPE_PLANT
                else:
                    continue
                if not "提瓦特" in file:
                    continue
                coll_name = os.path.dirname(os.path.dirname(file)).split('\\')[-1]
                d = read_file(file, is_print=False)
                row = {}
                row['name'] = f[:-5]
                row['position'] = d['position']
                row['collection_name'] = coll_name
                row['collection_type'] = coll_type
                row['path'] = relative_path
                row['location'] = LOCA_TEYVAT
                # row = PositionJson(name=f[:-5], position=d['position'], location=LOCA_TEYVAT, collection_type=coll_type,
                #                    collection_name=coll_name, path=file)
                if coll_name not in data.keys():
                    data[coll_name] = []
                data[coll_name].append(row)
                times += 1
                if times % 500 == 0:
                    logger.info(f'load data: {times}/11792')
        logger.info(t2t("data loaded. cost") + f'{round(time.time()) - pt}', 2)
        logger.info(f'load {times} data')

        save_json(data, json_name='preprocessing_integration_json.json', default_path=save_in)

JIApi = JsonIntegrationApi()

if __name__ == '__main__':
    jia = JIApi
    a = jia.preprocessing_data()
    a = jia.data
    print()
