import os

from cached_property import cached_property

from source.map.detection.resource_const import MiniMapConst
from source.map.detection.utils import *


class MiniMapResourceGenerate(MiniMapConst):
    def __init__(self, folder='./'):
        super().__init__(device_type=MiniMapConst.DETECT_Mobile_720p)
        self.folder = folder

    def load_image(self, file):
        return load_image(os.path.join(self.folder, file))

    def save_image(self, image, file):
        Image.fromarray(image).save(os.path.join(self.folder, file))

    """
    Input images
    """

    @cached_property
    def GIMAP(self):
        # GIMAP is from cvAutoTrack
        return self.load_image('GIMAP.png')

    @cached_property
    def GICityMask(self):
        # GICityMask.png is in black background and has city area manually drawn in white
        image = self.load_image('GICityMask.png')
        if image.ndim == 3:
            image = rgb2gray(image)
        return image

    @cached_property
    def GIReachableMask(self):
        # GICityMask.png is in black background and has city area manually drawn in white
        image = self.load_image('GIReachableMask.png')
        if image.ndim == 3:
            image = rgb2gray(image)
        return image

    @cached_property
    def ARROW(self):
        # GIMAP is capture from 1280x720 mobile
        return self.load_image('ARROW.png')

    """
    Output images
    """

    @cached_property
    def GIMAP_luma_05x(self):
        image = self.GIMAP
        image = rgb2luma(image)
        image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
        self.save_image(image, 'GIMAP_luma_05x.png')

        # Then open it in PhotoShop, save as "GIMAP_luma_05x_ps.png" to make it smaller.
        return image

    @cached_property
    def GIBigmap_luma_0125x_pad125(self):
        image = self.GIMAP_luma_05x
        image = cv2.resize(image, None, fx=self.BIGMAP_SEARCH_SCALE, fy=self.BIGMAP_SEARCH_SCALE,
                           interpolation=cv2.INTER_NEAREST)

        # Pad 600px, cause camera sight in game is larger than GIMAP
        border = int(600 * self.BIGMAP_SEARCH_SCALE)
        image = cv2.copyMakeBorder(image, border, border, border, border, borderType=cv2.BORDER_REPLICATE)

        blur = cv2.GaussianBlur(image, (9, 9), 0)
        blur[border:-border, border:-border] = image[border:-border, border:-border]
        image = blur

        self.save_image(image, 'GIBigmap_luma_0125x_pad125.png')
        return image

    @cached_property
    def ARROW_ROTATED(self):
        """
        Returns:

        """
        image = self.ARROW
        arrows = {}
        for degree in range(0, 360):
            rotated = rotate_bound(image, degree)
            rotated = crop(rotated, area=get_bbox(rotated, threshold=15))
            # rotated = cv2.resize(rotated, None, fx=self.ROTATE, fy=self.ROTATE, interpolation=cv2.INTER_NEAREST)
            rotated = color_similarity_2d(rotated, color=(0, 229, 255))
            arrows[degree] = rotated
        return arrows

    @cached_property
    def ArrowRotateMap(self):
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

        self.save_image(image, 'ArrowRotateMap.png')
        return image

    @cached_property
    def ArrowRotateMapAll(self):
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

        self.save_image(image, 'ArrowRotateMapAll.png')
        return image

    @cached_property
    def GICityOuter_05x(self):
        # This is how GICityOuter_05x.png was generated
        # GICityMask.png is in white background and has city area manually drawn in black

        image = self.GICityMask
        image = ~cv2.inRange(image, 0, 235)
        image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)

        scale = self.POSITION_SCALE_DICT['city'] * self.POSITION_SEARCH_SCALE
        local_size = self.MINIMAP_POSITION_RADIUS * 2 * scale
        local_size = int(local_size) + 1
        # Pad search area, cause it's no an instant switch between city and wild
        local_size += 20

        local_size = int(local_size // 2) * 2 + 1
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (local_size, local_size))
        image = cv2.dilate(image, kernel)

        self.save_image(image, 'GICityOuter_05x.png')
        return image

    @cached_property
    def GICityInner_05x(self):
        # This is how GICityInner_05x.png was generated
        # GICityMask.png is in white background and has city area manually drawn in black

        image = self.GICityMask
        image = ~cv2.inRange(image, 0, 235)
        image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)

        # Inner pad 10
        local_size = 10

        local_size = int(local_size) * 2 + 1
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (local_size, local_size))
        image = cv2.erode(image, kernel)

        self.save_image(image, 'GICityInner_05x.png')
        return image

    @cached_property
    def GIReachableMask_0125x_pad125(self):
        image = self.GIReachableMask
        image = ~cv2.inRange(image, 0, 235)
        image = cv2.resize(image, None, fx=0.125, fy=0.125, interpolation=cv2.INTER_NEAREST)

        image = image_center_pad(image, size=image_size(self.GIBigmap_luma_0125x_pad125))

        kernel = (30, 20)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel)
        image = cv2.dilate(image, kernel)
        self.save_image(image, 'GIReachableMask_0125x_pad125.png')
        return image

    def generate(self):
        _ = self.GIMAP_luma_05x
        _ = self.GIBigmap_luma_0125x_pad125
        _ = self.GIReachableMask_0125x_pad125
        _ = self.ArrowRotateMap
        _ = self.ArrowRotateMapAll
        _ = self.GICityOuter_05x
        _ = self.GICityInner_05x


if __name__ == '__main__':
    self = MiniMapResourceGenerate(r'')
    self.generate()
