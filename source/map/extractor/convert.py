import numpy as np

from source.device.alas.utils import point_in_area
from source.util import IS_DEVICE_PC


class UnknownPositionTypeError(Exception):
    pass

class MapConverter:
    """
    Convert coordinates among maps.

    cvAutoTrack: https://github.com/GengGode/cvAutoTrack
    GIMAP: Raw map image file in cvAutoTrack, named `GIMAP.png`
    kongying: https://v3.yuanshen.site/
    """
    LAYER_Domain = 'Domain'
    LAYER_Teyvat = 'Teyvat'
    LAYER_Enkanomiya = 'Enkanomiya'
    LAYER_TheChasm = 'TheChasm'
    LAYER_GoldenAppleArchipelago = 'GoldenAppleArchipelago'
    LAYER_ThreeRealmsGatewayOffering = 'ThreeRealmsGatewayOffering'

    REGION_Mondstadt = 'Mondstadt'
    REGION_GoldenAppleArchipelago = 'GoldenAppleArchipelago'
    REGION_Liyue = 'Liyue'
    REGION_TheChasm = 'TheChasm'
    REGION_Inazuma = 'Inazuma'
    REGION_ThreeRealmsGatewayOffering = 'ThreeRealmsGatewayOffering'
    REGION_Enkanomiya = 'Enkanomiya'
    REGION_Sumeru = 'Sumeru'

    TP_Statue = 'Statue'
    TP_Teleporter = 'Teleporter'
    TP_Domain = 'Domain'
    TP_Instance = 'Instance'

    @classmethod
    def convert_REGION_to_LAYER(cls, region: str) -> str:
        if region == cls.REGION_GoldenAppleArchipelago:
            return cls.LAYER_GoldenAppleArchipelago
        if region == cls.REGION_ThreeRealmsGatewayOffering:
            return cls.LAYER_ThreeRealmsGatewayOffering
        if region == cls.REGION_TheChasm:
            return cls.LAYER_TheChasm
        if region == cls.REGION_Enkanomiya:
            return cls.LAYER_Enkanomiya

        return cls.LAYER_Teyvat

    @classmethod
    def convert_GIMAP_to_LAYER(cls, points) -> str:
        """
        Get LAYER name from the position.
        If `points` contains multiple position, the first one will be used.
        """
        points = np.array(points)
        if points.ndim > 1:
            point = points
        else:
            point = points

        if point_in_area(point, area=(0, 0, 2389, 1730), threshold=0):
            return cls.LAYER_TheChasm
        if point_in_area(point, area=(0, 5731, 2391, 7944), threshold=0):
            return cls.LAYER_Enkanomiya

        return cls.LAYER_Teyvat

    @classmethod
    def convert_GIMAP_to_cvAutoTrack(cls, points) -> np.ndarray:
        """
        Formula from:
        https://github.com/GengGode/cvAutoTrack/blob/master/cvAutoTrack/src/AutoTrack.h

        cvAutoTrack is a kind of mess in Enkanomiya and The Chasm, so no converts
        """
        points = np.array(points)
        points = (points - (4480, 3015.5)) * 2.557
        return points

    @classmethod
    def convert_cvAutoTrack_to_GIMAP(cls, points, layer=LAYER_Teyvat) -> np.ndarray:
        points = np.array(points)
        points = points / 2.557 + (4480, 3015.5)
        return points

    @classmethod
    def convert_GIMAP_to_kongying(cls, points) -> np.ndarray:
        """
        kongying is not open-source, these are all magic numbers.
        Scaling factors are accurate while the offset are fitted.
        """
        points = np.array(points)
        layer = cls.convert_GIMAP_to_LAYER(points)
        if layer == cls.LAYER_Teyvat:
            points = cls.convert_GIMAP_to_cvAutoTrack(points)
            points = points * 0.66666667
            return points
        if layer == cls.LAYER_TheChasm:
            points = points * 5.114 + (-3561.4, -6275.4)
            return points
        if layer == cls.LAYER_Enkanomiya or layer == cls.LAYER_ThreeRealmsGatewayOffering:
            points = points * 5.114 + (-3561.4, -34614.4)
            return points

        return points

    @classmethod
    def convert_kongying_to_GIMAP(cls, points, layer=LAYER_Teyvat) -> np.ndarray:
        points = np.array(points)
        if layer == cls.LAYER_Teyvat:
            points = points / 0.66666667
            points = cls.convert_cvAutoTrack_to_GIMAP(points, layer)
            return points
        if layer == cls.LAYER_TheChasm:
            points = (points - (-3561.4, -6275.4)) / 5.114
            return points
        if layer == cls.LAYER_Enkanomiya or layer == cls.LAYER_ThreeRealmsGatewayOffering:
            points = (points - (-3561.4, -34614.4)) / 5.114
            return points

        return points
    
    @classmethod
    def convert_InGenshinMapPX_to_GIMAP(cls, points, layer=LAYER_Teyvat) -> np.ndarray:
        points = np.array(points)
        if IS_DEVICE_PC:
            points = points*0.81
    
        return points
    
    @classmethod
    def convert_GIMAP_to_InGenshinMapPX(cls, points, layer=LAYER_Teyvat) -> np.ndarray:
        points = np.array(points)
        if IS_DEVICE_PC:
            points = points/0.81
    
        return points
    
    # @classmethod
    # def convert_InGenshinMapPX_to_cvAutoTrack(cls, points, layer=LAYER_Teyvat) -> np.ndarray:
    #     points = np.array(points)
        
    #     points = cls.convert_InGenshinMapPX_to_GIMAP(points, layer=layer)
    #     points = cls.convert_GIMAP_to_cvAutoTrack(points)
        
    #     return points
    
    @classmethod
    def convert_cvAutoTrack_to_InGenshinMapPX(cls, points, layer=LAYER_Teyvat) -> np.ndarray:
        points = np.array(points)
        
        points = cls.convert_cvAutoTrack_to_GIMAP(points, layer=layer)
        points = cls.convert_GIMAP_to_InGenshinMapPX(points, layer=layer)
    
        return points

    @classmethod
    def convert_cvAutoTrack_to_kongying(cls, points, layer=LAYER_Teyvat) -> np.ndarray:
        points = np.array(points)
        
        if layer == cls.LAYER_Teyvat:
            points = points / 1.5
    
        return points
    
    @classmethod
    def convert_kongying_to_cvAutoTrack(cls, points, layer=LAYER_Teyvat) -> np.ndarray:
        points = np.array(points)
        
        if layer == cls.LAYER_Teyvat:
            points = points * 1.5
    
        return points

    # @classmethod
    # def convert_ANY_to_cvAutoTrack(cls,posi_obj:GenshinPosition) -> GenshinPosition:
    #     if isinstance(posi_obj, GIMAPPosition):
    #         return TianLiPosition(cls.convert_GIMAP_to_cvAutoTrack(posi_obj.position))
    #     elif isinstance(posi_obj, TianLiPosition):
    #         return posi_obj
    #     elif isinstance(posi_obj, KongYingPosition):
    #         return TianLiPosition(cls.convert_kongying_to_cvAutoTrack(posi_obj.position))
    #     elif isinstance(posi_obj, list):
    #         return TianLiPosition(posi_obj)
    #     elif isinstance(posi_obj, np.ndarray):
    #         return TianLiPosition(posi_obj)
    #     else:
    #         raise UnknownPositionTypeError
        
    # @classmethod
    # def convert_ANY_to_GIMAP(cls,posi_obj:GenshinPosition) -> GenshinPosition:
    #     if isinstance(posi_obj, GIMAPPosition):
    #         return posi_obj
    #     elif isinstance(posi_obj, TianLiPosition):
    #         return GIMAPPosition(cls.convert_cvAutoTrack_to_GIMAP(posi_obj.position))
    #     elif isinstance(posi_obj, KongYingPosition):
    #         return GIMAPPosition(cls.convert_kongying_to_GIMAP(posi_obj.position))
    #     elif isinstance(posi_obj, np.ndarray):
    #         return GIMAPPosition(posi_obj)
    #     elif isinstance(posi_obj, list):
    #         return GIMAPPosition(posi_obj)
    #     else:
    #         raise UnknownPositionTypeError
    
    # @classmethod
    # def convert_ANY_to_KongYing(cls,posi_obj:GenshinPosition) -> GenshinPosition:
    #     if isinstance(posi_obj, KongYingPosition):
    #         return posi_obj
    #     elif isinstance(posi_obj, TianLiPosition):
    #         return KongYingPosition(cls.convert_cvAutoTrack_to_kongying(posi_obj.position))
    #     elif isinstance(posi_obj, GIMAPPosition):
    #         return KongYingPosition(cls.convert_GIMAP_to_kongying(posi_obj.position))
    #     elif isinstance(posi_obj, np.ndarray):
    #         return KongYingPosition(posi_obj)
    #     elif isinstance(posi_obj, list):
    #         return KongYingPosition(posi_obj)
    #     else:
    #         raise UnknownPositionTypeError