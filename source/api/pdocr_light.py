from source.api.pdocr_api import *
pdocr_timer_performance.reset()
logger.info("creating ocr_light")
ocr_light = PaddleocrAPI(lang='en', use_angle_cls=False, device='cpu',
                        inference_path=os.path.join(root_path, f'assets\\inference\\light\\')),
logger.info('created ocr_light. cost ' + str(pdocr_timer_performance.get_diff_time()) + ' second.')