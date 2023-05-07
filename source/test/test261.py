from source.util import *
from source.assets.movement import *
# from source.interaction.interaction_core import itt

import cv2
import numpy as np

img = IconMovementClimb.image # itt.capture(posi=IconMovementFly.cap_posi)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_white = np.array([0, 0, 221])
upper_white = np.array([180, 40, 255])

mask = cv2.inRange(hsv, lower_white, upper_white)
res = cv2.bitwise_and(img,img, mask= mask)

# cv2.imshow('Original', img)
cv2.imshow('Mask', mask)
# cv2.imshow('Result', res)

cv2.waitKey(0)
# cv2.destroyAllWindows()

cv2.imwrite(fr"{ROOT_PATH}/assets/imgs/Windows/Movement/common/IconMovementClimbing.jpg", mask)