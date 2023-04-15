from source.map.detection.resource import MiniMapResource
from source.map.detection.utils import *
from source.map.extractor.convert import MapConverter
from source.util import logger


class BigMap(MiniMapResource):
    def _predict_bigmap(self, image, layer=MapConverter.LAYER_Teyvat):
        if layer in [
            MapConverter.LAYER_Enkanomiya,
            MapConverter.LAYER_ThreeRealmsGatewayOffering,
            MapConverter.LAYER_TheChasm,
        ]:
            scale = self.BIGMAP_POSITION_SCALE_ENKANOMIYA * self.BIGMAP_SEARCH_SCALE
        else:
            scale = self.BIGMAP_POSITION_SCALE * self.BIGMAP_SEARCH_SCALE
        image = rgb2luma(image)
        center = np.array(image_size(image)) / 2 * scale
        image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)

        result = cv2.matchTemplate(self.GIBigmap, image, cv2.TM_CCOEFF_NORMED)
        _, sim, _, loca = cv2.minMaxLoc(result)
        # Image.fromarray((result * 255).astype(np.uint8)).save('match_result.png')

        # Gaussian filter to get local maximum
        local_maximum = cv2.subtract(result, cv2.GaussianBlur(result, (9, 9), 0))
        mask = image_center_crop(self.GIReachableMask, size=image_size(local_maximum))
        local_maximum = cv2.copyTo(local_maximum, mask)
        _, local_sim, _, loca = cv2.minMaxLoc(local_maximum)

        # local_maximum = local_maximum * 255 * 10
        # local_maximum[local_maximum < 0] = 0
        # local_maximum[local_maximum > 255] = 255
        # Image.fromarray(local_maximum.astype(np.uint8)).save('local_maximum.png')

        # Calculate the precise location using CUBIC
        precise = crop(result, area=area_offset((-4, -4, 4, 4), offset=loca))
        precise_sim, precise_loca = cubic_find_maximum(precise, precision=0.05)
        precise_loca -= 5

        global_loca = (loca + precise_loca + center - self.BIGMAP_BORDER_PAD) \
                      / self.BIGMAP_SEARCH_SCALE / self.POSITION_SEARCH_SCALE
        self.bigmap_similarity = sim
        self.bigmap_similarity_local = local_sim
        self.bigmap = global_loca
        return sim, global_loca

    def update_bigmap(self, image, layer=MapConverter.LAYER_Teyvat):
        """
        Get position on bigmap (where you enter from the M button), costs about 125ms.

        The following attributes will be set:
        - bigmap_similarity
        - bigmap_similarity_local
        - bigmap
        """
        self._predict_bigmap(image, layer=layer)

        # BigMap P:(5629.136, 4045.064) (0.622|0.123)
        logger.trace(
            f'BigMap '
            f'P:({float2str(self.bigmap[0], 4)}, {float2str(self.bigmap[1], 4)}) '
            f'({float2str(self.bigmap_similarity, 3)}|{float2str(self.bigmap_similarity_local, 3)})'
        )

# if __name__ == '__main__':
#     bm = BigMap(BigMap.DETECT_Desktop_1080p)
#     from source.interaction.interaction_core import itt
#     import time
#
#     while 1:
#         bm.update_bigmap(itt.capture(jpgmode=0))
#         time.sleep(0.1)


# if __name__ == '__main__':
#     from source.device.genshin.genshin import Genshin
#
#     device = Genshin('127.0.0.1:7555')
#     self = BigMap('Emulator')
#
#     device.screenshot_interval_set(0.3)
#     device.disable_stuck_detection()
#     while 1:
#         device.screenshot()
#         self.update_bigmap(device.image)
