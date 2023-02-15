from functools import wraps

import numpy as np
from PIL import Image

from source.device.alas.timer import Timer
from source.device.alas.utils import load_image
from source.device.device.device import Device
from source.device.method.utils import HierarchyButton
from source.util import logger


def func_debug(function):
    """
    log debugs before and after a function
    """

    @wraps(function)
    def wrapper(*args, **kwargs):
        logger.debug(f'{function.__name__} enter')
        result = function(*args, **kwargs)
        logger.debug(f'{function.__name__} exit')
        return result

    return wrapper


class AppBase(Device):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interval_timer = {}

    def ensure_button(self, button):
        """
        Args:
            button (HierarchyButton, str):

        Returns:
            HierarchyButton:
        """
        if isinstance(button, str):
            button = HierarchyButton(self.hierarchy, button)

        return button

    def appear(self, button, interval=0):
        """
        Args:
            button (HierarchyButton, str):
            interval (int, float): interval between two active events.

        Returns:
            bool:

        Examples:
            Hierarchy detection (detect elements with xpath):
            ```
            self.device.dump_hierarchy()
            self.appear('//*[@resource-id="..."]')
            ```
        """
        button = self.ensure_button(button)
        self.stuck_record_add(button)

        if interval:
            if button.name in self.interval_timer:
                if self.interval_timer[button.name].limit != interval:
                    self.interval_timer[button.name] = Timer(interval)
            else:
                self.interval_timer[button.name] = Timer(interval)
            if not self.interval_timer[button.name].reached():
                return False

        appear = bool(button)

        if appear and interval:
            self.interval_timer[button.name].reset()

        return appear

    def appear_then_click(self, button, interval=3):
        button = self.ensure_button(button)
        appear = self.appear(button, interval=interval)
        if appear:
            self.click(button)
        return appear

    def interval_get(self, button) -> Timer:
        button = self.ensure_button(button)
        if button.name in self.interval_timer:
            return self.interval_timer[button.name]
        else:
            self.interval_timer[button.name] = Timer(3)
            return self.interval_timer[button.name]

    def interval_reset(self, button):
        if isinstance(button, (list, tuple)):
            for b in button:
                self.interval_reset(b)
            return

        self.interval_get(button).reset()

    def interval_clear(self, button):
        if isinstance(button, (list, tuple)):
            for b in button:
                self.interval_clear(b)
            return

        self.interval_get(button).clear()

    _image_file = ''

    @property
    def image_file(self):
        return self._image_file

    @image_file.setter
    def image_file(self, value):
        """
        For development.
        Load image from local file system and set it to self.device.image
        Test an image without taking a screenshot from emulator.
        """
        if isinstance(value, Image.Image):
            value = np.array(value)
        elif isinstance(value, str):
            value = load_image(value)

        self.image = value
