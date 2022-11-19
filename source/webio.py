import asyncio
import json
import os

from pywebio import *

from source import listening
from source import util

auto_combat = True
auto_domain = True


class WebUI:
    def __init__(self):
        self.file_name = ''

        self.config_files = []
        self.config_files_name = []
        for root, dirs, files in os.walk('config'):
            for f in files:
                self.config_files.append({"label": f, "value": os.path.join(root, f)})

        self.log_count = 0
        self.main_pin_change_thread = None

    @staticmethod
    async def _main_pin_change_thread():
        while True:
            await asyncio.sleep(0.1)
            if await pin.pin['FlowMode'] != listening.current_flow:
                listening.current_flow = await pin.pin['FlowMode']

    def put_setting(self, name=''):
        self.file_name = name
        output.put_markdown('## {}'.format(name), scope='now')
        j = json.load(open(name, 'r', encoding='utf8'))
        self.put_json(j, 'now', level=3)
        output.put_button('save', scope='now', onclick=self.save)

    async def save(self):

        j = json.load(open(self.file_name, 'r', encoding='utf8'))

        json.dump(await self.get_json(j), open(self.file_name, 'w', encoding='utf8'))
        # output.put_text('saved!', scope='now')
        output.toast('saved!')

    async def get_json(self, j: dict, add_name=''):
        rt_json = {}
        for k in j:

            v = j[k]
            if type(v) == dict:
                rt_json[k] = self.get_json(v, add_name='{}-{}'.format(add_name, k))

            elif type(v) == list:
                rt_json[k] = util.list_text2list(await pin.pin['{}-{}'.format(add_name, k)])
            else:
                rt_json[k] = await pin.pin['{}-{}'.format(add_name, k)]

        return rt_json

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

    async def main(self):
        await self.load_main()

    async def load_main(self):
        global auto_domain, auto_combat
        # 主scope
        output.put_scope('main')
        # 标题
        output.put_markdown('# Main', scope='main')

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

                output.put_row([output.put_text('PickUp'), output.put_scope('Button_PickUp')])

            ]), None,
            output.put_scope('Log')

        ], scope='main')
        # Button
        output.put_button(label=str(listening.FEAT_PICKUP), onclick=self.on_click_pickup, scope='Button_PickUp')
        # Log
        output.put_markdown('## Log', scope='Log')
        output.put_scrollable(output.put_scope('LogArea'), height=300, keep_bottom=True, scope='Log')
        '''self.main_pin_change_thread = threading.Thread(target=self._main_pin_change_thread, daemon=False)
        self.main_pin_change_thread.start()'''
        await self._main_pin_change_thread()

    def on_click_pickup(self):
        global auto_domain
        self.logout('click_auto_pickup')
        output.clear('Button_AutoDomain')
        listening.FEAT_PICKUP = not listening.FEAT_PICKUP
        output.put_button(label=str(listening.FEAT_PICKUP), onclick=self.on_click_pickup, scope='Button_AutoDomain')

    async def load_setting(self):
        output.put_scope('setting')
        output.put_markdown('# Setting', scope='setting')
        output.put_markdown('## config:', scope='setting')
        pin.put_select('file', self.config_files, scope='setting')
        with output.use_scope('now', clear=True):
            self.put_setting(await pin.pin['file'])
        while True:
            changed = await pin.pin_wait_change('file')
            with output.use_scope('now', clear=True):
                self.put_setting(changed['value'])

    def logout(self, text: str, color='black'):
        '''if self.log_count < 0:
            output.clear('LogArea')
            self.log_count = 0'''
        output.put_text(text, scope='LogArea').style(f'color: {color}')
        self.log_count += 1


if __name__ == '__main__':
    ui = WebUI()
    platform.tornado.start_server(ui.main, auto_open_webbrowser=True, debug=True)
