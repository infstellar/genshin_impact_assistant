from source.util import *
from source.interaction.interaction_core import itt
from source.api.pdocr_complete import ocr
from source.api.pdocr_api import SHAPE_MATCHING, ACCURATE_MATCHING
from source.manager import asset

domain_stage_name = "鸣雷城墟IV"
def _domain_text_process(text:str):
    text = text.replace('：', ':')
    text = text.replace(' ', '')
    text = text.replace("Ⅱ", "I")
    if ":" in text:
        text = text[text.index(':')+1:]
    return text
cap_area = asset.switch_domain_area.position

p1 = ocr.get_text_position(itt.capture(jpgmode=0, posi=cap_area), domain_stage_name,
                                   cap_posi_leftup=cap_area[:2],
                                   text_process = _domain_text_process,
                                   mode=ACCURATE_MATCHING,
                                   extract_white_threshold=254)
print(p1)