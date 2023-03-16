from source.api.pdocr_api import PaddleOcrFastDeploy
from source.util import *
pt = time.time()
if GLOBAL_LANG == "zh_CN":
    lang = 'ch'
elif GLOBAL_LANG == "en_US":
    lang = 'en'
ocr = PaddleOcrFastDeploy()
logger.info(f'created pdocr. cost {round(time.time()-pt,2)} second.')