from source.util import *
from pywebio import output


def toast_succ(text="success!", duration=2):
    output.toast(text, position='center', color='success', duration=duration)



