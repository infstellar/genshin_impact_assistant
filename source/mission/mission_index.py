"""This file is generated automatically. Do not manually modify it."""
MISSION_INDEX = ['MissionAutoCollector', 'MissionCrystalfly', 'MissionQingXin1', 'MissionQingXin2', 'MissionSakuraBloom1', 'MissionSweatFlower1', 'MissionSweatFlower2', 'MissionTest', 'MissionTest2', 'MissionV2PTest', 'MissionVioletgrass1', 'MissionVioletgrass2', 'MissionVioletgrass3']
def get_mission_object(mission_name:str):
    if mission_name == 'MissionAutoCollector':
        import source.mission.missions.MissionAutoCollector
        return source.mission.missions.MissionAutoCollector.MissionAutoCollector()
    if mission_name == 'MissionCrystalfly':
        import source.mission.missions.MissionCrystalfly
        return source.mission.missions.MissionCrystalfly.MissionCrystalfly()
    if mission_name == 'MissionQingXin1':
        import source.mission.missions.MissionQingXin1
        return source.mission.missions.MissionQingXin1.MissionQingXin1()
    if mission_name == 'MissionQingXin2':
        import source.mission.missions.MissionQingXin2
        return source.mission.missions.MissionQingXin2.MissionQingXin2()
    if mission_name == 'MissionSakuraBloom1':
        import source.mission.missions.MissionSakuraBloom1
        return source.mission.missions.MissionSakuraBloom1.MissionSakuraBloom1()
    if mission_name == 'MissionSweatFlower1':
        import source.mission.missions.MissionSweatFlower1
        return source.mission.missions.MissionSweatFlower1.MissionSweatFlower1()
    if mission_name == 'MissionSweatFlower2':
        import source.mission.missions.MissionSweatFlower2
        return source.mission.missions.MissionSweatFlower2.MissionSweatFlower2()
    if mission_name == 'MissionTest':
        import source.mission.missions.MissionTest
        return source.mission.missions.MissionTest.MissionTest()
    if mission_name == 'MissionTest2':
        import source.mission.missions.MissionTest2
        return source.mission.missions.MissionTest2.MissionTest2()
    if mission_name == 'MissionV2PTest':
        import source.mission.missions.MissionV2PTest
        return source.mission.missions.MissionV2PTest.MissionV2PTest()
    if mission_name == 'MissionVioletgrass1':
        import source.mission.missions.MissionVioletgrass1
        return source.mission.missions.MissionVioletgrass1.MissionVioletgrass1()
    if mission_name == 'MissionVioletgrass2':
        import source.mission.missions.MissionVioletgrass2
        return source.mission.missions.MissionVioletgrass2.MissionVioletgrass2()
    if mission_name == 'MissionVioletgrass3':
        import source.mission.missions.MissionVioletgrass3
        return source.mission.missions.MissionVioletgrass3.MissionVioletgrass3()
