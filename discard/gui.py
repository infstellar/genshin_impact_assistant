from paddleocr import PaddleOCR

# 模型路径下必须含有model和params文件
ocr = PaddleOCR(det_model_dir='./inference/default_det_model_dir/',  # 检测模型所在文件夹
                rec_model_dir='./inference/default_rec_model_dir/',  # 识别模型所在文件夹。
                cls_model_dir='./inference/default_cls_model_dir/',  # 分类模型所在文件夹。
                # rec_char_dict_path = './dict/japan_dict.txt', # 识别模型字典路径。
                # lang = 'en',
                use_angle_cls=True,  # 是否加载分类模型
                use_gpu=False)  # 是否使用gpu
img_path = './imgs/11.jpg'
result = ocr.ocr(img_path, cls=True)
ocr_result = [line[1][0] for line in result]  # 组合成列表形式
text = '\n'.join(ocr_result)  # 回车符连接列表中的每个元素
print(text)
# ————————————————
# 版权声明：本文为CSDN博主「aqqwvfbukn」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/aqqwvfbukn/article/details/120553124
