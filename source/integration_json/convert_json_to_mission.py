from source.mission.template.mission_just_collect import MissionJustCollectMoveStraight
from source.integration_json.utils import *
from source.map.extractor.convert import MapConverter
def convert_collect_json(j:PositionJson):
    pos = [j.position[0],j.position[2]]
    pos = MapConverter.convert_GenshinMap_to_cvAutoTrack(pos)
    pos = list(pos)
    return MissionJustCollectMoveStraight(pos, name=f"IntegrateJson-{j.name}")