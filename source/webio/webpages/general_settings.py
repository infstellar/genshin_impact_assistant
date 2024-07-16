from source.util import *
from pywebio import *
from source.webio.util import *
from source.webio.webpages.config import ConfigPage
from source.config.cvars import *


class SettingPage(ConfigPage):
    def __init__(self):
        super().__init__(config_file_name = CONFIGNAME_GENERAL)
        self.domain_name = load_json(f"Domain_Names_{GLOBAL_LANG}.json", fr"{ASSETS_PATH}/domain_names")
        self.input_verify={
            "domain_name":self.domain_name
        }

    def _load(self):
        self.last_file = None

        # 配置页
        output.put_markdown(t2t('## config:'), scope=self.main_scope)
        output.put_scope("select_scope", scope=self.main_scope)

        pin.put_select('file', self._config_file2lableAfile(self.config_files), scope="select_scope", value="config\\settings\\config.json")

    def _load_config_files(self):
        # for root, dirs, files in os.walk('config\\settings'):
        #     for f in files:
        #         if f[:f.index('.')] in ["auto_combat", "auto_collector", "auto_pickup_default_blacklist"]:
        #             continue
        #         if f[f.index('.') + 1:] == "json":
        #             self.config_files.append({"label": f, "value": os.path.join(root, f)})
        for i in [CONFIGNAME_GENERAL, CONFIGNAME_DOMAIN, CONFIGNAME_KEYMAP, CONFIGNAME_LEY_LINE_OUTCROP, CONFIGNAME_DEV]:
            self.config_files.append({"label": f"{i}.json", "value": os.path.join(fr"{CONFIG_PATH_SETTING}", f"{i}.json")})