# 使用PIL和OpenCV结合的方法
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
from loguru import logger
def convert_text_to_img(text=""):
    # 加载一个中文字体文件
    font = ImageFont.truetype("simhei.ttf", 32)

    # 获取一段中文文字的宽度和高度
    width, height = font.getsize(text)

    # 创建一个白色背景的图片，大小刚好能容纳文字
    img = Image.new("RGB", (width, height), "white")

    # 创建一个绘图对象
    draw = ImageDraw.Draw(img)

    # 在图片上绘制文字，位置为左上角
    draw.text((0, 0), text, font=font, fill="black")

    # 将图片转换回OpenCV格式
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    return img

def replace_text_format(text:str):
    text = text.replace("：",":")
    text = text.replace("！","!")
    text = text.replace("？","?")
    text = text.replace("，",",")
    text = text.replace("。",".")
    text = text.replace("“","\"")
    text = text.replace("”","\"")
    text = text.replace("‘","\'")
    text = text.replace("’","\'")
    return text

def compare_texts(text1, text2, is_show_res = False):
    # 读取两个短文本的图片
    img1 = convert_text_to_img(replace_text_format(text1))
    img2 = convert_text_to_img(replace_text_format(text2))

    if len(text1) != text2:
        logger.warning("compare_texts警告：不相同的文字长度")
    
    # 将图片转换为灰度图
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 计算两个灰度图之间的绝对差异
    diff = cv2.absdiff(gray1, gray2)

    # 设置一个阈值，将差异大于阈值的像素标记为白色，小于阈值的像素标记为黑色
    thresh = 50
    mask = diff > thresh

    # 将掩码转换为uint8类型，并乘以255，得到二值化后的差异图像
    mask = mask.astype(np.uint8) * 255

    matching_rate = 1 - len(np.where(mask==255)[0])/len(np.where(mask!=256)[0])
    logger.debug(f"texts matching rate:{matching_rate}")
    if is_show_res:
        # 在原始图片上绘制红色边框，表示差异区域
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(img1,(x,y),(x+w,y+h),(0,0,255),3)
            cv2.rectangle(img2,(x,y),(x+w,y+h),(0,0,255),3)

        # 显示结果图片
        cv2.imshow("Image 1", img1)
        cv2.imshow("Image 2", img2)
        cv2.imshow("Difference", mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    return matching_rate
        
compare_texts("你好,世界!","你好,世劼!", is_show_res=True)