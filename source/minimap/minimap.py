import typing as t

import gimap
from cached_property import cached_property

from source.minimap.utils import *
from source.util import logger


class MiniMap:
    # Hard-coded coordinates under 1280x720
    MINIMAP_CENTER = (50 + 90, 15 + 90)
    MINIMAP_RADIUS = 83

    # Magic number that resize a 1280x720 minimap to GIMAP
    POSITION_SCALE_DICT = {
        # In wild
        'wild': 1.5571,
        # In city
        'city': 0.5150,
    }
    # Downscale GIMAP and minimap for faster run
    SEARCH_SCALE = 0.5
    # Search the area that is 1.666x minimap, about 100px in wild on GIMAP
    SEARCH_RADIUS = 1.666

    # Radius to search direction arrow, about 15px
    DIRECTION_RADIUS = int(MINIMAP_RADIUS / 6)
    # Downscale direction arrows for faster run
    DIRECTION_ROTATATION_MAP_SCALE = 0.5

    def __init__(self):
        # 'wild' or 'city'
        self.scene = 'wild'
        # Usually to be 0.4~0.5
        # Warnnings will be logged if similarity <= 0.25
        self.position_similarity = 0.
        # Usually > 0.05
        self.position_similarity_local = 0.
        # Current position on GIMAP with an error of about 0.1 pixel
        self.position: t.Tuple[float, float] = (0, 0)

        # Usually to be 0.90~0.98
        # Warnnings will be logged if similarity <= 0.8
        self.direction_similarity = 0.
        # Current character direction with an error of about 0.1 degree
        self.direction: float = 0.

    @cached_property
    def GIMAP(self):
        # This is how GIMAP_luma_05x_ps.png was generated

        # file = r'GIMAP.png'
        # image = load_image(file)
        # image = rgb2luma(image)
        # image = cv2.resize(image, None, fx=self.SEARCH_SCALE, fy=self.SEARCH_SCALE, interpolation=cv2.INTER_NEAREST)
        # Image.fromarray(image).save('GIMAP_luma_05x.png')

        # Then open it in PhotoShop, save as "GIMAP_luma_05x_ps.png" to make it smaller.

        # About 100ms to load
        file = gimap.GIMAP_luma_05x_ps()
        image = load_image(file)
        return image

    @cached_property
    def ARROW_ROTATED(self):
        """
        Returns:

        """
        file = gimap.ARROW()
        image = load_image(file)
        arrows = {}
        for degree in range(0, 360):
            rotated = rotate_bound(image, degree)
            rotated = crop(rotated, area=get_bbox(rotated, threshold=15))
            # rotated = cv2.resize(rotated, None, fx=self.ROTATE, fy=self.ROTATE, interpolation=cv2.INTER_NEAREST)
            rotated = color_similarity_2d(rotated, color=(0, 229, 255))
            arrows[degree] = rotated
        return arrows

    @cached_property
    def ARROW_ROTATION_MAP(self):
        radius = self.DIRECTION_RADIUS
        image = np.zeros((10 * radius * 2, 9 * radius * 2), dtype=np.uint8)
        for degree in range(0, 360, 5):
            y, x = divmod(degree / 5, 8)
            rotated = self.ARROW_ROTATED.get(degree)
            point = (radius + int(y) * radius * 2, radius + int(x) * radius * 2)
            # print(degree, y, x, point[0],point[0] + radius, point[1],point[1] + rotated.shape[1])
            image[point[0]:point[0] + rotated.shape[0], point[1]:point[1] + rotated.shape[1]] = rotated
        image = cv2.resize(image, None,
                           fx=self.DIRECTION_ROTATATION_MAP_SCALE, fy=self.DIRECTION_ROTATATION_MAP_SCALE,
                           interpolation=cv2.INTER_NEAREST)
        # Image.fromarray(image).save('rotate_map.png')
        return image

    @cached_property
    def ARROW_ROTATION_MAP_ALL(self):
        radius = self.DIRECTION_RADIUS
        image = np.zeros((136 * radius * 2, 9 * radius * 2), dtype=np.uint8)
        for degree in range(360 * 3):
            y, x = divmod(degree, 8)
            rotated = self.ARROW_ROTATED.get(degree % 360)
            point = (radius + int(y) * radius * 2, radius + int(x) * radius * 2)
            # print(degree, y, x, point[0],point[0] + radius, point[1],point[1] + rotated.shape[1])
            image[point[0]:point[0] + rotated.shape[0], point[1]:point[1] + rotated.shape[1]] = rotated
        image = cv2.resize(image, None,
                           fx=self.DIRECTION_ROTATATION_MAP_SCALE, fy=self.DIRECTION_ROTATATION_MAP_SCALE,
                           interpolation=cv2.INTER_NEAREST)
        # Image.fromarray(image).save('rotate_map_all.png')
        return image

    def init_position(self, position: t.Tuple[int, int]):
        self.position = position

    def _get_minimap(self, image, radius):
        area = area_offset((-radius, -radius, radius, radius), offset=self.MINIMAP_CENTER)
        image = crop(image, area)
        return image

    @cached_property
    def _minimap_mask(self):
        mask = create_circular_mask(h=self.MINIMAP_RADIUS * 2, w=self.MINIMAP_RADIUS * 2)
        mask = (mask * 255).astype(np.uint8)
        mask = cv2.merge([mask, mask, mask])
        return mask

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
        scale *= self.SEARCH_SCALE
        local = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
        # Product search area
        search_position = np.array(self.position, dtype=np.int64)
        search_size = np.array(image_size(local)) * self.SEARCH_RADIUS
        search_size = (search_size // 2 * 2).astype(np.int64)
        search_area = area_offset((0, 0, *search_size), offset=(-search_size // 2).astype(np.int64))
        search_area = area_offset(search_area, offset=np.multiply(search_position, self.SEARCH_SCALE))
        search_area = np.array(search_area).astype(np.int64)
        search_image = crop(self.GIMAP, search_area)

        result = cv2.matchTemplate(search_image, local, cv2.TM_CCOEFF_NORMED)
        _, sim, _, loca = cv2.minMaxLoc(result)
        # result[result <= 0] = 0
        # Image.fromarray((result * 255).astype(np.uint8)).save('match_result.png')

        # Gaussian filter to get local maximum
        local_maximum = cv2.subtract(result, cv2.GaussianBlur(result, (5, 5), 0))
        _, local_sim, _, loca = cv2.minMaxLoc(local_maximum)

        # Calculate the precise location using CUBIC
        precise = crop(result, area=area_offset((-4, -4, 4, 4), offset=loca))
        precise_sim, precise_loca = cubic_find_maximum(precise, precision=0.05)
        precise_loca -= 5

        # Location on search_image
        lookup_loca = precise_loca + loca + np.array(image_size(image)) * scale / 2
        # Location on GIMAP
        global_loca = (lookup_loca + search_area[:2]) / self.SEARCH_SCALE
        # Can't figure out why but the result_of_0.5_lookup_scale + 0.5 ~= result_of_1.0_lookup_scale
        if self.SEARCH_SCALE == 0.5:
            global_loca += 0.5
        return precise_sim, local_sim, global_loca

    def update_position(self, image):
        """
        Get position on GIMAP, costs about 1.41ms.

        The following attributes will be set:
        - position_similarity
        - position
        - position_scene
        """
        image = self._get_minimap(image, self.MINIMAP_RADIUS) & self._minimap_mask
        image = rgb2luma(image)

        best_sim = 0.
        best_local_sim = 0.
        best_loca = (0, 0)
        best_scene = 'wild'
        for scene, scale in self.POSITION_SCALE_DICT.items():
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
        mapping = cv2.resize(image, None,
                             fx=self.DIRECTION_ROTATATION_MAP_SCALE, fy=self.DIRECTION_ROTATATION_MAP_SCALE,
                             interpolation=cv2.INTER_NEAREST)
        result = cv2.matchTemplate(self.ARROW_ROTATION_MAP, mapping, cv2.TM_CCOEFF_NORMED)
        _, sim, _, loca = cv2.minMaxLoc(result)
        loca = np.array(loca) / self.DIRECTION_ROTATATION_MAP_SCALE // (self.DIRECTION_RADIUS * 2)
        degree = int((loca[0] + loca[1] * 8) * 5)

        def to_map(x):
            return int((x * self.DIRECTION_RADIUS * 2 + self.DIRECTION_RADIUS) * self.SEARCH_SCALE)

        # Row on ARROW_ROTATION_MAP_ALL
        row = int(degree // 8) + 45
        # Calculate +-1 rows to get result with a precision of 1
        row = (row - 1, row + 2)
        # Convert to ARROW_ROTATION_MAP_ALL and to be 5px larger
        row = (to_map(row[0]) - 5, to_map(row[1]) + 5)

        precise_map = self.ARROW_ROTATION_MAP_ALL[row[0]:row[1], :]
        result = cv2.matchTemplate(precise_map, mapping, cv2.TM_CCOEFF_NORMED)

        def to_map(x):
            return int((x * self.DIRECTION_RADIUS * 2) * self.SEARCH_SCALE)

        def get_precise_sim(d):
            y, x = divmod(d, 8)
            im = result[to_map(y):to_map(y + 1), to_map(x):to_map(x + 1)]
            _, sim, _, _ = cv2.minMaxLoc(im)
            return sim

        precise = np.array([[get_precise_sim(_) for _ in range(24)]])
        precise_sim, precise_loca = cubic_find_maximum(precise, precision=0.1)
        precise_loca = degree // 8 * 8 - 8 + precise_loca[0]

        self.direction_similarity = round(precise_sim, 3)
        self.direction = precise_loca

    def update(self, image):
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
    def is_scene_in_wild(self):
        return self.scene == 'wild'

    @property
    def is_scene_in_city(self):
        return self.scene == 'city'

    def is_position_near(self, position, threshold=2):
        diff = np.linalg.norm(np.subtract(position, self.position))
        return diff <= threshold

    def is_direction_near(self, direction, threshold=10):
        diff = (self.direction - direction) % 360
        return diff <= threshold or diff >= 360 - threshold


if __name__ == '__main__':
    """
    MiniMap 监听测试
    """
    from source.device.device.device import Device

    device = Device('127.0.0.1:7555')
    device.disable_stuck_detection()
    device.screenshot_interval_set(0.3)
    minimap = MiniMap()

    # 从璃月港传送点出发，初始坐标大概大概50px以内就行
    # 坐标位置是 GIMAP 的图片坐标
    minimap.init_position((4580, 3046))
    # 你可以移动人物，GIA会持续监听小地图位置和角色朝向
    while 1:
        device.screenshot()
        minimap.update(device.image)
