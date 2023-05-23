"""This file is generated automatically. Do not manually modify it."""
MISSION_INDEX = ['MissionAutoCollector', 'MissionCecilia', 'MissionCrystalfly', 'MissionJueyunChili', 'MissionQingXin2', 'MissionSakuraBloom1', 'MissionSilkFlower', 'MissionSweatFlower1', 'MissionSweatFlower2', 'MissionVioletgrass1', 'MissionVioletgrass2', 'MissionVioletgrass3', 'MissionWindwhellAster']
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
META = {}
if __name__ == '__main__':
    from source.funclib import combat_lib
    combat_lib.CSDL.stop_threading()
    import source.mission.missions.MissionAutoCollector
    META['MissionAutoCollector'] = source.mission.missions.MissionAutoCollector.META
    import source.mission.missions.MissionCecilia
    META['MissionCecilia'] = source.mission.missions.MissionCecilia.META
    import source.mission.missions.MissionCrystalfly
    META['MissionCrystalfly'] = source.mission.missions.MissionCrystalfly.META
    import source.mission.missions.MissionJueyunChili
    META['MissionJueyunChili'] = source.mission.missions.MissionJueyunChili.META
    import source.mission.missions.MissionQingXin2
    META['MissionQingXin2'] = source.mission.missions.MissionQingXin2.META
    import source.mission.missions.MissionSakuraBloom1
    META['MissionSakuraBloom1'] = source.mission.missions.MissionSakuraBloom1.META
    import source.mission.missions.MissionSilkFlower
    META['MissionSilkFlower'] = source.mission.missions.MissionSilkFlower.META
    import source.mission.missions.MissionSweatFlower1
    META['MissionSweatFlower1'] = source.mission.missions.MissionSweatFlower1.META
    import source.mission.missions.MissionSweatFlower2
    META['MissionSweatFlower2'] = source.mission.missions.MissionSweatFlower2.META
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
    import missions.MissionQingXin1
    META['MissionQingXin1'] = missions.MissionQingXin1.META
    with open(r'M:\ProgramData\GIA\genshin_impact_assistant\missions\mission_meta.py', 'w', encoding='utf-8') as f:
        f.write(f'MISSION_META = {str(META)}')
    print('index end')
