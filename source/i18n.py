"""i18n module for GIA."""

import gettext, os, json, locale
from source.path_lib import *

def load_json(json_name='General.json', default_path='config\\settings') -> dict:
    all_path = os.path.join(ROOT_PATH, default_path, json_name)
    return json.load(open(all_path, 'r', encoding='utf-8'))

jpath = fr"{ROOT_PATH}/config/settings/General.json"
if os.path.exists(jpath):
    j = json.load(open(jpath, 'r', encoding='utf-8'))
    DEBUG_MODE = j["DEBUG"]
    GLOBAL_LANG = j["Lang"]
else:
    DEBUG_MODE = False
    GLOBAL_LANG = "$locale$"
def get_local_lang():
    lang = locale.getdefaultlocale()[0]
    print(lang)
    if lang in ["zh_CN", "zh_SG", "zh_MO", "zh_HK", "zh_TW"]:
        return "zh_CN"
    else:
        return "en_US"

if GLOBAL_LANG == "$locale$":
    GLOBAL_LANG = get_local_lang()
    
# create .mo files
po_file_path = os.path.join(ROOT_PATH, r'translation/locale', GLOBAL_LANG, 'LC_MESSAGES', f'{GLOBAL_LANG}.po')
mo_file_path = os.path.splitext(po_file_path)[0] + '.mo'
print(fr"python {ROOT_PATH}/source/msgfmt.py -o {mo_file_path} {po_file_path}")
os.system(fr"python {ROOT_PATH}/source/msgfmt.py -o {mo_file_path} {po_file_path}")

l10n = gettext.translation(GLOBAL_LANG, localedir=os.path.join(ROOT_PATH, r"translation/locale"), languages=[GLOBAL_LANG])
l10n.install()
t2t = l10n.gettext