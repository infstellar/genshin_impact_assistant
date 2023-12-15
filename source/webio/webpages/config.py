from source.util import *
from pywebio import *
from source.webio.util import *
import hashlib
import json
import os
import time
from source.webio.advance_page import AdvancePage
from source.config.cvars import *


class ConfigPage(AdvancePage):
    def __init__(self, config_file_name):
        pin.pin.use_strict()
        super().__init__(document_link=f'https://genshinimpactassistant.github.io/GIA-Document/#/{GLOBAL_LANG}/gui')

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
            except AssertionError:
                pass
                
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
        output.toast(t2t('saved!'), color='success', duration=4)
        output.toast(t2t('You may need to restart to apply changes.'), duration=4)
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
                try:
                    pin_value = pin.pin['{}-{}'.format(add_name, k_sha1)]
                    rt_json[k] = pin_value
                except AssertionError:
                    logger.debug(f'the value of {k} is empty, probably it is hidden.')
                    rt_json[k] = j[k]

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
            doc_type = None
            doc_conceal = False
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
                    if 'type' in doc[k]:
                        doc_type = doc[k]['type']
                    if 'conceal' in doc[k]:
                        doc_conceal = True
                if type(doc[k]) == str:
                    doc_now = doc[k]
            # 取显示名称
            display_name = doc_now if doc_now else k if self.mode else '{} {}'.format(k, doc_now)

            k_sha1 = hashlib.sha1(k.encode('utf8')).hexdigest()
            component_name = '{}-{}'.format(add_name, k_sha1)
            if doc_conceal:
                continue
            if doc_type != None:
                if doc_type == 'int':
                    self._show_int(doc_items, component_name, display_name, scope_name, v, doc_special)
                elif doc_type == 'float':
                    self._show_float(doc_items, component_name, display_name, scope_name, v, doc_special)
                elif doc_type == 'bool':
                    self._show_bool(component_name, display_name, scope_name, v, doc_special)
                elif doc_type == 'dict':
                    self._show_dict(level, component_name, display_name, scope_name, doc, v, doc_special)
                elif doc_type == 'list':
                    self._show_list(level, display_name, scope_name, component_name, doc, v, doc_special)
                elif doc_type == 'str':
                    self._show_str(doc_items, component_name, display_name, scope_name, v, doc_special)
            else:    
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
                    output.put_markdown(doc_annotation, scope=scope_name)
                    output.put_text("\n", scope=scope_name).style("font-size: 1px")

