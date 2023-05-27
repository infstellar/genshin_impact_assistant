from source.util import *
from pywebio import *
from source.webio.util import *

import hashlib
import json
import os
import socket
import threading
import time

from source import listening, webio
from source.webio import manager
from source.webio.advance_page import AdvancePage
from source.funclib import collector_lib
from source.common import timer_module
from source.webio.update_notice import upd_message
from source.config.cvars import *



# from source.webio.log_handler import webio_poster


class MainPage(AdvancePage):
    def __init__(self):
        super().__init__()
        self.log_list = []
        self.log_history = []
        self.log_list_lock = threading.Lock()
        self.ui_statement = -1
        self.refresh_flow_info_timer = timer_module.Timer()
        self.ui_mission_select = ""
        self.is_task_start = False

    # todo:多语言支持

    def _on_load(self):  # 加载事件
        super()._on_load()
        pin.pin['FlowMode'] = listening.current_flow

    def _event_thread(self):
        while self.loaded:  # 当界面被加载时循环运行
            try:
                pin.pin['isSessionExist']
            except SessionNotFoundException:
                logger.info(t2t("未找到会话，可能由于窗口关闭。请刷新页面重试。"))
                return
            except SessionClosedException:
                logger.info(t2t("未找到会话，可能由于窗口关闭。请刷新页面重试。"))
                return
            if pin.pin['FlowMode'] != listening.current_flow:  # 比较变更是否被应用
                listening.current_flow = pin.pin['FlowMode']  # 应用变更
                self.log_list_lock.acquire()
                output.put_text(t2t("正在导入模块, 可能需要一些时间。"), scope='LogArea').style(
                    f'color: black; font_size: 20px')
                output.put_text(t2t("在导入完成前，请不要切换页面。"), scope='LogArea').style(
                    f'color: black; font_size: 20px')
                self.log_list_lock.release()
                listening.call_you_import_module()
            if pin.pin["MissionSelect"] != self.ui_mission_select:
                self.ui_mission_select = pin.pin["MissionSelect"]
                output.clear_scope("SCOPEMissionIntroduction")
                if self.ui_mission_select is None:
                    continue
                # output.put_text(self._get_mission_groups_dict()["introduction"][GLOBAL_LANG],scope="SCOPEMissionIntroduction")
            
            self.log_list_lock.acquire()
            for text, color in self.log_list:
                if text == "$$end$$":
                    output.put_text("", scope='LogArea')
                else:
                    output.put_text(text, scope='LogArea', inline=True).style(f'color: {color}; font_size: 20px') # ; background: aqua
            
            self.log_list.clear()
            self.log_list_lock.release()

            if self.refresh_flow_info_timer.get_diff_time() >= 0.2:
                self.refresh_flow_info_timer.reset()
                if listening.TASK_MANAGER.get_task_statement() != self.ui_statement:
                    self.ui_statement = listening.TASK_MANAGER.get_task_statement()
                    output.clear(scope="StateArea")
                    # if isinstance(self.ui_statement, list):
                    #     for i in self.ui_statement:
                    #         output.put_text(f'{i["name"]}: {i["statement"]}: {i["rfc"]}', scope="StateArea")
                    # elif isinstance(self.ui_statement, str):
                    output.put_text(f'{self.ui_statement}', scope="StateArea")

                if listening.TASK_MANAGER.start_tasklist_flag != self.is_task_start:
                    self.is_task_start = listening.TASK_MANAGER.start_tasklist_flag
                    output.clear('Button_StartStop')
                    output.put_button(label=str(listening.TASK_MANAGER.start_tasklist_flag), onclick=self.on_click_startstop,
                          scope='Button_StartStop')

            
            time.sleep(0.1)
    
    def _load(self):
        # 标题
        # 获得链接按钮
        output.put_button(label=t2t("Get IP address"), onclick=self.on_click_ip_address, scope=self.main_scope)

        task_options = [
                {
                    "label":t2t("Launch genshin"),
                    "value":"LaunchGenshinTask"
                },
                {
                    "label":t2t("Domain Task"),
                    "value":"DomainTask"
                },
                {
                    "label":t2t("Daily Commission"),
                    "value":"CommissionTask"
                },
                {
                    "label":t2t("Claim Reward"),
                    "value":"ClaimRewardTask"
                },
                {
                    "label":t2t("Ley Line Outcrop"),
                    "value":"LeyLineOutcropTask"
                },
                {
                    "label":t2t("Mission"),
                    "value":"MissionTask"
                }
            ]
        output.put_row([  # 横列
            output.put_column([  # 左竖列
                output.put_markdown('## '+t2t("Task List")),
                output.put_markdown(t2t("Can only be activated from the button")),
                pin.put_checkbox(name="task_list", options=task_options),
                output.put_row([output.put_text(t2t('启动/停止Task')), None, output.put_scope('Button_StartStop')],size='40% 10px 60%'),
                output.put_markdown(t2t('## Statement')),
                output.put_row([output.put_text(t2t('任务状态')), None, output.put_scope('StateArea')],size='40% 10px 60%'),
                # output.put_markdown(t2t('## Mission')),  # 左竖列标题
                # Mission select
                # output.put_row([  # 5%
                #     output.put_text(t2t('Mission Group')),
                #     output.put_column([
                #         pin.put_select("MissionSelect",self._get_mission_groups_config()),
                #         output.put_scope("SCOPEMissionIntroduction")
                #         ])
                # ]),
                output.put_markdown(t2t('## Function')),  # 左竖列标题
                output.put_markdown(t2t("Can only be activated from the hotkey \'[\'")),
                output.put_row([  # FlowMode
                    output.put_text(t2t('FlowMode')),
                    pin.put_select(('FlowMode'), [
                        {'label': t2t('Idle'), 'value': listening.FLOW_IDLE},
                        {'label': t2t('AutoCombat'), 'value': listening.FLOW_COMBAT},
                        # {'label': t2t('AutoDomain'), 'value': listening.FLOW_DOMAIN},
                        # {'label': t2t('AutoCollector'), 'value': listening.FLOW_COLLECTOR}
                    ])])
            ], size='auto'), None,
            output.put_scope('Log')

        ], scope=self.main_scope, size='40% 10px 60%')

        # PickUpButton
        output.put_button(label=str(listening.FEAT_PICKUP), onclick=self.on_click_pickup, scope='Button_PickUp')
        # Button_StartStop
        output.put_button(label=str(listening.startstop_flag), onclick=self.on_click_startstop,
                          scope='Button_StartStop')

        # Log
        output.put_markdown(t2t('## Log'), scope='Log')
        output.put_scrollable(output.put_scope('LogArea'), height=600, keep_bottom=True, scope='Log')
        '''self.main_pin_change_thread = threading.Thread(target=self._main_pin_change_thread, daemon=False)
        self.main_pin_change_thread.start()'''

        m = upd_message()
        if m!="":
            output.popup(t2t('更新提示'), m)
        
    # def _get_mission_groups_config(self):
    #     jsons = load_json_from_folder(f"{CONFIG_PATH}\\mission_groups")
    #     r = [i["label"] for i in jsons]
    #     return r

    # def _get_mission_groups_dict(self):
    #     jsonname = pin.pin["MissionSelect"]
    #     if jsonname is None:
    #         raise FileNotFoundError
    #     return load_json(str(jsonname),default_path=f"{CONFIG_PATH}\\mission_groups")
    
    def on_click_pickup(self):
        output.clear('Button_PickUp')
        listening.FEAT_PICKUP = not listening.FEAT_PICKUP
        output.put_button(label=str(listening.FEAT_PICKUP), onclick=self.on_click_pickup, scope='Button_PickUp')
    
    def on_click_startstop(self):
        # listening.MISSION_MANAGER.set_mission_list(list(pin.pin["MissionSelect"]))
        listening.TASK_MANAGER.set_tasklist(pin.pin["task_list"])
        listening.TASK_MANAGER.start_stop_tasklist()
        if pin.pin["MissionSelect"] != None and pin.pin["MissionSelect"] != "":
            cj = load_json()
            cj["MissionGroup"] = pin.pin["MissionSelect"]
            save_json(cj)
            GIAconfig.update()

        time.sleep(0.2)
        output.clear('Button_StartStop')
        output.put_button(label=str(listening.TASK_MANAGER.start_tasklist_flag), onclick=self.on_click_startstop,
                          scope='Button_StartStop')

    def on_click_ip_address(self):
        LAN_ip = f"{socket.gethostbyname(socket.gethostname())}{session.info.server_host[session.info.server_host.index(':'):]}"
        WAN_ip = t2t("Not Enabled")
        output_text = t2t('LAN IP') + " : " + LAN_ip + '\n' + t2t("WAN IP") + ' : ' + WAN_ip
        output.popup(f'ip address', output_text, size=output.PopupSize.SMALL)

    def logout(self, text: str, color='black'):
        if self.loaded:
            self.log_list_lock.acquire()
            self.log_list.append((text, color))
            self.log_list_lock.release()


class ConfigPage(AdvancePage):
    def __init__(self, config_file_name):
        super().__init__()

        # self.main_scope = "SettingPage"

        self.exit_popup = None
        self.last_file = None
        self.file_name = ''
        self.config_file_name = config_file_name

        self.config_files = []
        self.config_files_name = []
        self._load_config_files()
        self.can_check_select = True
        self.can_remove_last_scope = False
        # 注释显示模式在这改
        self.mode = True
        self.read_only = False

        self.input_verify={
            "test":lambda x:x
        }

    def _load_config_files(self):
        for root, dirs, files in os.walk('config'):
            for f in files:
                if f[f.index('.') + 1:] == "json":
                    self.config_files.append({"label": f, "value": os.path.join(root, f)})

    def _load(self):
        self.last_file = None

        # 配置页
        output.put_markdown(t2t('## config:'), scope=self.main_scope)

        output.put_scope("select_scope", scope=self.main_scope)
        pin.put_select('file', self._config_file2lableAfile(self.config_files), scope="select_scope")

    def _config_file2lableAfile(self, l1):
        replace_dict = {
            "Combat.json": t2t("Combat.json"),
            "Domain.json": t2t("Domain.json"),
            "General.json": t2t("General.json"),
            "Keymap.json": t2t("Keymap.json"),
            "collected.json": t2t("collected.json"),
            "collection_blacklist.json": t2t("collection_blacklist.json"),
            "collection_log.json": t2t("collection_log.json"),
            "Collector.json": t2t("Collector.json"),
            "LeyLineOutcrop.json": t2t("LeyLineOutcrop.json")
        }
        
        for i in range(len(l1)):
            l1[i]["label"] = replace_dict.setdefault(l1[i]["label"], l1[i]["label"])
        return l1
    
    # 重新加载选项
    def _reload_select(self):
        self.can_check_select = False
        self._load_config_files()
        output.clear("select_scope")
        pin.put_select('file', self._config_file2lableAfile(self.config_files), scope="select_scope")
        self.can_check_select = True
    
    # 循环线程
    def _event_thread(self):
        while self.loaded:
            if not self.can_check_select:
                time.sleep(1)
                continue
            try:
                pin.pin['isSessionExist']
            except SessionNotFoundException:
                logger.info(t2t("未找到会话，可能由于窗口关闭。请刷新页面重试。"))
                return
                
            if pin.pin['file'] != self.last_file:  # 当下拉框被更改时
                self.last_file = pin.pin['file']

                if self.can_remove_last_scope:  # 判断是否可以移除
                    output.remove('now')
                else:
                    self.can_remove_last_scope = True

                output.put_scope('now', scope=self.main_scope)  # 创建配置页scope
                
                
                self.put_setting(pin.pin['file'])  # 配置配置页

            time.sleep(1)

    def _str_verify(self, x, verify_list, scope_name):
        if x in verify_list:
            output.clear_scope(scope_name)
            output.put_text(t2t("Verified!"), scope=scope_name).style(f'color: green; font_size: 20px')
            return
        else:
            f1 = False
            sl = []
            for i in verify_list:
                if x in i:
                    f1 = True
                    output.clear_scope(scope_name)
                    output.put_text(t2t("Waiting..."), scope=scope_name).style(f'color: black; font_size: 20px')
                    if len(sl)<=15:
                        sl.append(i)
            
        if f1:
            output.put_text(t2t("You may want to enter: "), scope=scope_name).style(f'color: black; font_size: 20px')
            for i in sl:
                output.put_text(i, scope=scope_name).style(f'color: black; font_size: 12px; font-style:italic')
        else:
            output.clear_scope(scope_name)
            output.put_text(t2t("Not a valid name"), scope=scope_name).style(f'color: red; font_size: 20px')

    def _before_load_json(self):
        pass
     
    def put_setting(self, name='', j=None):
        self.file_name = name
        self._before_load_json()
        output.put_markdown('## {}'.format(name), scope='now')  # 标题
        if j is None:
            with open(name, 'r', encoding='utf8') as f:
                j = json.load(f)

        # with open(os.path.join(root_path, "config", "settings", "config.json"), 'r', encoding='utf8') as f:
        #     lang = json.load(f)["lang"]
        doc_name = f'config\\json_doc\\{self.config_file_name}.yaml'
        lang_doc_name = f'config\\json_doc\\{self.config_file_name}.{GLOBAL_LANG}.yaml'

        if os.path.exists(doc_name):
            with open(doc_name, 'r', encoding='utf8') as f:
                doc = yaml.load(f, Loader=yaml.FullLoader)
            if os.path.exists(lang_doc_name):
                with open(lang_doc_name, 'r', encoding='utf8') as f:
                    doc_addi = yaml.load(f, Loader=yaml.FullLoader)
                for k1 in doc_addi:
                    for k2 in doc_addi[k1]:
                        if k1 not in doc:
                            doc[k1] = doc_addi[k1]
                        doc[k1][k2] = doc_addi[k1][k2]
        else:
            doc = {}
        self.put_json(j, doc, 'now', level=3)  # 载入json
        
        if not self.read_only:
            output.put_button('save', scope='now', onclick=self.save)

    # 保存json文件
    def save(self):

        j = json.load(open(self.file_name, 'r', encoding='utf8'))

        json.dump(self.get_json(j), open(self.file_name, 'w', encoding='utf8'), ensure_ascii=False, indent=4)
        # output.put_text('saved!', scope='now')
        output.toast(t2t('saved!'))
        GIAconfig.update()

    # 
    def get_json(self, j: dict, add_name=''):
        rt_json = {}
        for k in j:
            k_sha1 = hashlib.sha1(k.encode('utf8')).hexdigest()
            v = j[k]
            if type(v) == dict:
                rt_json[k] = self.get_json(v, add_name='{}-{}'.format(add_name, k_sha1))

            elif type(v) == list:

                # 判断是否为dict列表
                is_dict_list = True
                for i in v:
                    is_dict_list = is_dict_list and (type(i) == dict)

                if is_dict_list:
                    # 这个是dict的id,是在列表的位置,从1开始,当然也可以改成从0开始,都一样
                    dict_id = 0
                    # 在当前dict列表里循环,取出每一个dict
                    rt_list = []
                    for i in v:
                        # 计次+1
                        dict_id += 1
                        rt_list.append(
                            self.get_json(v[dict_id - 1], add_name='{}-{}-{}'.format(add_name, k_sha1, str(dict_id))))
                    rt_json[k] = rt_list
                else:
                    rt_json[k] = list_text2list(pin.pin['{}-{}'.format(add_name, k_sha1)])
            else:
                rt_json[k] = pin.pin['{}-{}'.format(add_name, k_sha1)]

        return rt_json

    def _on_unload(self):
        if not self.read_only:
            j = json.load(open(self.file_name, 'r', encoding='utf8'))
            self.exit_popup = True
            if not is_json_equal(json.dumps(self.get_json(j)), json.dumps(j)):
                self.exit_popup = False
                output.popup(t2t('Do you need to save changes?'), [
                    output.put_buttons([(t2t('No'), 'No'), (t2t('Yes'), 'Yes')], onclick=self.popup_button)
                ])
            while not self.exit_popup:
                time.sleep(0.1)

    def popup_button(self, val):
        if val == 'No':
            self.close_popup()
        elif val == 'Yes':
            self.save_and_exit_popup()

    def save_and_exit_popup(self):
        self.save()
        output.close_popup()
        self.exit_popup = True

    def close_popup(self):
        output.close_popup()
        self.exit_popup = True
    
    # 展示str型项
    def _show_str(self, doc_items, component_name, display_name, scope_name, v, doc_special):
        if doc_items:
            pin.put_select(component_name,
                            [{"label": i, "value": i} for i in doc_items], value=v,
                            label=display_name,
                            scope=scope_name)
        elif doc_special:
            doc_special = doc_special.split('#')
            if doc_special[0] == "$FILE_IN_FOLDER$":
                
                json_dict = load_json_from_folder(os.path.join(ROOT_PATH, doc_special[1]), black_file=["character","character_dist",""])
                sl = []
                for i in json_dict:
                    sl.append({"label": i["label"], "value": i["label"]})
                pin.put_select(component_name,
                    sl, value=v,
                    label=display_name,
                    scope=scope_name)
            elif doc_special[0] == "$INPUT_VERIFY$":
                pin.put_input(component_name, label=display_name, value=v, scope=scope_name)
                output.put_scope(name=component_name, content=[
                    output.put_text("")
                ], scope=scope_name)
                def onchange(x):
                    self._str_verify(x, verify_list=self.input_verify[doc_special[1]], scope_name=component_name)
                pin.pin_on_change(component_name, onchange=onchange, clear=False, init_run=True)
        else:
            pin.put_input(component_name, label=display_name, value=v, scope=scope_name)
    
    # 展示inf型项
    def _show_int(self, doc_items, component_name, display_name, scope_name, v, doc_special):
        if doc_items:
            pin.put_select(component_name,
                            [{"label": i, "value": i} for i in doc_items], value=v,
                            label=display_name,
                            scope=scope_name)
        else:
            pin.put_input(component_name, label=display_name, value=v, scope=scope_name, type='number')
    
    # 展示float型项
    def _show_float(self, doc_items, component_name, display_name, scope_name, v, doc_special):
        if doc_items:
            pin.put_select(component_name,
                            [{"label": i, "value": i} for i in doc_items], value=v,
                            label=display_name,
                            scope=scope_name)
        else:
            pin.put_input(component_name, label=display_name, value=v, scope=scope_name, type='float')
    
    # 展示bool型项
    def _show_bool(self, component_name, display_name, scope_name, v, doc_special):
        pin.put_select(component_name,
            [{"label": 'True', "value": True}, {"label": 'False', "value": False}], value=v,
            label=display_name,
            scope=scope_name)
    
    # 展示dict型项
    def _show_dict(self, level, component_name, display_name, scope_name, doc, v, doc_special):
        output.put_scope(component_name, scope=scope_name)
        output.put_markdown('#' * level + ' ' + display_name, scope=component_name)
        self.put_json(v, doc, component_name, add_name=component_name,
                        level=level + 1)
    
    # 展示list/list&dict型项
    def _show_list(self, level, display_name, scope_name, component_name, doc, v, doc_special):
        # 判断是否为dict列表
        is_dict_list = True
        for i in v:
            is_dict_list = is_dict_list and (type(i) == dict)

        if is_dict_list:
            output.put_markdown('#' * level + ' ' + display_name,
                                scope=scope_name)
            # 差点把我绕晕....
            # 这个是dict的id,是在列表的位置,从1开始,当然也可以改成从0开始,都一样
            dict_id = 0
            # 在当前dict列表里循环,取出每一个dict
            for i in v:
                # 计次+1
                dict_id += 1

                # 创建一个容器以容纳接下来的dict,第一个是控件名称,为了防止重复,加上了dict id,后面那个是当前容器id
                output.put_scope(component_name + '-' + str(dict_id), scope=scope_name)
                # 写标题,第一项是标题文本,遵守markdown语法,第二项是当前容器名称
                output.put_markdown('#' * (level + 1) + ' ' + str(dict_id),
                                    scope=component_name + '-' + str(dict_id))
                # 写dict,第一项为输入的dict,第二项为doc,第三项为当前容器名称,第四项为控件名称前缀,最后是缩进等级
                self.put_json(i, doc, component_name + '-' + str(dict_id),
                                component_name + '-' + str(dict_id),
                                level=level + 2)
        else:
            pin.put_textarea(component_name, label=display_name, value=list2format_list_text(v),
                                scope=scope_name)
    
    # 显示json
    def put_json(self, j: dict, doc: dict, scope_name, add_name='', level=1):
        for k in j:
            v = j[k]
            # 获取注释
            doc_now = ''
            doc_now_data = {}
            doc_items = None
            doc_special = None
            doc_annotation = None
            if k in doc:
                # 判断doc的类型
                if type(doc[k]) == dict:
                    if 'doc' in doc[k]:
                        doc_now = doc[k]['doc']
                    if 'data' in doc[k]:
                        doc_now_data = doc[k]['data']
                    if 'select_items' in doc[k]:
                        doc_items = doc[k]['select_items']
                    if 'special_index' in doc[k]:
                        doc_special = doc[k]['special_index']
                    if "annotation" in doc[k]:
                        doc_annotation = doc[k]['annotation']
                if type(doc[k]) == str:
                    doc_now = doc[k]
            # 取显示名称
            display_name = doc_now if doc_now else k if self.mode else '{} {}'.format(k, doc_now)

            k_sha1 = hashlib.sha1(k.encode('utf8')).hexdigest()
            component_name = '{}-{}'.format(add_name, k_sha1)
            
            
            if type(v) == str or v is None:
                self._show_str(doc_items, component_name, display_name, scope_name, v, doc_special)
            elif type(v) == int:
                self._show_int(doc_items, component_name, display_name, scope_name, v, doc_special)
            elif type(v) == float:
                self._show_float(doc_items, component_name, display_name, scope_name, v, doc_special)
            elif type(v) == bool:
                self._show_bool(component_name, display_name, scope_name, v, doc_special)
            elif type(v) == dict:
                self._show_dict(level, component_name, display_name, scope_name, doc, v, doc_special)
            elif type(v) == list:
                self._show_list(level, display_name, scope_name, component_name, doc, v, doc_special)
            if doc_annotation != None:
                    output.put_text(doc_annotation, scope=scope_name)
                    output.put_text("\n", scope=scope_name).style("font-size: 1px")

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
        for i in [CONFIGNAME_GENERAL, CONFIGNAME_DOMAIN, CONFIGNAME_KEYMAP, CONFIGNAME_LEY_LINE_OUTCROP]:
            self.config_files.append({"label": f"{i}.json", "value": os.path.join(fr"{CONFIG_PATH_SETTING}", f"{i}.json")})
        

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
        autofill_j = load_json("characters_parameters.json", f"{ASSETS_PATH}\\characters_data")
        not_found = []
            
        from source.common.lang_data import translate_character_auto
        for i in j:
            cname = translate_character_auto(j[i]["name"])
            if cname is None:
                not_found.append(j[i]["name"])
                continue
            if cname in autofill_j:
                for k in ["position", "E_short_cd_time", "E_long_cd_time", "Elast_time", "Epress_time", "tactic_group", "trigger", "Qlast_time", "Qcd_time", "vision"]:
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
        pin.put_select('file', self._config_file2lableAfile(self.config_files), scope="select_scope", value="config\\settings\\auto_combat.json")

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

class CollectorSettingPage(ConfigPage):
    def __init__(self):
        super().__init__(config_file_name = CONFIGNAME_COLLECTOR)
        self.collection_names = load_json("ITEM_NAME.json", f"assets\\POI_JSON_API\\{GLOBAL_LANG}")

    def _load_config_files(self):
        self.config_files = []
        for root, dirs, files in os.walk('config\\auto_collector'):
            for f in files:
                if f[f.index('.') + 1:] == "json":
                    self.config_files.append({"label": f, "value": os.path.join(root, f)})
        self.config_files.append({"label": f"{CONFIGNAME_COLLECTOR}.json", "value": os.path.join(fr"config/settings/{CONFIGNAME_COLLECTOR}.json")})

    # 重置列表
    @staticmethod
    def _reset_list_textarea(x):
        pin.pin[x] = "[\n\n]"
    
    def _load(self):
        self.last_file = None

        # 配置页
        output.put_markdown(t2t('## config:'), scope=self.main_scope)
        output.put_scope("select_scope", scope=self.main_scope)
        pin.put_select('file', self._config_file2lableAfile(self.config_files), scope="select_scope", value="config\\settings\\auto_collector.json")
    
    def _clean_textarea(self, set_value):
        set_value("")
    
    def _onclick_col_log_operate(self, btn_value:str):
        if btn_value == "$COLLECTED$":
            collector_lib.generate_collected_from_log()
            toast_succ()
        elif btn_value == "$BLACKLIST$":
            collector_lib.generate_masked_col_from_log()
            toast_succ()
    
    def _before_load_json(self):
        if "collection_log.json" in self.file_name:
            self.read_only = True
            # output.put_buttons([
                
            #     (_("Automatic generate a list of collected items"), "$COLLECTED$"),
            #     (_("Automatic generate a list of blacklist items"), "$BLACKLIST$")
            #     ], 
            #     onclick=self._onclick_col_log_operate,
            #     scope="now"
            # )
        else:
            self.read_only = False
        return super()._before_load_json()
    
    def _on_click_collectionlog(self, btn_value:str):
        # btn value: $AddToBlackList$#KEY#ID
        collect_key = btn_value.split('#')[1]
        collect_id = int(btn_value.split('#')[2])
        if "$AddToBlackList$" in btn_value:
            collector_lib.add_to_blacklist(collect_key, collect_id)
            toast_succ()
        elif "$AddToCollected$" in btn_value:
            collector_lib.add_to_collected(collect_key, collect_id)
            toast_succ()
            
        
    def _show_list(self, level, display_name, scope_name, component_name, doc, v, doc_special):
        # 判断是否为dict列表
        is_dict_list = True
        for i in v:
            is_dict_list = is_dict_list and (type(i) == dict)

        if is_dict_list:
            
            output.put_markdown('#' * level + ' ' + display_name,
                                scope=scope_name)
            if "collection_log.json" in self.file_name:
                for iii in range(len(v)):
                    v[iii]["picked item"] = str(v[iii]["picked item"])
                v = v[::-1]
                show_list = []
                for iii in range(len(v)):
                    ctime = v[iii]["time"][:v[iii]["time"].index('.')]
                    show_list.append( [v[iii]["error_code"], v[iii]["id"], v[iii]["picked item"], ctime, 
                                 output.put_buttons([
                                     (t2t("Add to blacklist"), f"$AddToBlackList$#{display_name}#{v[iii]['id']}"),
                                     # (_("Add to collected"), f"$AddToCollected$#{display_name}#{v[iii]['id']}")
                                     ],
                                 onclick=self._on_click_collectionlog, small=True)])
                a1,a2,a3,a4 = collector_lib.col_succ_times_from_log(display_name, day=1)
                b1,b2,b3,b4 = collector_lib.col_succ_times_from_log(display_name, day=7)
                c1,c2,c3,c4 = collector_lib.col_succ_times_from_log(display_name, day=15)
                d1,d2,d3,d4 = collector_lib.col_succ_times_from_log(display_name, day=900)
                output.put_collapse(t2t("展开/收起"), [
                    
                    output.put_text(f"{t2t('Within')} 1   {t2t('day(s)')} {t2t('success rate')}:{a1} {t2t('total num')}:{a2} {t2t('success num')}:{a3} {t2t('fail num')}:{a4}"),
                    output.put_text(f"{t2t('Within')} 7   {t2t('day(s)')} {t2t('success rate')}:{b1} {t2t('total num')}:{b2} {t2t('success num')}:{b3} {t2t('fail num')}:{b4}"),
                    output.put_text(f"{t2t('Within')} 15  {t2t('day(s)')} {t2t('success rate')}:{c1} {t2t('total num')}:{c2} {t2t('success num')}:{c3} {t2t('fail num')}:{c4}"),
                    output.put_text(f"{t2t('Within')} 900 {t2t('day(s)')} {t2t('success rate')}:{d1} {t2t('total num')}:{d2} {t2t('success num')}:{d3} {t2t('fail num')}:{d4}"),
                    output.put_table(show_list, header=["error_code", "id", "picked item", "time", "buttons"])
                ], scope=scope_name)
                
                
            else:
                # 差点把我绕晕....
                # 这个是dict的id,是在列表的位置,从1开始,当然也可以改成从0开始,都一样
                dict_id = 0
                # 在当前dict列表里循环,取出每一个dict
                for i in v:
                    # 计次+1
                    dict_id += 1
                    
                    
                # 创建一个容器以容纳接下来的dict,第一个是控件名称,为了防止重复,加上了dict id,后面那个是当前容器id
                    output.put_scope(component_name + '-' + str(dict_id), scope=scope_name)
                    # 写标题,第一项是标题文本,遵守markdown语法,第二项是当前容器名称
                    output.put_markdown('#' * (level + 1) + ' ' + str(dict_id),
                                        scope=component_name + '-' + str(dict_id))
                    # 写dict,第一项为输入的dict,第二项为doc,第三项为当前容器名称,第四项为控件名称前缀,最后是缩进等级
                    self.put_json(i, doc, component_name + '-' + str(dict_id),
                                    component_name + '-' + str(dict_id),
                                    level=level + 2)
        else:
            # 清除按钮
            if "collected.json" in self.file_name:
                output.put_row([
                    pin.put_textarea(component_name, label=display_name, value=list2format_list_text(v)),
                    None,
                    output.put_button(t2t("clean list"), onclick=lambda:self._reset_list_textarea(component_name))
                    ]
                , scope=scope_name,size="85% 5% 10%")
            elif "collection_log.json" in self.file_name:
                # output.put_table()
                output.put_text(f"{display_name} : {list2format_list_text(v, inline=True)}", scope=scope_name)
            else:
                pin.put_textarea(component_name, label=display_name, value=list2format_list_text(v), scope=scope_name)
                
    def _onchange_collection_name(self, x):
        if x in self.collection_names:
            output.clear_scope("PREDICT_AND_VERIFY_01_scope")
            output.put_text(t2t("Verified!"), scope="PREDICT_AND_VERIFY_01_scope").style(f'color: green; font_size: 20px')
            return
        else:
            f1 = False
            sl = []
            for i in self.collection_names:
                if x in i:
                    f1 = True
                    output.clear_scope("PREDICT_AND_VERIFY_01_scope")
                    output.put_text(t2t("Waiting..."), scope="PREDICT_AND_VERIFY_01_scope").style(f'color: black; font_size: 20px')
                    if len(sl)<=15:
                        sl.append(i)
            
        if f1:
            output.put_text(t2t("You may want to enter: "), scope="PREDICT_AND_VERIFY_01_scope").style(f'color: black; font_size: 20px')
            for i in sl:
                output.put_text(i, scope="PREDICT_AND_VERIFY_01_scope").style(f'color: black; font_size: 12px; font-style:italic')
        else:
            output.clear_scope("PREDICT_AND_VERIFY_01_scope")
            output.put_text(t2t("Not a valid name"), scope="PREDICT_AND_VERIFY_01_scope").style(f'color: red; font_size: 20px')
    
    def _show_str(self, doc_items, component_name, display_name, scope_name, v, doc_special):
        if doc_items:
            pin.put_select(component_name,
                            [{"label": i, "value": i} for i in doc_items], value=v,
                            label=display_name,
                            scope=scope_name)
        elif doc_special:
            if doc_special == "$PREDICT_AND_VERIFY_01$":
                pin.put_input(component_name, label=display_name, value=v, scope=scope_name)
                output.put_scope(name="PREDICT_AND_VERIFY_01_scope", content=[
                    output.put_text("")
                ], scope=scope_name)
                pin.pin_on_change(component_name, onchange=self._onchange_collection_name, clear=False, init_run=True)
        else:
            if "collection_log.json" in self.file_name:
                output.put_text(f"{display_name} : {v}", scope=scope_name)
            else:
                pin.put_input(component_name, label=display_name, value=v, scope=scope_name)
    
    # 展示inf型项
    def _show_int(self, doc_items, component_name, display_name, scope_name, v, doc_special):
        if doc_items:
            pin.put_select(component_name,
                            [{"label": i, "value": i} for i in doc_items], value=v,
                            label=display_name,
                            scope=scope_name)
        else:
            if "collection_log.json" in self.file_name:
                output.put_text(f"{display_name} : {v}", scope=scope_name)
            else:
                pin.put_input(component_name, label=display_name, value=v, scope=scope_name, type='number')



    