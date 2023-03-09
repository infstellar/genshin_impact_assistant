import typing as t

from source.util import logger


class MiniMapConst:
    DETECT_Desktop_1080p = 'Desktop_1080p'
    DETECT_Desktop_720p = 'Desktop_720p'
    DETECT_Mobile_1080p = 'Mobile_1080p'
    DETECT_Mobile_720p = 'Mobile_720p'

    # Hard-coded coordinates under 1280x720
    MINIMAP_CENTER = (50 + 90, 14 + 90)
    MINIMAP_RADIUS = 90
    MINIMAP_POSITION_RADIUS = 83

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
    DIRECTION_RADIUS = int(MINIMAP_POSITION_RADIUS / 6)
    # Downscale direction arrows for faster run
    DIRECTION_SEARCH_SCALE = 0.5
    # Scale to 1280x720
    DIRECTION_ROTATION_SCALE = 1.0

    # Downscale GIMAP to run faster
    BIGMAP_SEARCH_SCALE = 0.25
    # Magic number that resize a 1280x720 screenshot to GIMAP_luma_05x_ps
    BIGMAP_POSITION_SCALE = 0.6137
    BIGMAP_POSITION_SCALE_ENKANOMIYA = 0.6137 * 0.7641
    # Pad 600px, cause camera sight in game is larger than GIMAP
    BIGMAP_BORDER_PAD = int(600 * BIGMAP_SEARCH_SCALE)

    def __init__(self, device_type):
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

        # The bigger the better
        self.rotation_confidence = 0.
        # Current cameta rotation with an error of about 1 degree
        self.rotation: int = 0

        # Usually to be 0.4~0.5
        self.bigmap_similarity = 0.
        # Usually > 0.05
        self.bigmap_similarity_local = 0.
        # Current position on GIMAP with an error of about 0.1 pixel
        self.bigmap: t.Tuple[float, float] = (0, 0)

        if device_type == MiniMapConst.DETECT_Desktop_1080p:
            # Magic numbers for 1920x1080 desktop
            # 80% of Emulator, 1.5 * 80% = 1.2
            self.MINIMAP_CENTER = (60 + 108, 17 + 108)
            self.MINIMAP_RADIUS = 108
            self.MINIMAP_POSITION_RADIUS = 99
            self.POSITION_SCALE_DICT = {
                # In wild
                'wild': 1.5571 / 1.2,
                # In city
                'city': 0.5150 / 1.2,
            }
            self.DIRECTION_RADIUS = int(self.MINIMAP_POSITION_RADIUS / 6)
            self.DIRECTION_ROTATION_SCALE = 1.0 / 1.2
            # Same as Emulator
            self.BIGMAP_POSITION_SCALE = 0.6137 / 1.5
            self.BIGMAP_POSITION_SCALE_ENKANOMIYA = 0.6137 * 0.7641 / 1.5
            self.BIGMAP_BORDER_PAD = int(600 * self.BIGMAP_SEARCH_SCALE)

        elif device_type == MiniMapConst.DETECT_Desktop_720p:
            logger.error(f'Minimap detection on {device_type} is not supported')

        elif device_type == MiniMapConst.DETECT_Mobile_1080p:
            # Magic numbers for 1920x1080 mobile
            self.MINIMAP_CENTER = (75 + 135, 21 + 135)
            self.MINIMAP_RADIUS = 135
            self.MINIMAP_POSITION_RADIUS = 124
            self.POSITION_SCALE_DICT = {
                # In wild
                'wild': 1.5571 / 1.5,
                # In city
                'city': 0.5150 / 1.5,
            }
            self.DIRECTION_RADIUS = int(self.MINIMAP_POSITION_RADIUS / 6)
            self.DIRECTION_ROTATION_SCALE = 1.0 / 1.5
            self.BIGMAP_POSITION_SCALE = 0.6137 / 1.5
            self.BIGMAP_POSITION_SCALE_ENKANOMIYA = 0.6137 * 0.7641 / 1.5
            self.BIGMAP_BORDER_PAD = int(600 * self.BIGMAP_SEARCH_SCALE)

        elif device_type == MiniMapConst.DETECT_Mobile_720p:
            # Default
            pass

        else:
            logger.error(f'Minimap detection on {device_type} is not supported')
