import json
import os

from pywebio import *

from source import util

file_name = ''


def put_setting(name=''):
    global file_name
    file_name = name
    output.put_markdown('## {}'.format(name), scope='now')
    j = json.load(open(name, 'r', encoding='utf8'))
    put_json(j, 'now', level=3)
    output.put_button('save', scope='now', onclick=save)


async def save():
    global file_name
    j = json.load(open(file_name, 'r', encoding='utf8'))

    json.dump(await get_json(j), open(file_name, 'w', encoding='utf8'))
    # output.put_text('saved!', scope='now')
    output.toast('saved!')


async def get_json(j: dict, add_name=''):
    rt_json = {}
    for k in j:

        v = j[k]
        if type(v) == dict:
            rt_json[k] = get_json(v, add_name='{}-{}'.format(add_name, k))

        elif type(v) == list:
            rt_json[k] = util.list_text2list(await pin.pin['{}-{}'.format(add_name, k)])
        else:
            rt_json[k] = await pin.pin['{}-{}'.format(add_name, k)]

    return rt_json


def put_json(j: dict, scope_name, add_name='', level=1):
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
            put_json(v, '{}-{}'.format(add_name, k), add_name='{}-{}'.format(add_name, k), level=level + 1)
        elif type(v) == list:
            pin.put_textarea('{}-{}'.format(add_name, k), label=k, value=util.list2format_list_text(v),
                             scope=scope_name)
        elif type(v) == int:
            pin.put_input('{}-{}'.format(add_name, k), label=k, value=v, scope=scope_name, type='number')
        elif type(v) == float:
            pin.put_input('{}-{}'.format(add_name, k), label=k, value=v, scope=scope_name, type='float')


config_files = []
config_files_name = []
for root, dirs, files in os.walk('config'):
    for f in files:
        config_files.append({"label": f, "value": os.path.join(root, f)})


async def main():
    output.put_markdown('# Setting')
    output.put_markdown('## config:')
    pin.put_select('file', config_files)
    with output.use_scope('now', clear=True):
        put_setting(await pin.pin['file'])
    while True:
        changed = await pin.pin_wait_change('file')
        with output.use_scope('now', clear=True):
            put_setting(changed['value'])


if __name__ == '__main__':
    platform.tornado.start_server(main, auto_open_webbrowser=True, debug=True)
