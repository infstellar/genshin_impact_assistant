# from unit import *
import cv2
import os
import time

from interaction_background import InteractionBGD

itt = InteractionBGD()
i = 0

SA_name = 'test'


def jpg_with_alpha(png, bgclolr='black', channel='bg', alpha_num=50):
    if bgclolr == 'black':
        bgcol = 0
    else:
        bgcol = 255

    jpg = png[:, :, :3]
    if channel == 'bg':
        over_item_list = png[:, :, 3] > alpha_num
    else:
        over_item_list = png[:, :, 3] < alpha_num

    jpg[:, :, 0][over_item_list] = bgcol
    jpg[:, :, 1][over_item_list] = bgcol
    jpg[:, :, 2][over_item_list] = bgcol
    return jpg


def jwa_2(imsrc):
    Alpha = imsrc[:, :, 3:]
    Alpha = 255.0 - Alpha

    Alpha = Alpha * 2
    _, Alpha = cv2.threshold(Alpha, 503, 0, cv2.THRESH_TOZERO_INV)
    _, Alpha = cv2.threshold(Alpha, 50, 0, cv2.THRESH_TOZERO)
    _, Alpha = cv2.threshold(Alpha, 50, 255, cv2.THRESH_BINARY)
    return Alpha


def Line2Angle(p):
    # rad2degScale = 180/math.pi
    # res = math.atan2(-p[1], p[0])*rad2degScale
    # # const double rad2degScale = 180 / CV_PI;
    # # double res = atan2(-p.y, p.x)*rad2degScale;
    # # res = res - 90; //从屏幕空间左侧水平线为0度转到竖直向上为0度
    # if (res < -180.0):
    #     res = res + 360
    x = p[0]
    res = (x - 135) * (360 / 80)
    return res


def jwa_3(imsrc):
    Alpha = imsrc[:, :, 3:]
    Alpha = 255.0 - Alpha

    Alpha[360:, 286:] = 0
    Alpha[:, 303:] = 0

    Alpha = Alpha * 2
    _, Alpha = cv2.threshold(Alpha, 503, 0, cv2.THRESH_TOZERO_INV)
    _, Alpha = cv2.threshold(Alpha, 50, 0, cv2.THRESH_TOZERO)
    _, Alpha = cv2.threshold(Alpha, 50, 255, cv2.THRESH_BINARY)
    # cv2.imshow('1',Alpha)
    # cv2.waitKey(0)
    cv2.circle(Alpha, (int(Alpha.shape[0] / 2), int(Alpha.shape[1] / 2)),
               int((min(int(Alpha.shape[0] / 2), int(Alpha.shape[1] / 2)) * 1.21))
               , (0, 0, 0),
               int((min(int(Alpha.shape[0] / 2), int(Alpha.shape[1] / 2)) * 0.42)))
    cv2.circle(Alpha, (int(Alpha.shape[0] / 2), int(Alpha.shape[1] / 2)),
               int((min(int(Alpha.shape[0] / 2), int(Alpha.shape[1] / 2)) * 0.3)),
               (0, 0, 0), -1)

    dilate_element = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
    Alpha = cv2.dilate(Alpha, dilate_element)
    erode_element = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
    Alpha = cv2.erode(Alpha, erode_element)

    erode_element = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
    Alpha = cv2.erode(Alpha, erode_element)
    dilate_element = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
    Alpha = cv2.dilate(Alpha, dilate_element)
    Alpha = Alpha.astype('uint8')
    # return Alpha
    contours, hierarcy = cv2.findContours(Alpha, 0, 1)

    # std2.vector<cv2.Rect> boundRect(contours.size());  //定义外接矩形集合

    # cv2.Point p;
    # int maxBlack = 0;
    maxBlack = 0
    # int maxId = 0;
    maxId = 0
    boundRect = []
    # for (int i = 0; i < contours.size(); i++)
    for i in range(len(contours)):
        boundRect.append([])
        # {
        if len(contours[i]) > maxBlack:
            # 	{
            maxBlack = len(contours[i])
            maxId = i
        # 	}
        boundRect[i] = cv2.boundingRect(cv2.Mat(contours[i]))

    # }

    p = ((boundRect[maxId][0] + boundRect[maxId][1] / 2), (boundRect[maxId][2] + boundRect[maxId][3] / 2))
    print(p, Line2Angle(p))
    # Alpha =cv2.circle(Alpha, p, 3, (255, 0, 0))
    # Alpha =cv2.line(Alpha, p, (120, 170), (0, 255, 0))
    # cv2.imshow("Img", Alpha)
    # cv2.waitKey(0)
    # p = p - (img_object.cols / 2, img_object.rows / 2)
    return Alpha
    # p = p - cv2.Point(img_object.cols / 2, img_object.rows / 2);


# a = Line2Angle(p);
snap_path = "tools\\snapshot"
if not os.path.exists(snap_path + "\\png"):
    os.mkdir("tools\\snapshot\\png")

if not os.path.exists(snap_path + "\\jpg"):
    os.mkdir("tools\\snapshot\\jpg")

if not os.path.exists(snap_path + "\\jpg_withalpha"):
    os.mkdir("tools\\snapshot\\jpg_withalpha")

numi = 40
while 1:
    input('wait')
    i += 1
    numi += 1
    cap = itt.capture()
    x = str(time.time())
    # cv2.imwrite("tools\\snapshot\\png\\"+SA_name+str(numi)+".png",cap)
    # cv2.imwrite("tools\\snapshot\\jpg\\"+SA_name+str(numi)+".jpg",cap[:,:,:3])
    cv2.imwrite("tools\\snapshot\\jpg\\" + SA_name + str(numi) + ".jpg",
                jpg_with_alpha(cap, channel='ui', bgclolr='black', alpha_num=200))
    # cv2.imwrite("tools\\snapshot\\jpg_withalpha\\"+SA_name+str(numi)+".jpg",jwa_3(cap))
    # jwa_3(cap)
    time.sleep(0.1)
    print('pic', i)
