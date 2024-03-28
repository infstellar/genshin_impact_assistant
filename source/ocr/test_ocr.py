# import pytest
import cv2
from source.util import *


def test_ocr_availability():
    from source.ocr.ocr import Ocr
    ocr = Ocr()
    logger.info("OCR RESULT: "+str(ocr.ocr_single_line(cv2.imread(fr'{ROOT_PATH}/assets/pytest/AreaBigmapSidebarCommissionName.jpg'))))
    assert 1

if __name__ == '__main__':
    test_ocr_availability()