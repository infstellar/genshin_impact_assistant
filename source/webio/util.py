from source.util import *
from pywebio import output


def toast_succ(text="succ!", duration=2):
    output.toast(text, position='center', color='#2188ff', duration=duration)

def get_name(x):
    (filename, line_number, function_name, text) = x
    # = traceback.extract_stack()[-2]
    return text[:text.find('=')].strip()

def auto_name():
    return get_name(traceback.extract_stack()[-2])

AN = auto_name