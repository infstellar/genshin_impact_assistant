from source.util import *

if __name__ == '__main__':
    a = get_bbox(cv2.imread("assets/imgs/common/ui/emergency_food.jpg"))
    b = crop(cv2.imread("assets/imgs/common/ui/emergency_food.jpg"),a)
    cv2.imshow('123',b)
    cv2.waitKey(0)
    print()