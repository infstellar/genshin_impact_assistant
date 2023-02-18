from source.interaction.interaction_core import itt
from source.interaction import interaction_core
from source.manager import asset
from source.util import *

itt = itt
dx = 25
dy = 25
posi_map = [57 + dy, 15 + dx,278 - dy, 236 - dy ]
posi_teyvat_map = [57, 15, 278, 236]


# def get_direction_angle():
#     cap=itt.png2jpg(itt.capture(),bgcolor='white',channel='ui')
#     val=[]
#     for i in ['N.jpg','NE.jpg','E.jpg','SE.jpg','S.jpg','SW.jpg','W.jpg','NW.jpg']:
#         a=itt.similar_img(i,cap,posi_manager.posi_arrow)
#         val.append(a)
#     return [0,45,90,135,180,-135,-90,-45][val.index(max(val))]

def qshow(img1):
    cv2.imshow('123', img1)
    cv2.waitKey(0)


def line2angle(p):
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
    alpha = imsrc[:, :, 3:]
    alpha = 255.0 - alpha
    # alpha = alpha[:360,:286:,:]
    # alpha[:,303:,:]=0
    # qshow(alpha)
    alpha = alpha * 2
    _, alpha = cv2.threshold(alpha, 503, 0, cv2.THRESH_TOZERO_INV)
    _, alpha = cv2.threshold(alpha, 50, 0, cv2.THRESH_TOZERO)
    _, alpha = cv2.threshold(alpha, 50, 255, cv2.THRESH_BINARY)
    # qshow(alpha)
    cv2.circle(alpha,
               (int(alpha.shape[0] / 2), int(alpha.shape[1] / 2)),
               int((min(int(alpha.shape[0] / 2), int(alpha.shape[1] / 2)) * 1.15)),  # 1.21
               (0, 0, 0), int((min(int(alpha.shape[0] / 2), int(alpha.shape[1] / 2)) * 0.6)))  # 0.42
    # qshow(alpha)
    cv2.circle(alpha,
               (int(alpha.shape[0] / 2), int(alpha.shape[1] / 2)),
               int((min(int(alpha.shape[0] / 2), int(alpha.shape[1] / 2)) * 0.6)), (0, 0, 0), -1)
    # qshow(alpha)
    dilate_element = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
    alpha = cv2.dilate(alpha, dilate_element)
    erode_element = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
    alpha = cv2.erode(alpha, erode_element)

    erode_element = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
    alpha = cv2.erode(alpha, erode_element)
    dilate_element = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
    alpha = cv2.dilate(alpha, dilate_element)
    alpha = alpha.astype('uint8')
    # return alpha
    contours, hierarcy = cv2.findContours(alpha, 0, 1)
    # qshow(alpha)

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
        logger.warning('找不到小地图')
        return -1
    x, y, w, h = boundRect[maxId]

    p = [x + w / 2, y + h / 2]

    origin_point = [int(alpha.shape[0] / 2) + 1, int(alpha.shape[1] / 2) + 1]
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
    # cv2.imshow('123', cv2.drawMarker(alpha, position=(int(p[0]), int(p[1])), color=(255, 0, 255), markerSize=1,
    #                                  markerType=cv2.MARKER_CROSS, thickness=5))
    # cv2.waitKey(100)
    # print(degree)
    return degree

    # logger.debug(str(p)+' '+str(Line2Angle(p)))
    # alpha =cv2.circle(alpha, p, 3, (255, 0, 0))
    # alpha =cv2.line(alpha, p, (120, 170), (0, 255, 0))
    # cv2.imshow("Img", alpha)
    # cv2.waitKey(0)
    # p = p - (img_object.cols / 2, img_object.rows / 2)
    # return p,Line2Angle(p)


def teyvat_smallmap_crusade_target_search(itt: interaction_core.InteractionBGD, imgicon):
    imsrc = itt.capture(posi=posi_teyvat_map)
    imsrc = itt.png2jpg(imsrc, channel='ui')
    img_target = imgicon.image
    r, pp = itt.similar_img(imsrc, img_target, ret_mode=interaction_core.IMG_POSI)
    p = [0, 0]
    p[0] = pp[0] + img_target.shape[1] / 2
    p[1] = pp[1] + img_target.shape[0] / 2
    # p = [x + w / 2, y + h / 2]

    origin_point = [int(imsrc.shape[1] / 2) + 1, int(imsrc.shape[0] / 2) + 1]
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
    # qshow(imsrc)
    show_img = imsrc.copy()
    cv2.drawMarker(show_img, position=(int(p[0]), int(p[1])), color=(255, 0, 255), markerSize=3,
                   markerType=cv2.MARKER_CROSS, thickness=5)
    cv2.imshow('123', show_img)
    cv2.waitKey(100)
    print(degree)
    return degree


if __name__ == '__main__':
    # qshow(itt.capture(posi=posi_map))
    while 1:
        jwa_3(itt.capture(posi=posi_map))
        # teyvat_smallmap_crusade_target_search(itt)
        time.sleep(0.1)
    # cv2.imshow('123', img1)
    # cv2.waitKey(0)
