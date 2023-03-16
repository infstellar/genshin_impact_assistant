from source.util import *
import fastdeploy

inference_path = os.path.join(ROOT_PATH, f'assets\\PPOCRModels\\zh_CN')

det_model = fastdeploy.vision.ocr.DBDetector(model_file=inference_path+"\\pddet\\inference.pdmodel", params_file=inference_path+"\\pddet\\inference.pdiparams")
rec_model = fastdeploy.vision.ocr.Recognizer(model_file=inference_path+"\\pdrec\\inference.pdmodel", params_file=inference_path+"\\pdrec\\inference.pdiparams",label_path=inference_path+"\\rec\\keys.txt")
# cls_model = fastdeploy.vision.ocr.DBDetector(model_file=inference_path+"\\ch_ppocr_mobile_v2.0_cls_infer_3\\inference.pdmodel", params_file=inference_path+"\\ch_ppocr_mobile_v2.0_cls_infer_3\\inference.pdiparams")

# det_model = fastdeploy.vision.ocr.DBDetector(model_file=inference_path+"\\det\\inference.onnx", model_format=fastdeploy.ModelFormat.ONNX)
# rec_model = fastdeploy.vision.ocr.Recognizer(model_file=inference_path+"\\rec\\inference.onnx",label_path=inference_path+"\\rec\\keys.txt", model_format=fastdeploy.ModelFormat.ONNX)
# cls_model = fastdeploy.vision.ocr.DBDetector()

ocr = fastdeploy.vision.ocr.PPOCRv3(det_model,None,rec_model)
ocr2 = fastdeploy.vision.ocr.PPOCRv3(det_model,None,rec_model)
imsrc = cv2.imread("D:\\test.jpg")
cv2.imshow('123',imsrc)
cv2.waitKey(0)
print(ocr.predict(imsrc))
print(ocr2.predict(imsrc))