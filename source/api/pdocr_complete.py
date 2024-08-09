from source.api.pdocr_api import PaddleOcrFastDeploy
from source.util import *
pt = time.time()
if GLOBAL_LANG == "zh_CN":
    lang = 'ch'
elif GLOBAL_LANG == "en_US":
    lang = 'en'
ocr = PaddleOcrFastDeploy()
logger.info(f'created pdocr. cost {round(time.time()-pt,2)} second.')


if __name__ == '__main__':
    from source.interaction.interaction_core import itt
    while 1:
        ocr.get_all_texts(itt.capture())