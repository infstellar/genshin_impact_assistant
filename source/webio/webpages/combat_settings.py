from source.util import *
from pywebio import *
from source.webio.util import *
from source.webio.webpages.config import ConfigPage
from source.config.cvars import *




class CombatSettingPage(ConfigPage):
    def __init__(self):
        super().__init__(config_file_name = CONFIGNAME_COMBAT)
        from source.common.lang_data import get_all_characters_name
        self.character_names = get_all_characters_name()
        self.input_verify={
            "character_name":self.character_names
        }
        
    def _autofill(self):
        j = self.get_json(json.load(open(self.file_name, 'r', encoding='utf8')))
        for i in j:
            if 'long_attack_time' not in i:
                j[i]["long_attack_time"]=2.5
        autofill_j = load_json("characters_parameters.json", f"{ASSETS_PATH}\\characters_data")
        not_found = []
            
        from source.common.lang_data import translate_character_auto
        for i in j:
            cname = translate_character_auto(j[i]["name"])
            if cname is None:
                not_found.append(j[i]["name"])
                continue
            if cname in autofill_j:
                for k in ["position", "E_short_cd_time", "E_long_cd_time", "Elast_time", "Epress_time", "tactic_group", "trigger", "Qlast_time", "Qcd_time", "vision", "long_attack_time"]:
                    if j[i][k] == "" or j[i][k] == -1:
                        j[i][k] = autofill_j[cname][k]
            else:
                not_found.append(cname)
        output.clear_scope('now')
        if len(not_found)==0:
            output.popup("自动填充", "自动填充成功\n以下选项不会自动填充:\n优先级,角色在队伍中的位置。\n记得保存(￣▽￣)~*")
        else:
            output.popup("自动填充", 
                         "自动填充部分失败\n"+
                         str(not_found)+"\n"+
                         "以下选项不会自动填充:\n优先级,角色在队伍中的位置。\n记得保存(￣▽￣)~*")
        self.put_setting(name=self.file_name, j=j)

    def _load_config_files(self):
        self.config_files = []
        for root, dirs, files in os.walk('config\\tactic'):
            for f in files:
                if f[f.index('.') + 1:] == "json":
                    self.config_files.append({"label": f, "value": os.path.join(root, f)})
        self.config_files.append({"label": f"{CONFIGNAME_COMBAT}.json", "value": fr"config/settings/{CONFIGNAME_COMBAT}.json"})

    def _load(self):
        self.last_file = None

        # 添加team.json
        output.put_markdown(t2t('# Add team'), scope=self.main_scope)

        # 添加team.json按钮
        output.put_row([
            output.put_button(t2t("Add team"), onclick=self.onclick_add_teamjson),
            None,
            output.put_button(t2t("自动填充"), onclick=self._autofill)],
            scope=self.main_scope, size="10% 10px 20%")

        # 配置页
        output.put_markdown(t2t('## config:'), scope=self.main_scope)
        output.put_scope("select_scope", scope=self.main_scope)
        pin.put_select('file', self._config_file2lableAfile(self.config_files), scope="select_scope", value="config/settings/Combat.json")

    def onclick_add_teamjson(self):
        n = input.input('team name')
        shutil.copy(os.path.join(ROOT_PATH, "config\\tactic\\team.uijsontemplate"),
                    os.path.join(ROOT_PATH, "config\\tactic", n + '.json'))
        self._reload_select()

    def onclick_add_teamjson_withcharacters(self):
        n = input.input('team name')
        shutil.copy(os.path.join(ROOT_PATH, "config\\tactic\\team_with_characters.uijsontemplate"),
                    os.path.join(ROOT_PATH, "config\\tactic", n + '.json'))
        self._reload_select()
        pass