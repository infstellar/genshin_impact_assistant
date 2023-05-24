from source.util import *
from pywebio import output


def toast_succ(text="succ!", duration=2):
    output.toast(text, position='center', color='#2188ff', duration=duration)