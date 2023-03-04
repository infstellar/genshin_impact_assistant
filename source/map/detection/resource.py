import typing as t

import gimap
from cached_property import cached_property

from source.device.alas.decorator import has_cached_property, del_cached_property
from source.map.detection.utils import *
from source.util import IS_DEVICE_PC


class MiniMapResource:
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
    POSITION_SEARCH_SCALE = 0.5
    # Search the area that is 1.666x minimap, about 100px in wild on GIMAP
    POSITION_SEARCH_RADIUS = 1.666
    # Can't figure out why but the result_of_0.5_lookup_scale + 0.5 ~= result_of_1.0_lookup_scale
    POSITION_MOVE = (0.5, 0.5)

    # Radius to search direction arrow, about 15px
    DIRECTION_RADIUS = int(MINIMAP_RADIUS / 6)
    # Downscale direction arrows for faster run
    DIRECTION_SEARCH_SCALE = 0.5
    # Scale to 1280x720
    DIRECTION_ROTATION_SCALE = 1.0

    # Downscale GIMAP to run faster
    BIGMAP_SEARCH_SCALE = 0.25
    # Magic number that resize a 1280x720 screenshot to GIMAP_luma_05x_ps
    BIGMAP_POSITION_SCALE = 0.6137
    # Pad 600px, cause camera sight in game is larger than GIMAP
    BIGMAP_BORDER_PAD = int(600 * BIGMAP_SEARCH_SCALE)

    def __init__(self):
        # 'wild' or 'city'
        self.scene = 'wild'
        # Usually to be 0.4~0.5
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

        # Usually to be 0.4~0.5
        self.bigmap_similarity = 0.
        # Usually > 0.05
        self.bigmap_similarity_local = 0.
        # Current position on GIMAP with an error of about 0.1 pixel
        self.bigmap: t.Tuple[float, float] = (0, 0)

        if IS_DEVICE_PC:
            # Magic numbers for 1920x1080 desktop
            # 80% of Emulator, 1.5 * 80% = 1.2
            self.MINIMAP_CENTER = (60 + 108, 18 + 108)
            self.MINIMAP_RADIUS = 99
            self.POSITION_SCALE_DICT = {
                # In wild
                'wild': 1.5571 / 1.2,
                # In city
                'city': 0.5150 / 1.2,
            }
            self.DIRECTION_RADIUS = int(self.MINIMAP_RADIUS / 6)
            self.DIRECTION_ROTATION_SCALE = 1.0 / 1.2
            # Same as Emulator
            self.BIGMAP_POSITION_SCALE = 0.6137 / 1.5
            self.BIGMAP_BORDER_PAD = int(600 * self.BIGMAP_SEARCH_SCALE)
            # Set bigmap tp arguments
            self.MAP_POSI2MOVE_POSI_RATE = 0.2 # 移动距离与力度的比例
            self.BIGMAP_TP_OFFSET = 100 # 距离目标小于该误差则停止
            self.BIGMAP_MOVE_MAX = 100 # 最大移动力度
        else:
            # Magic numbers for 1920x1080 mobile
            self.MINIMAP_CENTER = (75 + 135, 22 + 135)
            self.MINIMAP_RADIUS = 124
            self.POSITION_SCALE_DICT = {
                # In wild
                'wild': 1.5571 / 1.5,
                # In city
                'city': 0.5150 / 1.5,
            }
            self.DIRECTION_RADIUS = int(self.MINIMAP_RADIUS / 6)
            self.DIRECTION_ROTATION_SCALE = 1.0 / 1.5
            self.BIGMAP_POSITION_SCALE = 0.6137 / 1.5
            self.BIGMAP_BORDER_PAD = int(600 * self.BIGMAP_SEARCH_SCALE)
            # Set bigmap tp arguments
            self.MAP_POSI2MOVE_POSI_RATE = 0.01 # 待调试
            self.BIGMAP_TP_OFFSET = 10 # 待调试
            self.BIGMAP_MOVE_MAX = 100

    @cached_property
    def _minimap_mask(self):
        mask = create_circular_mask(h=self.MINIMAP_RADIUS * 2, w=self.MINIMAP_RADIUS * 2)
        mask = (mask * 255).astype(np.uint8)
        return mask

    @cached_property
    def GIMAP(self):
        # This is how GIMAP_luma_05x_ps.png was generated

        # file = r'GIMAP.png'
        # image = load_image(file)
        # image = rgb2luma(image)
        # image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
        # Image.fromarray(image).save('GIMAP_luma_05x.png')

        # Then open it in PhotoShop, save as "GIMAP_luma_05x_ps.png" to make it smaller.

        # About 100ms to load
        file = gimap.GIMAP_luma_05x_ps()
        image = load_image(file)
        return image

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
                           fx=self.DIRECTION_SEARCH_SCALE, fy=self.DIRECTION_SEARCH_SCALE,
                           interpolation=cv2.INTER_NEAREST)
        # Image.fromarray(image).save('rotate_map.png')

        # Release ARROW_ROTATED if both maps are loaded.
        if has_cached_property(self, 'ARROW_ROTATION_MAP_ALL'):
            del_cached_property(self, 'ARROW_ROTATED')

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
                           fx=self.DIRECTION_SEARCH_SCALE, fy=self.DIRECTION_SEARCH_SCALE,
                           interpolation=cv2.INTER_NEAREST)
        # Image.fromarray(image).save('rotate_map_all.png')

        # Release ARROW_ROTATED if both maps are loaded.
        if has_cached_property(self, 'ARROW_ROTATION_MAP'):
            del_cached_property(self, 'ARROW_ROTATED')

        return image

    @cached_property
    def GICityMask_dict(self):
        # This is how GIMAP_luma_05x_ps.png was generated
        # GICityMask.png is in white background and has city area manually drawn in black

        # file = r'GICityMask.png'
        # image = load_image(file)
        # image = ~cv2.inRange(image, 0, 235)
        # image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
        #
        # scale = self.POSITION_SCALE_DICT['city'] * self.SEARCH_SCALE
        # local_size = self.MINIMAP_RADIUS * 2 * scale
        # local_size = int(local_size) + 1
        # # Pad search area, cause it's no an instant switch between city and wild
        # local_size += 20
        #
        # local_size = int(local_size // 2) * 2 + 1
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (local_size, local_size))
        # image = cv2.dilate(image, kernel)
        # Image.fromarray(image).save('GICityMask_05x.png')

        file = gimap.GICityMask_05x()
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
