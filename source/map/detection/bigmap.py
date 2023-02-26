from source.map.detection.resource import MiniMapResource
from source.map.detection.utils import *
from source.util import logger


class BigMap(MiniMapResource):
    def _predict_bigmap(self, image):
        scale = self.BIGMAP_POSITION_SCALE * self.BIGMAP_SEARCH_SCALE
        image = rgb2luma(image)
        center = np.array(image_size(image)) / 2 * scale
        image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)

        result = cv2.matchTemplate(self.GIMAP_bigmap, image, cv2.TM_CCOEFF_NORMED)
        _, sim, _, loca = cv2.minMaxLoc(result)
        # Remove < 0 because GIMAP has pure background
        result[result <= 0] = 0
        Image.fromarray((result * 255).astype(np.uint8)).save('match_result.png')

        # Gaussian filter to get local maximum
        local_maximum = cv2.subtract(result, cv2.GaussianBlur(result, (5, 5), 0))
        _, local_sim, _, loca = cv2.minMaxLoc(local_maximum)

        # local_maximum[local_maximum < 0] = 0
        # local_maximum[local_maximum > 0.1] = 0.1
        # Image.fromarray((local_maximum * 255 * 10).astype(np.uint8)).save('local_maximum.png')

        # Calculate the precise location using CUBIC
        precise = crop(result, area=area_offset((-4, -4, 4, 4), offset=loca))
        precise_sim, precise_loca = cubic_find_maximum(precise, precision=0.05)
        precise_loca -= 5

        global_loca = (loca + precise_loca + center) / self.BIGMAP_SEARCH_SCALE / self.POSITION_SEARCH_SCALE
        self.bigmap_similarity = sim
        self.bigmap_similarity_local = local_sim
        self.bigmap = global_loca
        return sim, global_loca

    def update(self, image):
        """
        Get position on bigmap (where you enter from the M button), costs about 125ms.

        The following attributes will be set:
        - position_similarity
        - position
        """
        self._predict_bigmap(image)

        # BigMap P:(5629.136, 4045.064) (0.622|0.123)
        logger.info(
            f'BigMap '
            f'P:({float2str(self.bigmap[0], 4)}, {float2str(self.bigmap[1], 4)}) '
            f'({float2str(self.bigmap_similarity, 3)}|{float2str(self.bigmap_similarity_local, 3)})'
        )
