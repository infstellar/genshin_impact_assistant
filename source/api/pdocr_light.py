from source.api.pdocr_api import *
pdocr_timer_performance.reset()
logger.info("creating ocr_light")
ocr_light = PaddleocrAPI(inference_path=os.path.join(ROOT_PATH, f'assets\\PPOCRModels\\ppocr_onnx_en'))
logger.info('created ocr_light. cost ' + str(pdocr_timer_performance.get_diff_time()) + ' second.')