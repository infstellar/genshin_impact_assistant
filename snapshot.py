# from source.util import *
import cv2
import time, math

from source.interaction.interaction_core import itt
from source.util import *

itt = itt
i = 0

SA_name = 'test'


def jpg_with_alpha(png, bg_color='black', channel='bg', alpha_num=50):
    if bg_color == 'black':
        bg_col = 0
    else:
        bg_col = 255

    jpg = png[:, :, :3]
    if channel == 'bg':
        over_item_list = png[:, :, 3] > alpha_num
    else:
        over_item_list = png[:, :, 3] < alpha_num

    jpg[:, :, 0][over_item_list] = bg_col
    jpg[:, :, 1][over_item_list] = bg_col
    jpg[:, :, 2][over_item_list] = bg_col
    return jpg


def jwa_2(imsrc):
    alpha = imsrc[:, :, 3:]
    alpha = 255.0 - alpha

    alpha = alpha * 2
    _, alpha = cv2.threshold(alpha, 503, 0, cv2.THRESH_TOZERO_INV)
    _, alpha = cv2.threshold(alpha, 50, 0, cv2.THRESH_TOZERO)
    _, alpha = cv2.threshold(alpha, 50, 255, cv2.THRESH_BINARY)
    return alpha


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
    # Alpha = Alpha[:360,:286:,:]
    # Alpha[:,303:,:]=0
    # qshow(Alpha)
    Alpha = 255 - Alpha
    Alpha = Alpha.astype('uint8')
    # Alpha = Alpha * 2
    # _, Alpha = cv2.threshold(Alpha, 200, 0, cv2.THRESH_TOZERO_INV)
    _, Alpha = cv2.threshold(Alpha, 245, 0, cv2.THRESH_TOZERO)
    # _, Alpha = cv2.threshold(Alpha, 50, 255, cv2.THRESH_BINARY)
    # qshow(Alpha)
    cv2.circle(Alpha,
               (int(Alpha.shape[0] / 2), int(Alpha.shape[1] / 2)),
               int((min(int(Alpha.shape[0] / 2), int(Alpha.shape[1] / 2)) * 1.3)),  # 1.21
               (0, 0, 0), int((min(int(Alpha.shape[0] / 2), int(Alpha.shape[1] / 2)) * 0.2)))  # 0.42
    # qshow(Alpha)
    cv2.circle(Alpha,
               (int(Alpha.shape[0] / 2), int(Alpha.shape[1] / 2)),
               int((min(int(Alpha.shape[0] / 2), int(Alpha.shape[1] / 2)) * 0.6)), (0, 0, 0), -1)
    # qshow(Alpha)
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
    contours, _ = cv2.findContours(Alpha, 0, 1)
    # qshow(Alpha)

    maxBlack = 0
    maxId = 0
    boundRect = []
    for i in range(len(contours)):
        boundRect.append([])
        if len(contours[i]) > maxBlack:
            maxBlack = len(contours[i])
            maxId = i
        boundRect[i] = cv2.boundingRect(cv2.Mat(contours[i]))

    if len(boundRect) == 0:
        # logger.warning('找不到小地图')
        return -1
    x, y, w, h = boundRect[maxId]

    p = [x + w / 2, y + h / 2]

    origin_point = [int(Alpha.shape[0] / 2) + 1, int(Alpha.shape[1] / 2) + 1]
    point = [p[0] - origin_point[0], -p[1] + origin_point[1]]

    if point[0] == 0:
        point[0] += 0.1
    if point[1] == 0:
        point[1] += 0.1

    degree = math.degrees(math.atan((point[1]) / (point[0])))

    if point[0] > 0 and point[1] > 0:
        quadrant = 1
        degree = degree
    elif point[0] < 0 < point[1]:
        quadrant = 2
        degree += 180
    elif point[0] < 0 and point[1] < 0:
        quadrant = 3
        degree += 180
    elif point[0] > 0 > point[1]:
        quadrant = 4
        degree += 360

    # degree = math.atan((point[1]/hypotenuse_length)/(point[0]/hypotenuse_length))*(180 / math.pi)
    degree -= 90

    if degree > 180:
        degree -= 360
    # cv2.imshow('123', cv2.drawMarker(Alpha, position=(int(p[0]), int(p[1])), color=(255, 0, 255), markerSize=1,
    #                                  markerType=cv2.MARKER_CROSS, thickness=5))
    # cv2.waitKey(100)
    # print(degree)
    return degree

    # logger.debug(str(p)+' '+str(Line2Angle(p)))
    # Alpha =cv2.circle(Alpha, p, 3, (255, 0, 0))
    # Alpha =cv2.line(Alpha, p, (120, 170), (0, 255, 0))
    # cv2.imshow("Img", Alpha)
    # cv2.waitKey(0)
    # p = p - (img_object.cols / 2, img_object.rows / 2)
    # return p,Line2Angle(p)


# a = Line2Angle(p);
# snap_path = "tools\\snapshot"
# if not os.path.exists(snap_path + "\\png"):
#     os.mkdir("tools\\snapshot\\png")

# if not os.path.exists(snap_path + "\\jpg"):
#     os.mkdir("tools\\snapshot\\jpg")

# if not os.path.exists(snap_path + "\\jpg_withalpha"):
#     os.mkdir("tools\\snapshot\\jpg_withalpha")

num_i = 180
while 1:
    input('wait')
    i += 1
    num_i += 1
    cap = itt.capture(jpgmode=0)
    # cap = itt.png2jpg(cap, channel = 'ui', alpha_num = 50)# 22 no Q
    cv2.imwrite(ROOT_PATH + '\\' + "tools\\snapshot\\" + str(time.time()) + ".jpg", cap) # type: ignore
    x = str(time.time())
    time.sleep(0.1)
    print('pic', i)
