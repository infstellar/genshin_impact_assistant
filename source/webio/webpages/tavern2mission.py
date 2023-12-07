import functools
from source.webio.util import *
from pywebio import *
from source.webio.advance_page import AdvancePage
from source.config.cvars import *
from source.map.extractor.convert import MapConverter
from source.funclib import collector_lib


class Tavern2Mission(AdvancePage):
    
    FILE_UPLOAD_ROUTE = AN()
    
    INPUT_COLLECTION_NAME = AN()
    INPUT_MISSION_NAME = AN()
    INPUT_AUTHOR=AN()
    INPUT_DESCRIPTION=AN()
    INPUT_NOTE=AN()
    
    SCOPE_POSSIBLE_ROUTE = AN()
    
    BUTTON_GENERATE = AN()
    BUTTON_UPLOAD_FILE = t2t('Analyze curve')
    
    def __init__(self) -> None:
        super().__init__()
        self.file_last_modify_time = 0
        self.route_dict = {}
    
    def _load(self):
        with output.use_scope(self.main_scope):
            pin.put_file_upload(self.FILE_UPLOAD_ROUTE, label=t2t('upload route json file'), accept='.json')
            output.put_button(self.BUTTON_UPLOAD_FILE, onclick=self._upload_file)
            # output.put_button('load file', onclick=self._)
            output.put_scope(self.SCOPE_POSSIBLE_ROUTE)
            pin.put_input(self.INPUT_COLLECTION_NAME, help_text=t2t('input collection name'))
            output.put_scope(name="PREDICT_AND_VERIFY_01_scope", content=[
                    output.put_text("")
                ])
            pin.pin_on_change(self.INPUT_COLLECTION_NAME, onchange=self._onchange_collection_name, clear=False, init_run=True)
            pin.put_input(self.INPUT_MISSION_NAME, help_text=t2t('input mission name'))
            pin.put_input(self.INPUT_AUTHOR, help_text=t2t('input author'))
            pin.put_input(self.INPUT_DESCRIPTION, help_text=t2t('input description'))
            pin.put_input(self.INPUT_NOTE, help_text=t2t('input note'))
            # output.put_button(self.BUTTON_GENERATE, onclick=self._generate_mission)
    
    def _summarize_collection(self, plist):
        rdict = {}
        ITA = collector_lib.load_all_dict()
        for p in plist:
            tl_p = MapConverter.convert_kongying_curve_to_cvAutoTrack(p)
            features_list = collector_lib.predict_feature_by_position(tl_p, ITA)
            rlist = []
            for i in features_list:
                rlist.append(i['markerTitle'])
            rset = set(rlist)
            for i in rset:
                if i in rdict.keys():
                    rdict[i] += rlist.count(i)
                else:
                    rdict[i] = rlist.count(i)
        names = sorted(rdict, reverse=True)
        r = {}
        for i in names:
            r[i]=rdict[i]
        return r
    
    
    
    def _render_POSSIBLE_ROUTE(self):
        output.clear(self.SCOPE_POSSIBLE_ROUTE)
        with output.use_scope(self.SCOPE_POSSIBLE_ROUTE):
            name = f"{self.route_dict['curveName']}"
            buttons = []
            for curve in self.route_dict['curve_list']:
                lineName = f"{t2t('From')} {curve['lineName']} {t2t('to generate `collect` mission')}"
                buttons.append([lineName, curve['curve_poi']])
                curve_poi = curve['curve_poi']
            
            for i in buttons:
                ky_posi = []
                for pii in range(len(curve_poi)):
                    if self.is_real_index(pii):
                          ky_posi.append([curve_poi[pii]['x'], curve_poi[pii]['y']])
                d = self._summarize_collection(ky_posi)
                output.put_text(f"{t2t('Collections along the way: ')} {d}")
                output.put_button(i[0], onclick=functools.partial(self._generate_mission, i[1]))
                
                # output.put_buttons(buttons=[i[0] for i in buttons], onclick=[functools.partial(self._generate_mission, i[1]) for i in buttons])
    
    def is_real_index(self, i):
            # if i==0:return True
            # if i==1:return False
            # if i==2:return True
            # if i==3:return False
            # if i==4:return False
            # if i==5:return False
            # if i==6:return True
            # if i==7:return False
            # if i==8:return False
            # if i==9:return False
            # if i==10:return True
            # if i==11:return False
            return (i==0 or (i-2)%4==0)
    
    def _generate_mission(self, curve_poi:list):
        
        if pin.pin[self.INPUT_MISSION_NAME] == '' or pin.pin[self.INPUT_COLLECTION_NAME] == '' or pin.pin[self.INPUT_AUTHOR] == '':
            output.toast(t2t('mission name or collection name or author is/are empty, please check it.'), color='error')
            return
        
        tianli_posi_list = []
        # 1 2- 2 2+ 3- 3 3+ 4- 4 4+ 5- 5 5+
        # typesss = ['true', 'control', 'unknow'], 0,1,2
        for i in range(len(curve_poi)):
            if self.is_real_index(i):
                ky_posi = curve_poi[i]['x'], curve_poi[i]['y']
                tianli_posi_list.append(list(MapConverter.convert_kongying_curve_to_cvAutoTrack(ky_posi, decimal=2)))
        if DEBUG_MODE:
            print(len(tianli_posi_list))
            print(tianli_posi_list)
        
        verify_path(fr'{ROOT_PATH}/local_edit_missions')
        path = fr'{ROOT_PATH}/local_edit_missions/{pin.pin[self.INPUT_MISSION_NAME]}.py'
        position_list = []
        i=0
        for p in tianli_posi_list:
            position_list.append(
                {
      "id": i+1,
      "motion": "ANY",
      "position": tianli_posi_list[i],
      "special_key": None
    }
            )
            i+=1
        adsorptive_position=[]
        pickup_points=[]
        
        ita = collector_lib.load_items_position(pin.pin[self.INPUT_COLLECTION_NAME], ret_mode=2)
        for p in tianli_posi_list:
            rita = collector_lib.predict_feature_by_position(p, ita)
            if len(rita) > 0:
                for i in rita:
                    adsorptive_position.append(list(MapConverter.convert_kongying_to_cvAutoTrack(np.array( list(map(float,i["position"].split(',')))), decimal=2)))
                pickup_points.append(tianli_posi_list.index(p))
                
        META={
            'name':f'{pin.pin[self.INPUT_MISSION_NAME]}',
            'author':f"{pin.pin[self.INPUT_AUTHOR]}",
            'tags':["采集"],
            'local_edit_mission':f'{pin.pin[self.INPUT_MISSION_NAME]}',
            'description':f'{pin.pin[self.INPUT_DESCRIPTION]}',
            'note':f'{pin.pin[self.INPUT_NOTE]}'
        }       
        
        with open(path, 'w', encoding='utf-8') as f:
            tlpp_path = {
                "start_position": tianli_posi_list[0],
                "end_position": tianli_posi_list[-1],
                "position_list":position_list,
                "break_position": tianli_posi_list,
                "time": "",
                "additional_info":{
                    "kyt2m_version":"1.0",
                    "pickup_points":pickup_points
                    
                },
                "adsorptive_position":adsorptive_position
            }
            s = \
f'''from source.mission.template.mission_just_collect import MissionJustCollect

META={META}

class MissionMain(MissionJustCollect):
    def __init__(self):
        super().__init__(kyt2m_default_value, "kyt2m_default_name")

if __name__ == '__main__':
    mission = MissionMain()
    mission.start()

kyt2m_default_value = {str(tlpp_path)}
'''

            f.write(s)
        
        # verify_path(fr"{ROOT_PATH}/config/mission")
        local_meta = load_json('local_edit_mission_meta.json', fr"{ROOT_PATH}/config/mission",auto_create=True)
        JSON_META = META
        JSON_META['title'] = META['name']
        local_meta.update({pin.pin[self.INPUT_MISSION_NAME]:JSON_META})
        save_json(local_meta,'local_edit_mission_meta.json', fr"{ROOT_PATH}/config/mission")
        output.toast(t2t('mission has saved to ')+f'{path}')
    def _upload_file(self):
        if pin.pin[self.FILE_UPLOAD_ROUTE] is not None:
            output.toast(t2t('Analyzing curve, please waiting'), duration=6)
            self.route_dict = eval(pin.pin[self.FILE_UPLOAD_ROUTE]['content'])
            self.file_last_modify_time = pin.pin[self.FILE_UPLOAD_ROUTE]['last_modified']
            self._render_POSSIBLE_ROUTE()
            output.toast(t2t('Successfly analyzed curve'), duration=4, color='success')
    
    def _event_thread(self):
        if self.loaded:
            while 1:
                time.sleep(0.1)
    
    collection_names = load_json("ITEM_NAME.json", f"assets\\POI_JSON_API\\{GLOBAL_LANG}")         
    def _onchange_collection_name(self, x):
        if x == '':
            output.clear("PREDICT_AND_VERIFY_01_scope")
            output.put_text(t2t("Waiting..."), scope="PREDICT_AND_VERIFY_01_scope").style(f'color: black; font_size: 20px')
            return
        if x in self.collection_names:
            output.clear("PREDICT_AND_VERIFY_01_scope")
            output.put_text(t2t("Verified!"), scope="PREDICT_AND_VERIFY_01_scope").style(f'color: green; font_size: 20px')
            return
        else:
            f1 = False
            sl = []
            for i in self.collection_names:
                if x in i:
                    f1 = True
                    output.clear("PREDICT_AND_VERIFY_01_scope")
                    output.put_text(t2t("Waiting..."), scope="PREDICT_AND_VERIFY_01_scope").style(f'color: black; font_size: 20px')
                    if len(sl)<=15:
                        sl.append(i)
            
        if f1:
            output.put_text(t2t("You may want to enter: "), scope="PREDICT_AND_VERIFY_01_scope").style(f'color: black; font_size: 20px')
            for i in sl:
                output.put_text(i, scope="PREDICT_AND_VERIFY_01_scope").style(f'color: black; font_size: 12px; font-style:italic')
        else:
            output.clear("PREDICT_AND_VERIFY_01_scope")
            output.put_text(t2t("Not a valid name"), scope="PREDICT_AND_VERIFY_01_scope").style(f'color: red; font_size: 20px')