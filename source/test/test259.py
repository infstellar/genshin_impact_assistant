import yaml
from source.util import *

j = load_json("auto_collector.en_US.jsondoc", default_path=fr"{CONFIG_PATH}/json_doc")
with open(fr"{CONFIG_PATH}/json_doc/auto_collector.en_US.yaml", 'w', encoding="utf-8") as f:
    yaml.dump(data=j, stream=f, allow_unicode=True)