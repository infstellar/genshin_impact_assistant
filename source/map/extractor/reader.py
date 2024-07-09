import re
import typing as t

from cached_property import cached_property
from pydantic import BaseModel

from i18n import GLOBAL_LANG
from source.device.alas.config_utils import *
from source.map.extractor.convert import MapConverter

from source.en_tools.poi_json_api import zh2en


class PointItemModel(BaseModel):
    count: int
    itemId: int

# class ItemModel(BaseModel):
#     id: int
#     name: str

DOMAIN_IDS = [52, 161, 339, 447, 558, 759, 871, 1285, 1437, 1513, 1937, 2156, 2399, 2564, 2802, 3065]# generate manually.

class PointInfoModel(BaseModel):
    content: str
    hiddenFlag: int
    id: int
    itemList: t.List[PointItemModel]
    markerCreatorId: int
    markerTitle: str
    picture: str = ''
    pictureCreatorId: int = 0
    position: str
    refreshTime: int
    version: int
    videoPath: str

    class Config:
        ignored_types = (cached_property,)

    @cached_property
    def first_item(self):
        # for item in self.itemList:
        #     if item.iconTag == '传送锚点':
        #         return item
        #     if item.iconTag == '副本':
        #         return item
        #     if item.iconTag == '秘境':
        #         return item
        #     if '神像' in item.iconTag:
        #         return item
        if self.markerTitle == '传送锚点':
            return self
        if self.markerTitle == '副本':
            return self
        # if self.markerTitle == '秘境':
        #     return self
        if self.itemList[0].itemId in DOMAIN_IDS:
            self.markerTitle = '秘境'
            return self
        if '神像' in self.markerTitle:
            self.markerTitle='七天神像'
            return self
        return None

    @cached_property
    def teleporter(self) -> t.Optional[str]:
        tag = self.first_item.markerTitle
        if tag == '传送锚点':
            return MapConverter.TP_Teleporter
        if '神像' in tag:
            return MapConverter.TP_Statue
        if tag == '副本':
            return MapConverter.TP_Instance
        if tag == '秘境':
            return MapConverter.TP_Domain
        return None

    @cached_property
    def position_tuple(self) -> t.Tuple[float, float]:
        x, y = self.position.split(',')
        x = float(x)
        y = float(y)
        return x, y

    @cached_property
    def teleporter_name(self) -> str:
        if self.first_item.markerTitle == '传送锚点' or '神像' in self.first_item.markerTitle:
            if self.first_item.id == 758:
                return '三界路飨祭'
            res = re.search(r'【(.*)】', self.content)
            if res:
                name = res.group(1)
                for region in ['蒙德', '璃月', '稻妻', '须弥', '层岩巨渊', '金苹果群岛', '枫丹']:
                    if region in name:
                        try:
                            _, name = name.rsplit(' ', maxsplit=1)
                        except ValueError:
                            pass
                return name

            return ''
        else:
            return self.markerTitle


class ItemModel(BaseModel):
    areaId: int
    count: int
    defaultContent: str
    defaultCount: int
    defaultRefreshTime: int
    # hiddenFlag: int
    iconStyleType: int
    iconTag: str
    id: int
    name: str
    sortIndex: int
    # specialFlag: int
    typeIdList: t.List[int]
    version: int
    


class AreaModel(BaseModel):
    areaId: int
    code: str
    hiddenFlag: int
    iconTag: str
    isFinal: bool
    name: str
    parentId: int
    sortIndex: int
    version: int


class TeleporterModel(BaseModel):
    id: int
    region: str
    tp: str
    item_id: int
    name: str
    position: t.Tuple[float, float]


class PoiJsonApi:
    def __init__(self, path=None, lang=GLOBAL_LANG):
        """
        Args:
            path (str): Path to POI_JSON_API/zh_CN/dataset
        """
        if path is None:
            path = f'./assets/POI_JSON_API/{lang}/dataset'
        self.path = path
        self.lang=lang

    @classmethod
    def read_json(cls, data, model, attr: str):
        out = {}
        if isinstance(data, str):
            data = read_file(data)

        for row in data:
            row = model(**row)
            key = row.__getattribute__(attr)
            out[key] = row
        return out

    @cached_property
    def data(self) -> t.Dict[int, PointInfoModel]:
        data = {}
        for file in iter_folder(self.path, ext='.json'):
            if not re.search(r'\d+\.json$', file):
                continue
            data.update(self.read_json(file, PointInfoModel, 'id'))
        return data

    @cached_property
    def item(self) -> t.Dict[int, ItemModel]:
        return self.read_json(os.path.join(self.path, './item.json'), ItemModel, 'id')

    @cached_property
    def area(self) -> t.Dict[int, AreaModel]:
        return self.read_json(os.path.join(self.path, './area.json'), AreaModel, 'areaId')

    DICT_AREA_ID = {
        1: MapConverter.REGION_Liyue,
        2: MapConverter.REGION_Liyue,
        3: MapConverter.REGION_Liyue,
        4: MapConverter.REGION_TheChasm,
        5: MapConverter.REGION_Mondstadt,
        6: MapConverter.REGION_Mondstadt,
        10: MapConverter.REGION_GoldenAppleArchipelago,
        11: MapConverter.REGION_Inazuma,
        12: MapConverter.REGION_Inazuma,
        13: MapConverter.REGION_Inazuma,
        14: MapConverter.REGION_Inazuma,
        15: MapConverter.REGION_Enkanomiya,
        16: MapConverter.REGION_ThreeRealmsGatewayOffering,
        17: MapConverter.REGION_Mondstadt,
        18: MapConverter.REGION_Sumeru,
        19: MapConverter.REGION_Sumeru,
        21: MapConverter.REGION_Sumeru,
        22: MapConverter.REGION_Sumeru,
        23: MapConverter.REGION_Sumeru,
        27: MapConverter.REGION_Fontaine,
        28: MapConverter.REGION_Fontaine,
        29: MapConverter.REGION_Fontaine,
        30: MapConverter.REGION_Fontaine,
        34: MapConverter.REGION_Liyue,
    }

    LIST_AREA_TEYVAT = [1,2,3,5,6,11,12,13,14,15,17,18,19,20,21,22,23,27,28,29,30,34]

    IGNORE_ID = [
        13408,#TeleporterModel(id=13408, region='Inazuma', tp='Statue', item_id=336, name='离岛', position=(7842.925, 4429.069))
        13407,#TeleporterModel(id=13407, region='Inazuma', tp='Statue', item_id=336, name='踏鞴砂', position=(7324.447, 5295.089))
        14997,#TeleporterModel(id=14997, region='Liyue', tp='Domain', item_id=162, name='「伏龙树」之底', position=(3417.727, 2052.848))
        6624,#TeleporterModel(id=6624, region='Liyue', tp='Domain', item_id=162, name='进入「黄金屋」', position=(4594.587, 3241.352))
        6280,# TeleporterModel(id=6280, region='Mondstadt', tp='Teleporter', item_id=51, name='风龙废墟', position=(4697.584, 457.263))
        6552,6549,6553,6548,6561,
        # 6552: TeleporterModel(id=6552, region='Mondstadt', tp='Domain', item_id=53, name='北风之狼的庙宇', position=(6075.522, 841.175)),
        # 6549: TeleporterModel(id=6549, region='Mondstadt', tp='Domain', item_id=53, name='南风之狮的庙宇', position=(5913.712, 1236.364)),
        # 6553: TeleporterModel(id=6553, region='Mondstadt', tp='Domain', item_id=53, name='深入风龙废墟', position=(4685.808, 458.988)),
        # 6548: TeleporterModel(id=6548, region='Mondstadt', tp='Domain', item_id=53, name='西风之鹰的庙宇', position=(5709.468, 862.586)),
        # 6561: TeleporterModel(id=6561, region='Mondstadt', tp='Domain', item_id=53, name='鹰之门', position=(6253.954, 1497.608)),
        56363,56364,56365 # 名字里带神像，但他不是神像

    ]

    def iter_teleporter(self):
        lang=self.lang
        for id_, row in self.data.items():
            if row.first_item is None:
                continue
            item_id = row.first_item.itemList[0].itemId
            area_id = self.item[item_id].areaId
            region = self.DICT_AREA_ID.get(area_id)
            # region = self.DICT_AREA_ID.get(1)
            layer = MapConverter.convert_REGION_to_LAYER(region)
            position = MapConverter.convert_kongying_to_GIMAP(row.position_tuple, layer=layer).round(3)
            # if lang=='en_US':
            #     name = zh2en(row.teleporter_name)
            # else:
            #     name = row.teleporter_name
            name = row.teleporter_name
            if region is None:
                print(f'none region: id={row.id}, itemId={item_id}, areaid={area_id}')
                continue

            tp = TeleporterModel(
                id=row.id,
                region=region,
                tp=row.teleporter,
                item_id=item_id,
                name=name,
                position=tuple(position),
            )
            yield tp

    def save_teleporter(self):
        lang = self.lang
        from source.device.alas.map_grids import SelectedGrids
        tp = SelectedGrids(list(self.iter_teleporter()))
        tp = tp.sort('region', 'item_id', 'name', 'id')

        from source.device.alas.code_generator import CodeGenerator
        gen = CodeGenerator()
        gen.Import("""
        from source.map.extractor.reader import TeleporterModel
        """)

        with gen.Dict('DICT_TELEPORTER'):
            for row in tp:
                if row.id in self.IGNORE_ID:
                    continue
                gen.DictItem(row.id, row)

        gen.write(f'./source/map/data/teleporter_{lang}.py')


    @cached_property
    def get_domain_ids(self):
        domain_ids = []
        for i in range(1,len(self.item)+1):
            if not (i in self.item): continue
            if self.item[i].name == ('秘境' if self.lang == 'zh_CN' else 'Domains'):
                domain_ids.append(i)
        print(domain_ids)
        return domain_ids

    @cached_property
    def get_domains(self):
        domains = []
        for i in range(1,len(self.data)+1):
            if not (i in self.data): continue
            if self.data[i].itemList[0].itemId in self.get_domain_ids:
                domains.append(self.data[i].markerTitle)
        return domains


if __name__ == '__main__':
    # self = PoiJsonApi(lang='zh_CN')
    # self.
    # self.get_domains
    for lang in ['zh_CN', 'en_US']:
        self = PoiJsonApi(lang=lang)
        self.save_teleporter()
    