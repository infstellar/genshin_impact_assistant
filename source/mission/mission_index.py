"""This file is generated automatically. Do not manually modify it."""
MISSION_INDEX = ['MissionAutoCollector', 'MissionCecilia', 'MissionCrystalfly', 'MissionJueyunChili', 'MissionQingXin2', 'MissionSakuraBloom1', 'MissionSilkFlower', 'MissionSweatFlower1', 'MissionSweatFlower2', 'MissionVioletgrass1', 'MissionVioletgrass2', 'MissionVioletgrass3', 'MissionWindwhellAster', 'MissionGlazeLily', 'MissionQingXin1']
def get_mission_object(mission_name:str):
    if mission_name == 'MissionAutoCollector':
        import source.mission.missions.MissionAutoCollector
        return source.mission.missions.MissionAutoCollector.MissionMain()
    if mission_name == 'MissionCecilia':
        import source.mission.missions.MissionCecilia
        return source.mission.missions.MissionCecilia.MissionMain()
    if mission_name == 'MissionCrystalfly':
        import source.mission.missions.MissionCrystalfly
        return source.mission.missions.MissionCrystalfly.MissionMain()
    if mission_name == 'MissionJueyunChili':
        import source.mission.missions.MissionJueyunChili
        return source.mission.missions.MissionJueyunChili.MissionMain()
    if mission_name == 'MissionQingXin2':
        import source.mission.missions.MissionQingXin2
        return source.mission.missions.MissionQingXin2.MissionMain()
    if mission_name == 'MissionSakuraBloom1':
        import source.mission.missions.MissionSakuraBloom1
        return source.mission.missions.MissionSakuraBloom1.MissionMain()
    if mission_name == 'MissionSilkFlower':
        import source.mission.missions.MissionSilkFlower
        return source.mission.missions.MissionSilkFlower.MissionMain()
    if mission_name == 'MissionSweatFlower1':
        import source.mission.missions.MissionSweatFlower1
        return source.mission.missions.MissionSweatFlower1.MissionMain()
    if mission_name == 'MissionSweatFlower2':
        import source.mission.missions.MissionSweatFlower2
        return source.mission.missions.MissionSweatFlower2.MissionMain()
    if mission_name == 'MissionVioletgrass1':
        import source.mission.missions.MissionVioletgrass1
        return source.mission.missions.MissionVioletgrass1.MissionMain()
    if mission_name == 'MissionVioletgrass2':
        import source.mission.missions.MissionVioletgrass2
        return source.mission.missions.MissionVioletgrass2.MissionMain()
    if mission_name == 'MissionVioletgrass3':
        import source.mission.missions.MissionVioletgrass3
        return source.mission.missions.MissionVioletgrass3.MissionMain()
    if mission_name == 'MissionWindwhellAster':
        import source.mission.missions.MissionWindwhellAster
        return source.mission.missions.MissionWindwhellAster.MissionMain()
    if mission_name == 'MissionGlazeLily':
        import missions.MissionGlazeLily
        return missions.MissionGlazeLily.MissionMain()
    if mission_name == 'MissionQingXin1':
        import missions.MissionQingXin1
        return missions.MissionQingXin1.MissionMain()
