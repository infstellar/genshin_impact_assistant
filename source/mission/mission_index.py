"""This file is generated automatically. Do not manually modify it."""
MISSION_INDEX = ['MissionAutoCollector', 'MissionCrystalfly', 'MissionSakuraBloom1', 'MissionSweatFlower1', 'MissionTest', 'MissionTest2']
def get_mission_object(mission_name:str):
    if mission_name == 'MissionAutoCollector':
        import source.mission.missions.MissionAutoCollector
        return source.mission.missions.MissionAutoCollector.MissionAutoCollector()
    if mission_name == 'MissionCrystalfly':
        import source.mission.missions.MissionCrystalfly
        return source.mission.missions.MissionCrystalfly.MissionCrystalfly()
    if mission_name == 'MissionSakuraBloom1':
        import source.mission.missions.MissionSakuraBloom1
        return source.mission.missions.MissionSakuraBloom1.MissionSakuraBloom1()
    if mission_name == 'MissionSweatFlower1':
        import source.mission.missions.MissionSweatFlower1
        return source.mission.missions.MissionSweatFlower1.MissionSweatFlower1()
    if mission_name == 'MissionTest':
        import source.mission.missions.MissionTest
        return source.mission.missions.MissionTest.MissionTest()
    if mission_name == 'MissionTest2':
        import source.mission.missions.MissionTest2
        return source.mission.missions.MissionTest2.MissionTest2()
