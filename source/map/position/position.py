import numpy as np
from source.map.extractor.convert import MapConverter


class GenshinPosition(MapConverter):
    def __init__(self,position) -> None:
        if isinstance(position,list):
            self.position=np.array(position)
        else:
            self.position=position

        self.tianli = self._get_TianLi_position()
        self.kongying = self._get_kongying_position()
        self.gimap = self._get_GIMAP_position()
        
    def _get_TianLi_position(self) -> np.ndarray:
        pass

    def _get_GIMAP_position(self) -> np.ndarray:
        pass

    def _get_kongying_position(self) -> np.ndarray:
        pass

class TianLiPosition(GenshinPosition):
    def __init__(self,position) -> None:
        super().__init__(position)

    def _get_TianLi_position(self):
        return self.position

    def _get_GIMAP_position(self):
        return self.convert_cvAutoTrack_to_GIMAP(self.position)

    def _get_kongying_position(self):
        return self.convert_cvAutoTrack_to_kongying(self.position)

class GIMAPPosition(GenshinPosition):
    def __init__(self,position) -> None:
        super().__init__(position)

    def _get_TianLi_position(self):
        return self.convert_GIMAP_to_cvAutoTrack(self.position)

    def _get_GIMAP_position(self):
        return self.position

    def _get_kongying_position(self):
        return self.convert_GIMAP_to_kongying(self.position)

class KongYingPosition(GenshinPosition):
    def __init__(self,position) -> None:
        super().__init__(position)

    def _get_TianLi_position(self):
        return self.convert_kongying_to_cvAutoTrack(self.position)

    def _get_GIMAP_position(self):
        return self.convert_kongying_to_GIMAP(self.position)

    def _get_kongying_position(self):
        return self.position