from source.map.extractor.reader import PoiJsonApi
from source.util import *
poiapi = PoiJsonApi(lang='en_US')
save_json(poiapi.get_domains, json_name='Domain_Names_en_US.json', default_path=fr"{ROOT_PATH}/assets/domain_names")
poiapi = PoiJsonApi(lang='zh_CN')
save_json(poiapi.get_domains, json_name='Domain_Names_zh_CN.json', default_path=fr"{ROOT_PATH}/assets/domain_names")