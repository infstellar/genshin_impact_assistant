from source.device.genshin.base import AppBase


class Genshin(AppBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config.Emulator_PackageName = 'com.miHoYo.Yuanshen'
