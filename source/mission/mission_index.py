"""This file is generated automatically. Do not manually modify it."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MISSION_INDEX = ['MissionAutoCollector', 'MissionCecilia', 'MissionCrystalfly', 'MissionJueyunChili', 'MissionQingXin1', 'MissionQingXin2', 'MissionSakuraBloom1', 'MissionSweatFlower1', 'MissionSweatFlower2', 'MissionTest', 'MissionTest2', 'MissionV2PTest', 'MissionVioletgrass1', 'MissionVioletgrass2', 'MissionVioletgrass3', 'MissionWindwhellAster']
def get_mission_object(mission_name:str):
    if mission_name == 'MissionAutoCollector':
        import source.mission.missions.MissionAutoCollector
        return source.mission.missions.MissionAutoCollector.MissionAutoCollector()
    if mission_name == 'MissionCecilia':
        import source.mission.missions.MissionCecilia
        return source.mission.missions.MissionCecilia.MissionCecilia()
    if mission_name == 'MissionCrystalfly':
        import source.mission.missions.MissionCrystalfly
        return source.mission.missions.MissionCrystalfly.MissionCrystalfly()
    if mission_name == 'MissionJueyunChili':
        import source.mission.missions.MissionJueyunChili
        return source.mission.missions.MissionJueyunChili.MissionJueyunChili()
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
    if mission_name == 'MissionWindwhellAster':
        import source.mission.missions.MissionWindwhellAster
        return source.mission.missions.MissionWindwhellAster.MissionWindwhellAster()
    if mission_name == 'MissionGlazeLily':
        import missions.MissionGlazeLily
        return missions.MissionGlazeLily.MissionGlazeLily()
META = {}
if __name__ == '__main__':
    import source.mission.missions.MissionAutoCollector
    META['MissionAutoCollector'] = source.mission.missions.MissionAutoCollector.META
    import source.mission.missions.MissionCecilia
    META['MissionCecilia'] = source.mission.missions.MissionCecilia.META
    import source.mission.missions.MissionCrystalfly
    META['MissionCrystalfly'] = source.mission.missions.MissionCrystalfly.META
    import source.mission.missions.MissionJueyunChili
    META['MissionJueyunChili'] = source.mission.missions.MissionJueyunChili.META
    import source.mission.missions.MissionQingXin1
    META['MissionQingXin1'] = source.mission.missions.MissionQingXin1.META
    import source.mission.missions.MissionQingXin2
    META['MissionQingXin2'] = source.mission.missions.MissionQingXin2.META
    import source.mission.missions.MissionSakuraBloom1
    META['MissionSakuraBloom1'] = source.mission.missions.MissionSakuraBloom1.META
    import source.mission.missions.MissionSweatFlower1
    META['MissionSweatFlower1'] = source.mission.missions.MissionSweatFlower1.META
    import source.mission.missions.MissionSweatFlower2
    META['MissionSweatFlower2'] = source.mission.missions.MissionSweatFlower2.META
    import source.mission.missions.MissionTest
    META['MissionTest'] = source.mission.missions.MissionTest.META
    import source.mission.missions.MissionTest2
    META['MissionTest2'] = source.mission.missions.MissionTest2.META
    import source.mission.missions.MissionV2PTest
    META['MissionV2PTest'] = source.mission.missions.MissionV2PTest.META
    import source.mission.missions.MissionVioletgrass1
    META['MissionVioletgrass1'] = source.mission.missions.MissionVioletgrass1.META
    import source.mission.missions.MissionVioletgrass2
    META['MissionVioletgrass2'] = source.mission.missions.MissionVioletgrass2.META
    import source.mission.missions.MissionVioletgrass3
    META['MissionVioletgrass3'] = source.mission.missions.MissionVioletgrass3.META
    import source.mission.missions.MissionWindwhellAster
    META['MissionWindwhellAster'] = source.mission.missions.MissionWindwhellAster.META
    import missions.MissionGlazeLily
    META['MissionGlazeLily'] = missions.MissionGlazeLily.META
    with open('M:\ProgramData\GIA\genshin_impact_assistant\source\mission\mission_meta.py', 'w', encoding='utf-8') as f:
        f.write(f'MISSION_META = {str(META)}')
    from source.funclib import combat_lib
    combat_lib.CSDL.stop_threading()
    print('index end')
