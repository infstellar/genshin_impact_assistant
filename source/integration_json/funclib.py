import logger
from source.integration_json.utils import *
from source.integration_json import JIApi
from source.map.extractor.convert import MapConverter

def correction_collection_position(pos:list, name:str=''):
    """

    Args:
        pos: Tianli format
        name: the name of collection

    Returns:
        corrected position, Tianli format.

    magic number: offset.

    """
    possible_list = []
    if name != '':
        possible_list = JIApi.data[name]
    else:
        for i in JIApi.values():
            for j in i:
                possible_list.append(j)
    possible_pos = []
    for i in possible_list:
        i: PositionJson
        possible_pos.append(MapConverter.convert_GenshinMap_to_cvAutoTrack(i.position))
    logger.debug(f'{len(possible_pos)}')
    offset = 10
    ed_list = quick_euclidean_distance_plist(pos, possible_pos)
    if min(ed_list) < offset:
        rp = possible_pos[np.argmin(ed_list)]
        logger.info(f"position correct succ: {pos} -> {rp}; name:{name}")
        return rp
    else:
        logger.info(f"position correct fail: {pos}; name:{name}")
        return pos


