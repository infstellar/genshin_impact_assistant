import asyncio
import json
import os
import threading
import time

from pywebio import *

from source import listening, util, webio
from source.util import is_json_equal
from source.webio import manager
from source.webio.page_manager import Page


class MainPage(Page):
    def __init__(self):
        super().__init__()

    def _on_load(self):  # 加载事件
        self._load()  # 加载主页
        t = threading.Thread(target=self._event_thread, daemon=False)  # 创建事件线程
        session.register_thread(t)  # 注册线程
        t.start()  # 启动线程

    def _event_thread(self):
        while self.loaded:  # 当界面被加载时循环运行
            if pin.pin['FlowMode'] != listening.current_flow:  # 比较变更是否被应用
                listening.current_flow = pin.pin['FlowMode']  # 应用变更
            time.sleep(0.1)

    def _load(self):
        # 标题
        output.put_markdown('# Main', scope=self.main_scope)

        # 页面切换按钮
        output.put_buttons(list(manager.page_dict), onclick=webio.manager.load_page, scope=self.main_scope)

        output.put_row([  # 横列
            output.put_column([  # 左竖列
                output.put_markdown('## Options'),  # 左竖列标题

                output.put_row([  # FlowMode
                    output.put_text('FlowMode'),
                    pin.put_select('FlowMode', [
                        {'label': 'Idle', 'value': listening.FLOW_IDLE},
                        {'label': 'AutoCombat', 'value': listening.FLOW_COMBAT},
                        {'label': 'AutoDomain', 'value': listening.FLOW_DOMAIN}
                    ])]),
                # PickUpMode
                output.put_row([output.put_text('PickUp'), output.put_scope('Button_PickUp')])

            ]), None,
            output.put_scope('Log')

        ], scope=self.main_scope)

        # PickUpButton
        output.put_button(label=str(listening.FEAT_PICKUP), onclick=self.on_click_pickup, scope='Button_PickUp')

        # Log
        output.put_markdown('## Log', scope='Log')
        output.put_scrollable(output.put_scope('LogArea'), height=300, keep_bottom=True, scope='Log')
        '''self.main_pin_change_thread = threading.Thread(target=self._main_pin_change_thread, daemon=False)
        self.main_pin_change_thread.start()'''

    def on_click_pickup(self):
        output.clear('Button_PickUp')
        listening.FEAT_PICKUP = not listening.FEAT_PICKUP
        output.put_button(label=str(listening.FEAT_PICKUP), onclick=self.on_click_pickup, scope='Button_PickUp')

    def logout(self, text: str, color='black'):
        if self.loaded:
            output.put_text(text, scope='LogArea').style(f'color: {color}')

    def _on_unload(self):
        pass


class SettingPage(Page):
    def __init__(self):
        super().__init__()
        self.exit_popup = None
        self.last_file = None
        self.file_name = ''

        self.config_files = []
        self.config_files_name = []
        for root, dirs, files in os.walk('config'):
            for f in files:
                self.config_files.append({"label": f, "value": os.path.join(root, f)})
        self.can_remove_last_scope = False

    def _load(self):
        self.last_file = None

        # 标题
        output.put_markdown('# Setting', scope=self.main_scope)

        # 页面切换按钮
        output.put_buttons(list(manager.page_dict), onclick=webio.manager.load_page, scope=self.main_scope)

        # 配置页
        output.put_markdown('## config:', scope=self.main_scope)
        pin.put_select('file', self.config_files, scope=self.main_scope)

    def _on_load(self):
        self._load()  # 加载页面
        t = threading.Thread(target=self._event_thread, daemon=False)
        session.register_thread(t)  # 注册线程
        t.start()

    def _event_thread(self):
        while self.loaded:
            if pin.pin['file'] != self.last_file:  # 当下拉框被更改时
                self.last_file = pin.pin['file']

                if self.can_remove_last_scope:  # 判断是否可以移除
                    output.remove('now')
                else:
                    self.can_remove_last_scope = True

                output.put_scope('now', scope=self.main_scope)  # 创建配置页scope

                self.put_setting(pin.pin['file'])  # 配置配置页

            time.sleep(1)

    def put_setting(self, name=''):
        self.file_name = name
        output.put_markdown('## {}'.format(name), scope='now')  # 标题
        j = json.load(open(name, 'r', encoding='utf8'))
        self.put_json(j, 'now', level=3)  # 载入json
        output.put_button('save', scope='now', onclick=self.save)

    def save(self):

        j = json.load(open(self.file_name, 'r', encoding='utf8'))

        json.dump(self.get_json(j), open(self.file_name, 'w', encoding='utf8'))
        # output.put_text('saved!', scope='now')
        output.toast('saved!')

    def get_json(self, j: dict, add_name=''):
        rt_json = {}
        for k in j:

            v = j[k]
            if type(v) == dict:
                rt_json[k] = self.get_json(v, add_name='{}-{}'.format(add_name, k))

            elif type(v) == list:
                rt_json[k] = util.list_text2list(pin.pin['{}-{}'.format(add_name, k)])
            else:
                rt_json[k] = pin.pin['{}-{}'.format(add_name, k)]

        return rt_json

    def _on_unload(self):
        j = json.load(open(self.file_name, 'r', encoding='utf8'))
        self.exit_popup = True
        if not is_json_equal(json.dumps(self.get_json(j)), json.dumps(j)):
            self.exit_popup = False
            output.popup('Do you need to save changes?', [
                output.put_buttons(['No', 'Yes'], onclick=self.popup_button)
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

    def put_json(self, j: dict, scope_name, add_name='', level=1):
        for k in j:
            v = j[k]
            if type(v) == str or v is None:
                pin.put_input('{}-{}'.format(add_name, k), label=k, value=v, scope=scope_name)
            elif type(v) == bool:
                pin.put_select('{}-{}'.format(add_name, k),
                               [{"label": 'True', "value": True}, {"label": 'False', "value": False}], value=v, label=k,
                               scope=scope_name)
            elif type(v) == dict:
                output.put_scope('{}-{}'.format(add_name, k), scope=scope_name)
                output.put_markdown('#' * level + ' ' + k, scope='{}-{}'.format(add_name, k))
                self.put_json(v, '{}-{}'.format(add_name, k), add_name='{}-{}'.format(add_name, k), level=level + 1)
            elif type(v) == list:
                pin.put_textarea('{}-{}'.format(add_name, k), label=k, value=util.list2format_list_text(v),
                                 scope=scope_name)
            elif type(v) == int:
                pin.put_input('{}-{}'.format(add_name, k), label=k, value=v, scope=scope_name, type='number')
            elif type(v) == float:
                pin.put_input('{}-{}'.format(add_name, k), label=k, value=v, scope=scope_name, type='float')
