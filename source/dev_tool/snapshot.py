import cv2
import time
from source.interaction.interaction_core import itt
from source.util import *
cap = itt.capture(jpgmode=0)
cv2.imwrite(ROOT_PATH + '\\' + "tools\\snapshot\\" + str(time.time()) + ".jpg", cap) # type: ignore
