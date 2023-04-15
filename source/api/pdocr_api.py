from source.util import *


logger.info(t2t('Creating ocr object.'))
from common.timer_module import Timer

pdocr_timer_performance = Timer()
pdocr_timer_performance.reset()
import inspect

try:
    import fastdeploy
except Exception as error:
    logger.critical(t2t("导入paddleocr时错误; err code: 001"))
    logger.exception(error)
logger.info(f"import pdocr time: {round(pdocr_timer_performance.get_diff_time(),2)}")

# paddleocr.MODEL_URLS["OCR"]["PP-OCRv3"]["rec"]["num_only"] = {
#                     'url':
#                     'https://paddleocr.bj.bcebos.com/PP-OCRv3/english/en_PP-OCRv3_rec_infer.tar',
#                     'dict_path': './ppocr/utils/en_dict.txt'
                # },

# globaldevice = 
# if globaldevice == 'auto':
#     import paddle

#     paddle.fluid.install_check.run_check()
#     globaldevice = 'cpu'
CONTAIN_MATCHING = 0
ACCURATE_MATCHING = 1
TWICE_AND_MATCHING = 3
TWICE_OR_MATCHING = 5
TWICE_FRONTANDBACK_MATCHING = 4
TWICE_FRONTANDBACK_SEQUENTIAL_MATCHING = 6
REPEATLY_MATCHING = 7
SHAPE_MATCHING = 8

CHANNEL_RED = 2
RETURN_TEXT = 1
RETURN_POSITION = 0
RETURN_POINT = 3



class PaddleOcrFastDeploy():
    def __init__(self, inference_path:str=None, lang=GLOBAL_LANG) -> None:
        if inference_path is None:
            inference_path = os.path.join(ROOT_PATH, f'assets\\PPOCRModels\\{lang}')
        logger.info(f"Creating PaddleOCRFastDeploy object: {inference_path}")
        pt=time.time()
        det_file_path = os.path.join(inference_path, "pddet\\inference.pdmodel")
        det_para_path = os.path.join(inference_path, "pddet\\inference.pdiparams")
        rec_file_path = os.path.join(inference_path, "pdrec\\inference.pdmodel")
        rec_para_path = os.path.join(inference_path, "pdrec\\inference.pdiparams")
        rec_keys_path = os.path.join(inference_path, "rec\\keys.txt")
        self.det_model = fastdeploy.vision.ocr.DBDetector(model_file=det_file_path, params_file=det_para_path)
        self.rec_model = fastdeploy.vision.ocr.Recognizer(model_file=rec_file_path, params_file=rec_para_path,label_path=rec_keys_path)
        logger.info(f"created DBDetector and Recognizer. cost {round(time.time()-pt,2)}")
        pt2=time.time()
        self.model = fastdeploy.vision.ocr.PPOCRv3(self.det_model,None,self.rec_model)
        logger.info(f"created PPOCRv3. cost {round(time.time()-pt2,2)}")
    
    def analyze(self, img:np.ndarray):
        if False:
            cv2.imshow("123",img)
            cv2.waitKey(0)
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        res = self.model.predict(img)
        logger.trace(str(res).replace('\n',''))
        return res
    REPLACE_DICT = {
            "惊垫":"惊蛰",
            "烟排":"烟绯",
            "花染":"椛染"
        }
    def _replace_texts(self, text:str):
        for i in self.REPLACE_DICT:
            if i in text:
                text = text.replace(i, self.REPLACE_DICT[i])
        return text

    def find_text(self,res,text,mode=CONTAIN_MATCHING,text_process=lambda x:x):
        ret_indexes = []

        if mode == SHAPE_MATCHING:
            max_rate = 0
            max_result = None
            for i in range(len(res.text)):
                curr_rate = compare_texts(text, self._replace_texts(text_process(res.text[i])))
                if curr_rate > max_rate:
                    max_result = i
                    max_rate = curr_rate
            logger.debug(f"text: {res.text[max_result]}")
            return [max_result]

        for i in range(len(res.text)):
            res_text = self._replace_texts(text_process(res.text[i]))
            if mode == CONTAIN_MATCHING:
                if text in res_text:
                    ret_indexes.append(i)
            elif mode == ACCURATE_MATCHING:
                if text == res_text:
                    ret_indexes.append(i)
        
        return ret_indexes

    def get_text_position(self,
                           img:np.ndarray,
                           text:str,
                           mode=CONTAIN_MATCHING,
                           position_mode = RETURN_POINT,
                           cap_posi_leftup=None,
                           text_process=lambda x:x,
                           extract_white_threshold=None)->list:
        ret_position = []
        if cap_posi_leftup == None:
            cap_posi_leftup = [0,0]
        if extract_white_threshold!=None:
            img = extract_white_letters(img, threshold = extract_white_threshold)
        res = self.analyze(img)
        indexes = self.find_text(res,text,mode=mode,text_process=text_process)
        for i in indexes:
            # left up - right down 
            # docs from https://github.com/PaddlePaddle/FastDeploy/blob/develop/docs/api/vision_results/ocr_result_CN.md
            # boxes: 成员变量，表示单张图片检测出来的所有目标框坐标，
            # boxes.size()表示单张图内检测出的框的个数，每个框以8个int数值依次表示框的4个坐标点，
            # 顺序为左下 01，右下 23，右上 45，左上 67
            if position_mode == RETURN_POSITION:
                ret_position.append(
                                    [cap_posi_leftup[0]+res.boxes[i][6], cap_posi_leftup[1]+res.boxes[i][7],
                                    cap_posi_leftup[0]+res.boxes[i][2], cap_posi_leftup[1]+res.boxes[i][3]]
                                    )
            elif position_mode == RETURN_POINT:
                ret_position.append(
                                    [(cap_posi_leftup[0]+res.boxes[i][6]+cap_posi_leftup[0]+res.boxes[i][2])/2,
                                    (cap_posi_leftup[1]+res.boxes[i][7]+cap_posi_leftup[1]+res.boxes[i][3])/2
                                    ]
                                    )


        if len(ret_position)==0:
            return -1
        elif len(ret_position)==1:
            return list(ret_position[0])
        elif len(ret_position)>1:
            return list(ret_position)
            
    def get_all_texts(self, img, mode=0):
        res = self.analyze(img)
        if mode==1:
            return ','.join(str(i) for i in res.text).replace(',','')
        return res.text
    
    def is_img_num(self, im_src):
        pdocr_timer_performance.reset()
        is_num = False
        res_num = None
        res = self.analyze(im_src)

        for num in res.text:
            if is_number(num):
                res_num = float(num)
                is_num = True
            else:
                res_num = None
                is_num = False
        t = pdocr_timer_performance.get_diff_time()

        return is_num, res_num, t

    def is_img_num_plus(self, im_src):
        ret1, ret2, t = self.is_img_num(im_src)
        if ret1 is not None:
            ret1, ret2, t = self.is_img_num(im_src)
        logger.debug(str(ret1) + ' ' + str(ret2) + ' ' + str(t) + ' |function name: ' +
                     inspect.getframeinfo(inspect.currentframe().f_back)[2])
        return ret1, ret2

if __name__ == '__main__':
    ocr = PaddleOcrFastDeploy()
    imsrc = cv2.imread("D:\\test2.jpg")
    r = ocr.get_text_position(imsrc, "VsCode")
    print(r)# boxes, rec_scores, text
    imsrc = cv2.imread("D:\\test.jpg")
    r = ocr.get_text_position(imsrc, "VsCode")
    print(r)# boxes, rec_scores, text





default_infer_path = os.path.join(ROOT_PATH, f'assets\\PPOCRModels\\zh_CN')

class PaddleocrAPI:
    
    def __init__(self, device='gpu',inference_path=default_infer_path):
        
        device = 'cpu'
        logger.info(t2t("ocr device: ") + device)
        det_model = fastdeploy.vision.ocr.DBDetector(model_file=inference_path+"\\pddet\\inference.pdmodel", params_file=inference_path+"\\pddet\\inference.pdiparams")
        rec_model = fastdeploy.vision.ocr.Recognizer(model_file=inference_path+"\\pdrec\\inference.pdmodel", params_file=inference_path+"\\pdrec\\inference.pdiparams",label_path=inference_path+"\\rec\\keys.txt")
        # cls_model = fastdeploy.vision.ocr.DBDetector(model_file=inference_path+"\\ch_ppocr_mobile_v2.0_cls_infer_3\\inference.pdmodel", params_file=inference_path+"\\ch_ppocr_mobile_v2.0_cls_infer_3\\inference.pdiparams")
        
        # det_model = fastdeploy.vision.ocr.DBDetector(model_file=inference_path+"\\det\\inference.onnx", model_format=fastdeploy.ModelFormat.ONNX)
        # rec_model = fastdeploy.vision.ocr.Recognizer(model_file=inference_path+"\\rec\\inference.onnx",label_path=inference_path+"\\rec\\keys.txt", model_format=fastdeploy.ModelFormat.ONNX)
        # cls_model = fastdeploy.vision.ocr.DBDetector()
        
        self.pdocr = fastdeploy.vision.ocr.PPOCRv3(det_model,None,rec_model)
                            # cls_model_dir=inference_path+"cls_model\\")
        # self.ocr.use_ort_backend()
        # self.

    def img_analyze(self, im_src):
        if True:
            pass
        result = self.pdocr.predict(im_src)
        for line in result:
            pass
            # print(line)
        return result[0] # py3.7

    # def imgAnalysePlus(self,hwnd:winInfo,rangePosition):
    #     imsrc,position=GetScrWindowsImg(hwnd,rangePosition)
    #     res=self.ImgAnalyse(imsrc)
    #     return res,position

    # def SaveResult(self,imsrc,result):
    #     from source.PIL import Image
    #     #image = Image.open(img_path).convert('RGB')
    #     boxes = [line[0] for line in result]
    #     txts = [line[1][0] for line in result]
    #     scores = [line[1][1] for line in result]
    #     im_show = draw_ocr(imsrc, boxes, txts, scores, font_path='./fonts/simfang.ttf')
    #     im_show = Image.fromarray(im_show)
    #     im_show.save('result.jpg')

    @staticmethod
    def find_text(result, text, mode=CONTAIN_MATCHING, text_process=lambda x:x):
        if result == [[]]:
            return None
        
        if True:
            max_rate = 0
            max_result = None
            for i in range(len(result)):
                curr_rate = compare_texts(text, text_process(result[i][1][0]))
                if curr_rate > max_rate:
                    max_result = result[i]
                    max_rate = curr_rate
            if max_rate >= 0.9:
                logger.debug(f"text: {max_result[1][0]}")
                return max_result
        
        if mode == CONTAIN_MATCHING:
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

    def get_text_position(self, im_src, text, mode=CONTAIN_MATCHING, returnMode=RETURN_POSITION, isprintlog=False,
                          message='', default_end='\n', cap_posi_leftup = None, text_process=lambda x:x):
        if cap_posi_leftup == None:
            cap_posi_leftup = [0,0]
        res = self.img_analyze(im_src)
        res_position = self.find_text(res, text, mode=mode, text_process = text_process)
        # logger.debug('getTextPosition:  ' + message, end=' | ')
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
                    result.append([res_position[0][0][0]+cap_posi_leftup[0], res_position[0][0][1]+cap_posi_leftup[1]])
                return result
            if returnMode == RETURN_POSITION:
                logger.debug('found the text:' + text + ' |function name: ' +
                             inspect.getframeinfo(inspect.currentframe().f_back)[2])
                return [res_position[0][0][0] + cap_posi_leftup[0], res_position[0][0][1] + cap_posi_leftup[1]]
            elif returnMode == RETURN_TEXT:
                logger.debug('found the text:' + text + ' |function name: ' +
                             inspect.getframeinfo(inspect.currentframe().f_back)[2])
                return list( np.array(res_position[1][0]) + np.array(cap_posi_leftup) )
        else:
            logger.debug('can not find the text:' + text + ' |function name: ' +
                         inspect.getframeinfo(inspect.currentframe().f_back)[2])
            return -1


    def is_img_num(self, im_src):
        pdocr_timer_performance.reset()
        is_num = False
        res_num = None
        res = self.img_analyze(im_src)

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