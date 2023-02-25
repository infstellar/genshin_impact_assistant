import cv2
from cached_property import cached_property

from source.map.minimap.resource import MiniMapResource


class BigMapResource(MiniMapResource):
    # Downscale GIMAP to run faster
    BIGMAP_SEARCH_SCALE = 0.25
    # Magic number that resize a 1280x720 screenshot to GIMAP_luma_05x_ps
    BIGMAP_POSITION_SCALE = 0.6137

    @cached_property
    def GIMAP_bigmap(self):
        image = self.GIMAP
        image = cv2.resize(image, None, fx=self.BIGMAP_SEARCH_SCALE, fy=self.BIGMAP_SEARCH_SCALE,
                           interpolation=cv2.INTER_NEAREST)

        # Pad 600px, cause camera sight in game is larger than GIMAP
        border = int(600 * self.BIGMAP_SEARCH_SCALE)
        border = (border, border, border, border)
        image = cv2.copyMakeBorder(image, *border, borderType=cv2.BORDER_REPLICATE)
        return image
