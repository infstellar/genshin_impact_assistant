import cv2, numpy as np, posi_manager

COMING_OUT_BY_SPACE="coming_out_by_space"
IN_DOMAIN="IN_DOMAIN"
USE_20RESIN_DOBLE_CHOICES="USE_20RESIN_DOBLE_CHOICES"
USE_20X2RESIN_DOBLE_CHOICES="USE_20X2RESIN_DOBLE_CHOICES"

imsrc_coming_out_by_space=cv2.imread("assests\\imgs\\common\\coming_out_by_space.jpg")
imsrc_IN_DOMAIN=cv2.imread("assests\\imgs\\common\\IN_DOMAIN.jpg")
imsrc_USE_20RESIN_DOBLE_CHOICES=cv2.imread("assests\\imgs\\common\\USE_20RESIN_DOBLE_CHOICES.jpg")
imsrc_USE_20X2RESIN_DOBLE_CHOICES=cv2.imread("assests\\imgs\\common\\USE_20X2RESIN_DOBLE_CHOICES.jpg")

imgs_dict={
    "coming_out_by_space":imsrc_coming_out_by_space,
    "IN_DOMAIN":imsrc_IN_DOMAIN,
    "USE_20RESIN_DOBLE_CHOICES":imsrc_USE_20RESIN_DOBLE_CHOICES,
    "USE_20X2RESIN_DOBLE_CHOICES":imsrc_USE_20X2RESIN_DOBLE_CHOICES,
}

def qshow(img1):
    cv2.imshow('123', img1)
    cv2.waitKey(0)

def get_img_from_imgname(str1:str):
    
    imsrc = imgs_dict[str1]
    p = posi_manager.get_posi_from_str(str1)
    retimg = imsrc[p[0]:p[2],p[1]:p[3]]
    # cv2.imshow('12',retimg)
    # cv2.waitKey(0)
    return retimg

def refrom_img(imsrc, p):
    
    img = np.zeros((1080,1920,3),dtype=np.uint8)
    img[p[0]:p[2],p[1]:p[3]]=imsrc
    cv2.imshow('12',img)
    cv2.imshow('123',imsrc)
    cv2.waitKey(0)
    return img

def auto_import_img(impath,name):
    imsrc = cv2.imread(impath)
    origin_img = imsrc.copy()
    Grayimg = cv2.cvtColor(imsrc, cv2.COLOR_BGR2GRAY) # 先要转换为灰度图片
    ret, imsrc = cv2.threshold(Grayimg, 1, 255,cv2.THRESH_BINARY) # 这里的第二个参数要调，是阈值！！
    qshow(origin_img)
    
    
    contours, hierarcy=cv2.findContours(imsrc, 0, 1)
    # qshow(Alpha)

    maxBlack=0
    maxId=0
    boundRect=[]
    for i in range(len(contours)):
        boundRect.append([])
        if (len(contours[i]) > maxBlack):
            maxBlack = len(contours[i])
            maxId = i
        boundRect[i] = cv2.boundingRect(cv2.Mat(contours[i]))
    
    x,y,w,h=boundRect[maxId]
    
    draw_1 = cv2.rectangle(origin_img, (x,y), (x+w,y+h), (0,255,0), 2)
    qshow(draw_1)
    print('\"'+name+'\"',':',[y,x,y+h,x+w])
    return [y,x,y+h,x+w]
    p = [x+w/2, y+h/2]

def get_rect(imsrc,origin_img,ret_mode=0):
    # if origin_img==None:
    #     origin_img = imsrc
    ret, imsrc = cv2.threshold(imsrc, 1, 255,cv2.THRESH_BINARY)
    contours, hierarcy=cv2.findContours(imsrc, 0, 1)
    # qshow(Alpha)
    draw_1=origin_img
    maxBlack=0
    maxId=0
    boundRect=[]
    center_points=[]
    for i in range(len(contours)):
        boundRect.append([])
        
        
        if (len(contours[i]) > maxBlack):
            maxBlack = len(contours[i])
            maxId = i
        boundRect[i] = cv2.boundingRect(cv2.Mat(contours[i]))
        x,y,w,h=boundRect[i]
        center_points.append([(x+w/2), (y+h/2)])
        if ret_mode==1:
            draw_1 = cv2.rectangle(draw_1, (x,y), (x+w,y+h), (0,255,0), 2)
            
        x,y,w,h=boundRect[maxId]
        
        

    # qshow(draw_1)
    # print('\"'+name+'\"',':',[y,x,y+h,x+w])
    if ret_mode==0:
        return [y,x,y+h,x+w]
    elif ret_mode==1:
        return draw_1
    elif ret_mode==2:
        return center_points

if __name__=='__main__':
    # img = refrom_img(cv2.imread("assests\\imgs\\common\\coming_out_by_space.jpg"),posi_manager.get_posi_from_str('coming_out_by_space'))
    # cv2.imwrite("assests\\imgs\\common\\coming_out_by_space.jpg", img)
    # get_img_from_imgname(COMING_OUT_BY_SPACE)
    pname=USE_20RESIN_DOBLE_CHOICES
    p = auto_import_img("assests\\imgs\\common\\"+pname+".jpg",pname)
    print(p)