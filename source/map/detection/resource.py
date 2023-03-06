import gimap
from cached_property import cached_property

from source.map.detection.resource_const import MiniMapConst
from source.map.detection.utils import *


class MiniMapResource(MiniMapConst):
    @cached_property
    def _minimap_mask(self):
        mask = create_circular_mask(h=self.MINIMAP_RADIUS * 2, w=self.MINIMAP_RADIUS * 2)
        mask = (mask * 255).astype(np.uint8)
        return mask

    @cached_property
    def GIMAP(self):
        # About 100ms to load
        file = gimap.get_file('GIMAP_luma_05x.png')
        image = load_image(file)
        return image

    @cached_property
    def GIBigmap(self):
        file = gimap.get_file('GIBigmap_luma_0125x_pad125.png')
        image = load_image(file)
        return image

    @cached_property
    def ArrowRotateMap(self):
        file = gimap.get_file('ArrowRotateMap.png')
        image = load_image(file)
        return image

    @cached_property
    def ArrowRotateMapAll(self):
        file = gimap.get_file('ArrowRotateMapAll.png')
        image = load_image(file)
        return image

    @cached_property
    def GICityMask_dict(self):
        file = gimap.get_file('GICityMask_05x.png')
        image = load_image(file)

        # Split image to reduce memory usage
        out = {}
        image = cv2.multiply(image, 1 / 255)
        contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)
            area = (x, y, x + w, y + h)
            out[area] = crop(image, area=area)
        return out

    def _position_in_GICityMask(self, position) -> bool:
        position = (np.array(position) * self.POSITION_SEARCH_SCALE).astype(np.int64)
        for area, image in self.GICityMask_dict.items():
            if point_in_area(position, area, threshold=0):
                x, y = position - area[:2]
                info = image[y, x]
                return info > 0

        return False

    @cached_property
    def GIReachableMask(self):
        file = gimap.get_file('GIReachableMask_0125x_pad125.png')
        image = load_image(file)
        return image
