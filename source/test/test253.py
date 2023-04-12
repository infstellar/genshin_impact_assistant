from source.util import *
from source.manager.asset import AreaCombatBloodBar
from source.api.pdocr_light import ocr_light

img = cv2.imread(os.path.join(ROOT_PATH, "tools\\snapshot\\bloodbar.jpg"))
img2 = crop(img, AreaCombatBloodBar.position)
img2 = extract_white_letters(img2, threshold=251)
t = ocr_light.get_all_texts(img2)
t = ocr_light.get_all_texts(img2)

pt1 = time.time()
t = ocr_light.get_all_texts(img2)
print(time.time()-pt1)
print(t)
