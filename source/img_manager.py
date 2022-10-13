import cv2
coming_out_by_space=cv2.imread("assests\\imgs\\common\\coming_out_by_space.jpg")

imgs_dict={
    "coming_out_by_space":cv2.imread("assests\\imgs\\common\\coming_out_by_space.jpg")
}

def get_img_from_imgname(str1:str):
    return imgs_dict[str1]