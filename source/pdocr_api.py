from util import *

logger.info('Creating ocr object.')
from timer_module import Timer

pdocr_timer_performance = Timer()
pdocr_timer_performance.reset()
import inspect

try:
    from paddleocr import PaddleOCR
    from paddleocr import draw_ocr
except Exception as error:
    logger.critical("导入paddleocr时错误; err code: 001")
    logger.exception(error)

globaldevice = config_json["device_paddle"]
if globaldevice == 'auto':
    import paddle

    paddle.fluid.install_check.run_check()
    globaldevice = 'cpu'
APPROXIMATE_MATCHING = 0
ACCURATE_MATCHING = 1
TWICE_AND_MATCHING = 3
TWICE_OR_MATCHING = 5
TWICE_FRONTANDBACK_MATCHING = 4
TWICE_FRONTANDBACK_SEQUENTIAL_MATCHING = 6
REPEATLY_MATCHING = 7

CHANNEL_RED = 2
RETURN_TEXT = 1
RETURN_POSITION = 0


class PaddleocrAPI:

    def __init__(self, lang='ch', device='gpu'):
        device = globaldevice
        logger.info("ocr device: " + device)
        self.ocr = PaddleOCR(use_angle_cls=True, lang=lang, show_log=False,
                             device=device)  # need to run only once to download and load model into memory
        # self.

    def img_analyse(self, im_src):
        result = self.ocr.ocr(im_src, cls=False)
        for line in result:
            pass
            # print(line)
        return result

    # def imgAnalysePlus(self,hwnd:winInfo,rangePosition):
    #     imsrc,position=GetScrWindowsImg(hwnd,rangePosition)
    #     res=self.ImgAnalyse(imsrc)
    #     return res,position

    # def SaveResult(self,imsrc,result):
    #     from PIL import Image
    #     #image = Image.open(img_path).convert('RGB')
    #     boxes = [line[0] for line in result]
    #     txts = [line[1][0] for line in result]
    #     scores = [line[1][1] for line in result]
    #     im_show = draw_ocr(imsrc, boxes, txts, scores, font_path='./fonts/simfang.ttf')
    #     im_show = Image.fromarray(im_show)
    #     im_show.save('result.jpg')

    @staticmethod
    def find_text(result, text, mode=APPROXIMATE_MATCHING):
        if mode == APPROXIMATE_MATCHING:
            for i in range(len(result)):
                if text in result[i][1][0]:
                    return result[i]
        elif mode == ACCURATE_MATCHING:
            for i in range(len(result)):
                if result[i][1][0] == text:
                    return result[i]
        elif mode == TWICE_AND_MATCHING:
            for i in range(len(result)):
                if text[0] in result[i][1][0] and text[1] in result[i][1][0]:
                    logger.debug('TWICE_AND_MATCHING found ' + text + ' |function name: ' +
                                 inspect.getframeinfo(inspect.currentframe().f_back)[2])
                    return result[i]
        elif mode == TWICE_FRONTANDBACK_MATCHING:
            for i in range(len(result)):
                if i != len(result) - 1:
                    if (text[0] in result[i][1][0] or text[1] in result[i][1][0]) and (
                            text[0] in result[i + 1][1][0] or text[1] in result[i + 1][1][0]):
                        return result[i]
        elif mode == TWICE_OR_MATCHING:
            for i in range(len(result)):
                if text[0] in result[i][1][0] or text[1] in result[i][1][0]:
                    return result[i]
        elif mode == TWICE_FRONTANDBACK_SEQUENTIAL_MATCHING:
            for i in range(len(result)):
                if (i != len(result) - 1) and (text[0] in result[i][1][0]) and (text[1] in result[i + 1][1][0]):
                    logger.debug('TWICE_FRONTANDBACK_SEQUENTIAL_MATCHING found ' + text,
                                 '|function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])
                    return result[i]
        elif mode == REPEATLY_MATCHING:
            result = []
            for i in range(len(result)):
                if (i != len(result) - 1) and (text[0] in result[i][1][0]) and (text[1] in result[i + 1][1][0]):
                    logger.debug('TWICE_FRONTANDBACK_SEQUENTIAL_MATCHING found ' + text + '|function name: ' +
                                 inspect.getframeinfo(inspect.currentframe().f_back)[2])
                    result.append(result[i])
            if result:
                return result
        return None

    def get_text_position(self, im_src, text, mode=APPROXIMATE_MATCHING, returnMode=RETURN_POSITION, isprintlog=False,
                          message='', default_end='\n'):
        res = self.img_analyse(im_src)
        res_position = self.find_text(res, text, mode=mode)
        logger.debug('getTextPosition:  ' + message, end=' | ')
        if isprintlog:
            logger.debug('res: ' + '|function name: ' + inspect.getframeinfo(inspect.currentframe().f_back)[2])
            for i in res:
                logger.debug(i[1][0], end=', ')
            logger.debug(end=default_end)
        # cv2.imshow('pic',im_src)
        # cv2.waitKey(0)
        if res_position is not None:
            # print('res_position',res_position)
            if mode == REPEATLY_MATCHING and returnMode == RETURN_POSITION:
                result = []
                for i in res_position:
                    result.append([res_position[0][0][0], res_position[0][0][1]])
                return result
            if returnMode == RETURN_POSITION:
                logger.debug('found the text:' + text + ' |function name: ' +
                             inspect.getframeinfo(inspect.currentframe().f_back)[2])
                return [res_position[0][0][0], res_position[0][0][1]]
            elif returnMode == RETURN_TEXT:
                logger.debug('found the text:' + text + ' |function name: ' +
                             inspect.getframeinfo(inspect.currentframe().f_back)[2])
                return res_position[1][0]
        else:
            logger.debug('can not find the text:' + text + ' |function name: ' +
                         inspect.getframeinfo(inspect.currentframe().f_back)[2])
            return -1

    def is_img_num(self, im_src):
        pdocr_timer_performance.reset()
        is_num = False
        res_num = None
        res = self.img_analyse(im_src)

        for result_item in res:
            # noinspection PyBroadException
            try:
                num = result_item[1][0]
            except:
                num = ''

            for i in num:
                if i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
                    is_num = True

            if is_number(num):
                res_num = float(num)
            else:
                res_num = None
        t = pdocr_timer_performance.get_diff_time()

        return is_num, res_num, t

    def is_img_num_plus(self, im_src):
        ret1, ret2, t = self.is_img_num(im_src)
        if ret1 is not None:
            ret1, ret2, t = self.is_img_num(im_src)
        logger.debug(str(ret1) + ' ' + str(ret2) + ' ' + str(t) + ' |function name: ' +
                     inspect.getframeinfo(inspect.currentframe().f_back)[2])
        return ret1, ret2


ocr = PaddleocrAPI()
logger.info('created pdocr. cost ' + str(pdocr_timer_performance.get_diff_time()) + ' second.')
