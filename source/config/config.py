from source.util import *
from source.config.util import *
from source.config.config_generated import GeneratedConfig





class GIAConfig(GeneratedConfig):
    bound = {}
    CONFIG_FILE_NAMES = [CONFIGNAME_CONFIG, CONFIGNAME_COLLECTOR, CONFIGNAME_AIM, CONFIGNAME_COMBAT,
                         CONFIGNAME_DOMAIN, CONFIGNAME_PICKUP, CONFIGNAME_PICKUP]

    def __init__(self) -> None:
        super().__init__()

    def load(self):
        for jsonname in self.CONFIG_FILE_NAMES:
            j = load_json(json_name=f"{jsonname}.jsontemplate", default_path=fr"{CONFIG_PATH}/json_template")
            for k in j:
                # if f"{jsonname}_{k}" in self.__dict__:
                self.__dict__[f"{jsonname}___{k}"] = j[k]
                print(f"set {jsonname}___{k} to {j[k]}")

    # def save(self):
    #     var_names = [f"{i}_" for i in self.CONFIG_FILE_NAMES]
    #     var_dicts = {}
    #     for k in self.__dict__:
    #         if f"{k.split('___')[0]}_" in var_names:
    #             var_dicts[k.split('___')[0]] = k

    def update(self):
        self.load()
        

if __name__ == '__main__':
    conf = GIAConfig()
    conf.update()
    print(conf.config___DEBUG)
    conf.update()
    print(conf.config___DEBUG)