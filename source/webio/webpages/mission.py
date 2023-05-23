from source.webio.util import *
from pywebio import *
from source.webio.advance_page import AdvancePage
from source.config.cvars import *
import threading

try:
    from missions.mission_index import MISSION_INDEX
    logger.debug(f"load custom mission index succ")
except:
    from source.mission.mission_index import MISSION_INDEX
try:
    from missions.mission_meta import MISSION_META
    logger.debug(f"load custom mission meta succ")
except:
    from source.mission.mission_meta import MISSION_META
from source.mission.index_generator import generate_mission_index

class MissionPage(AdvancePage):
    NAME_PROCESSBAR_MissionRebuild = 'PROCESSBAR_MissionRebuild'
    def __init__(self) -> None:
        super().__init__()
        self.missions = MISSION_INDEX
        self._create_default_settings()
        self.process_i = 1
        self.process_flag = False
    
    def _create_default_settings(self):
        j = load_json('mission_settings.json', f"{CONFIG_PATH}\\mission", auto_create=True)
        if j == {}: j = []
        save_json(j, 'mission_settings.json', f"{CONFIG_PATH}\\mission")
        j = load_json('mission_group.json', f"{CONFIG_PATH}\\mission", auto_create=True)
        if j == {}: j = []
        save_json(j, 'mission_group.json', f"{CONFIG_PATH}\\mission")
    
    def _render_scopes(self):
        j = load_json('mission_settings.json', f"{CONFIG_PATH}\\mission")
        for mission_name in self.missions:
            output.clear(mission_name)
            mauthor = None
            mnote = None
            mtime = None
            if mission_name in MISSION_META:
                if GLOBAL_LANG in MISSION_META[mission_name]['name']:
                    mission_show_name = MISSION_META[mission_name]['name'][GLOBAL_LANG]
                else:
                    mission_show_name = mission_name
                if 'author' in MISSION_META[mission_name]:
                    mauthor = MISSION_META[mission_name]['author']
                if 'note' in MISSION_META[mission_name]:
                    mnote = MISSION_META[mission_name]['note']
                if 'time' in MISSION_META[mission_name]:
                    mtime = MISSION_META[mission_name]['time']
                
                
            else:
                mission_show_name = mission_name
            output.put_text(mission_show_name, scope=mission_name)
            pv = 999
            ebd = False
            for iii in j:
                if iii['filename'] == mission_name:
                    if 'priority' in iii:
                        pv = iii['priority']
                    if 'enabled' in iii:
                        ebd = iii['enabled']
            if ebd:ebd=['enabled']
            pin.put_checkbox(name=f"CHECKBOX_{mission_name}",options=[{'label':t2t('Enable'),'value':'enabled'}],scope=mission_name,value=ebd)
            pin.put_input(name=f"PRIORITY_{mission_name}",label=t2t("Priority"),scope=mission_name,type=input.NUMBER,value=pv)
            if mauthor!=None:
                output.put_text(t2t('Author: ')+mauthor, scope=mission_name)
            if mnote!=None:
                output.put_text(t2t('Note: ')+mnote, scope=mission_name)
            if mtime!=None:
                output.put_text(t2t('Time: ')+mtime, scope=mission_name)

    
    def _get_all_mission_info(self):
        mission_info = []
        for i in self.missions:
            is_enable = pin.pin[f'CHECKBOX_{i}']
            if is_enable == []:
                is_enable = False
            else:
                is_enable = True
            mission_info.append(
                {
                    'filename':i,
                    'priority':pin.pin[f'PRIORITY_{i}'],
                    'enabled':is_enable
                }
            )
            
        return mission_info
    
    def _onclick_rebuild_missions(self):
        output.put_processbar(name=self.NAME_PROCESSBAR_MissionRebuild,label=t2t('Rebuild Progress'), auto_close=False, scope='SCOPE_PROCESSBAR')
        t = threading.Thread(target = generate_mission_index)
        t.start()
        for i in range(1,400-1):
            time.sleep(0.1)
            output.set_processbar(self.NAME_PROCESSBAR_MissionRebuild, i/400)
            if not t.is_alive():
                break
        for i in range(60):
            if not t.is_alive():
                break
            time.sleep(1)
        if t.is_alive():
            output.set_processbar(self.NAME_PROCESSBAR_MissionRebuild, 0)
            output.popup(t2t("Compile Fail, please see the console and ask for help."))
        else:
            output.set_processbar(self.NAME_PROCESSBAR_MissionRebuild, 1)
            output.popup(t2t("Compile success, please restart GIA program."))

    def _onclick_add_missions(self):
        pass
    
    def _onclick_save_missions(self):
        mission_info = self._get_all_mission_info()
        def sort_by_priority(x):
            return x['priority']
        mission_info = sorted(mission_info, key=sort_by_priority)
        save_json(mission_info, json_name='mission_settings.json', default_path=fr'{CONFIG_PATH}/mission')
        save_json([i['filename'] for i in mission_info if i['enabled']], json_name='mission_group.json', default_path=fr'{CONFIG_PATH}/mission')
        toast_succ()
    
    def _load(self):
        # put buttons
        output.put_row([output.put_button(label=t2t('Compile Missions'), onclick=self._onclick_rebuild_missions),
                        # output.put_button(label=t2t('Add Mission'), onclick=self._onclick_add_missions),
                        output.put_button(label=t2t('Save Changes'), onclick=self._onclick_save_missions)],scope=self.main_scope)
        output.put_text(t2t('If no mission is displayed here or if you have modified any mission in the missions folder, click on the Compile Missions button.'),scope=self.main_scope)
        output.put_text(t2t('The order of execution decreases from smallest to largest, with 0 being the highest priority.'),scope=self.main_scope)
        output.put_scope(name='SCOPE_PROCESSBAR',scope=self.main_scope)
        
        # put missions grid
        grid_content = []
        for i in range(len(self.missions)):
            if i%3==0:
                grid_content.append([])
            grid_content[i//3].append(output.put_scope(f"{self.missions[i]}").style('border: 1px solid #ccc; border-radius: 16px'))
        output.put_grid(content=grid_content, scope=self.main_scope)
        
        self._render_scopes()
    
    def _event_thread(self):
        time.sleep(0.1)

        