from source.api.pdocr_api import *
pdocr_timer_performance.reset()
if GLOBAL_LANG == "zh_CN":
    lang = 'ch'
elif GLOBAL_LANG == "en_US":
    lang = 'en'
ocr = PaddleocrAPI()
logger.info('created pdocr. cost ' + str(pdocr_timer_performance.get_diff_time()) + ' second.')