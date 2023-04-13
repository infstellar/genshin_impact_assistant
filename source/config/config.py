# from source.util import *
from source.path_lib import *
from source.config.util import *
from source.config.config_generated import GeneratedConfig



class ReadOnlyError(Exception):
    pass

class GIAConfig(GeneratedConfig):
    bound = {}
    TRACE = False

    def __init__(self) -> None:
        super().__init__()
        self.merge()
        self.load()

    def __setattr__(self, key, value, read_only=True):
        if not read_only:
            super().__setattr__(key, value)
        else:
            raise ReadOnlyError

    def load(self):
        for jsonname in CONFIG_FILE_NAMES:
            j = load_json(json_name=f"{jsonname}.json", default_path=fr"{CONFIG_PATH}/settings")
            for k in j:
                # if f"{jsonname}_{k}" in self.__dict__:
                self.__setattr__(f"{jsonname}_{k}", j[k], read_only=False)
                if self.TRACE:
                    print(f"set {jsonname}_{k} to {j[k]}")

    def merge(self):
        for jsonname in CONFIG_FILE_NAMES:
            j_template = load_json(json_name=f"{jsonname}.jsontemplate", default_path=fr"{CONFIG_PATH}/json_template")
            if not os.path.exists(os.path.join(fr"{CONFIG_PATH}/settings", f"{jsonname}.json")):
                j_config = {}
            else:
                j_config = load_json(json_name=f"{jsonname}.json", default_path=fr"{CONFIG_PATH}/settings")
            j_template.update(j_config)
            # for k in j_template:
            #     if k in j_config:
            #         j_template[k] = j_config[k]
            #         if self.TRACE: print(f"{j_template[k]} = {j_config[k]}")
            save_json(j_template, json_name=f"{jsonname}.json", default_path=fr"{CONFIG_PATH}/settings")
    # def save(self):
    #     var_names = [f"{i}_" for i in CONFIG_FILE_NAMES]
    #     var_dicts = {}
    #     for k in self.__dict__:
    #         if f"{k.split('___')[0]}_" in var_names:
    #             var_dicts[k.split('___')[0]] = k

    def update(self):
        self.load()

GIAconfig = GIAConfig() 

if __name__ == '__main__':
    # config.merge()
    print(GIAconfig.General_CaptureMode)
    print(GIAconfig.Domain_DomainName)