"""This file is generated automatically. Do not manually modify it."""
MISSION_INDEX = ['MissionCrystalfly', 'MissionTest', 'MissionTest2']
def get_mission_object(mission_name:str):
    if mission_name == 'MissionCrystalfly':
        import source.mission.missions.MissionCrystalfly
        return source.mission.missions.MissionCrystalfly.MissionCrystalfly()
    if mission_name == 'MissionTest':
        import source.mission.missions.MissionTest
        return source.mission.missions.MissionTest.MissionTest()
    if mission_name == 'MissionTest2':
        import source.mission.missions.MissionTest2
        return source.mission.missions.MissionTest2.MissionTest2()
