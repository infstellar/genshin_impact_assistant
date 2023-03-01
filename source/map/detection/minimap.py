import typing as t

from source.map.detection.resource import MiniMapResource
from source.map.detection.utils import *
from source.util import logger


class MiniMap(MiniMapResource):
    def init_position(self, position: t.Tuple[int, int]):
        self.position = position

    def _get_minimap(self, image, radius):
        area = area_offset((-radius, -radius, radius, radius), offset=self.MINIMAP_CENTER)
        image = crop(image, area)
        return image

    def _predict_position(self, image, scale):
        """
        Args:
            image:
            scale:

        Returns:
            float: Precise similarity
            float: local_sim
            tuple[float, float]: Location on GIMAP
        """
        scale *= self.POSITION_SEARCH_SCALE
        local = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
        # Product search area
        search_position = np.array(self.position, dtype=np.int64)
        search_size = np.array(image_size(local)) * self.POSITION_SEARCH_RADIUS
        search_size = (search_size // 2 * 2).astype(np.int64)
        search_area = area_offset((0, 0, *search_size), offset=(-search_size // 2).astype(np.int64))
        search_area = area_offset(search_area, offset=np.multiply(search_position, self.POSITION_SEARCH_SCALE))
        search_area = np.array(search_area).astype(np.int64)
        search_image = crop(self.GIMAP, search_area)

        result = cv2.matchTemplate(search_image, local, cv2.TM_CCOEFF_NORMED)
        _, sim, _, loca = cv2.minMaxLoc(result)
        # result[result <= 0] = 0
        # Image.fromarray((result * 255).astype(np.uint8)).save('match_result.png')

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

        # Location on search_image
        lookup_loca = precise_loca + loca + np.array(image_size(image)) * scale / 2
        # Location on GIMAP
        global_loca = (lookup_loca + search_area[:2]) / self.POSITION_SEARCH_SCALE
        # Can't figure out why but the result_of_0.5_lookup_scale + 0.5 ~= result_of_1.0_lookup_scale
        global_loca += self.POSITION_MOVE
        return precise_sim, local_sim, global_loca

    @property
    def _position_scale_dict(self) -> t.Dict[str, float]:
        dic = {}
        dic['wild'] = self.POSITION_SCALE_DICT['wild']
        if self._position_in_GICityMask(self.position):
            dic['city'] = self.POSITION_SCALE_DICT['city']
        return dic

    def update_position(self, image):
        """
        Get position on GIMAP, costs about 1.41ms.

        The following attributes will be set:
        - position_similarity
        - position
        - position_scene
        """
        image = self._get_minimap(image, self.MINIMAP_RADIUS)
        image = rgb2luma(image)
        image &= self._minimap_mask

        best_sim = -1.
        best_local_sim = -1.
        best_loca = (0, 0)
        best_scene = 'wild'
        for scene, scale in self._position_scale_dict.items():
            similarity, local_sim, location = self._predict_position(image, scale)
            # print(scene, scale, similarity, location)
            if similarity > best_sim:
                best_sim = similarity
                best_local_sim = local_sim
                best_loca = location
                best_scene = scene

        self.position_similarity = round(best_sim, 3)
        self.position_similarity_local = round(best_local_sim, 3)
        self.position = tuple(np.round(best_loca, 1))
        self.scene = best_scene

    def update_direction(self, image):
        """
        Get direction of character, costs about 0.64ms.

        The following attributes will be set:
        - direction_similarity
        - direction
        """
        image = self._get_minimap(image, self.DIRECTION_RADIUS)

        image = color_similarity_2d(image, color=(0, 229, 255))
        try:
            area = area_pad(get_bbox(image, threshold=15), pad=-1)
        except IndexError:
            # IndexError: index 0 is out of bounds for axis 0 with size 0
            logger.warning('No direction arrow on minimap')
            return
        image = crop(image, area=area)
        scale = self.DIRECTION_ROTATION_SCALE * self.DIRECTION_SEARCH_SCALE
        mapping = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
        result = cv2.matchTemplate(self.ARROW_ROTATION_MAP, mapping, cv2.TM_CCOEFF_NORMED)
        _, sim, _, loca = cv2.minMaxLoc(result)
        loca = np.array(loca) / self.DIRECTION_SEARCH_SCALE // (self.DIRECTION_RADIUS * 2)
        degree = int((loca[0] + loca[1] * 8) * 5)

        def to_map(x):
            return int((x * self.DIRECTION_RADIUS * 2 + self.DIRECTION_RADIUS) * self.POSITION_SEARCH_SCALE)

        # Row on ARROW_ROTATION_MAP_ALL
        row = int(degree // 8) + 45
        # Calculate +-1 rows to get result with a precision of 1
        row = (row - 1, row + 2)
        # Convert to ARROW_ROTATION_MAP_ALL and to be 5px larger
        row = (to_map(row[0]) - 5, to_map(row[1]) + 5)

        precise_map = self.ARROW_ROTATION_MAP_ALL[row[0]:row[1], :]
        result = cv2.matchTemplate(precise_map, mapping, cv2.TM_CCOEFF_NORMED)

        def to_map(x):
            return int((x * self.DIRECTION_RADIUS * 2) * self.POSITION_SEARCH_SCALE)

        def get_precise_sim(d):
            y, x = divmod(d, 8)
            im = result[to_map(y):to_map(y + 1), to_map(x):to_map(x + 1)]
            _, sim, _, _ = cv2.minMaxLoc(im)
            return sim

        precise = np.array([[get_precise_sim(_) for _ in range(24)]])
        precise_sim, precise_loca = cubic_find_maximum(precise, precision=0.1)
        precise_loca = degree // 8 * 8 - 8 + precise_loca[0]

        self.direction_similarity = round(precise_sim, 3)
        self.direction = precise_loca % 360

    def update_minimap(self, image):
        self.update_position(image)
        self.update_direction(image)

        # MiniMap P:(4451.5, 3113.0) (0.184|0.050), S:wild, D:259.5 (0.949)
        logger.info(
            f'MiniMap '
            f'P:({float2str(self.position[0], 4)}, {float2str(self.position[1], 4)}) '
            f'({float2str(self.position_similarity, 3)}|{float2str(self.position_similarity_local, 3)}), '
            f'S:{self.scene}, '
            f'D:{float2str(self.direction, 3)} ({float2str(self.direction_similarity, 3)})')

    @property
    def is_scene_in_wild(self) -> bool:
        return self.scene == 'wild'

    @property
    def is_scene_in_city(self) -> bool:
        return self.scene == 'city'

    def is_position_near(self, position, threshold=1) -> bool:
        diff = np.linalg.norm(np.subtract(position, self.position))
        return diff <= threshold

    def is_direction_near(self, direction, threshold=10) -> bool:
        diff = (self.direction - direction) % 360
        return diff <= threshold or diff >= 360 - threshold


# if __name__ == '__main__':
#     """
#     MiniMap 模拟器监听测试
#     """
#     from source.device import Device
#
#     device = Device('127.0.0.1:7555')
#     device.disable_stuck_detection()
#     device.screenshot_interval_set(0.3)
#     minimap = MiniMap('Emulator')
#
#     # 从璃月港传送点出发，初始坐标大概大概50px以内就行
#     # 坐标位置是 GIMAP 的图片坐标
#     minimap.init_position((4580, 3046))
#     # 你可以移动人物，GIA会持续监听小地图位置和角色朝向
#     while 1:
#         device.screenshot()
#         minimap.update_minimap(device.image)


# if __name__ == '__main__':
#     """
#     MiniMap windows窗口监听测试
#     """
#     from source.interaction.capture import WindowsCapture
#     import time
#
#     device = WindowsCapture()
#     minimap = MiniMap('Windows')
#     # 从风起地传送点出发，初始坐标大概大概50px以内就行
#     # 坐标位置是 GIMAP 的图片坐标
#     minimap.init_position((5783, 1042))
#     # 你可以移动人物，GIA会持续监听小地图位置和角色朝向
#     while 1:
#         image = device.capture()
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         if image.shape != (1080, 1920, 3):
#             time.sleep(0.3)
#             continue
#
#         minimap.update_minimap(image)
#         time.sleep(0.3)
