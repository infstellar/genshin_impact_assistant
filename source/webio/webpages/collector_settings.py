from source.util import *
from pywebio import *
from source.webio.util import *
from source.webio.webpages.config import ConfigPage
from source.config.cvars import *
from source.funclib import collector_lib



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
        if x == '':
            output.clear("PREDICT_AND_VERIFY_01_scope")
            output.put_text(t2t("Waiting..."), scope="PREDICT_AND_VERIFY_01_scope").style(f'color: black; font_size: 20px')
            return
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