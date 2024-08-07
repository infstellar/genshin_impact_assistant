import datetime
import functools
import time

import cv2
import numpy as np
import pytz

from source.webio.util import *
from pywebio import *
from source.webio.advance_page import AdvancePage
from source.config.cvars import *
from source.map.extractor.convert import MapConverter
from source.funclib import collector_lib
from source.tavern import convert_tavern_curve_to_cvat
from source.tavern import convert_cvat_to_tavern_curve
from source.map.detection.resource import MiniMapResource
from source.map.extractor.convert import MapConverter

class TLPath2Mission(AdvancePage):
    FILE_UPLOAD_ROUTE = AN()
    FILE_UPLOAD_TAVERN = AN()
    FILE_UPLOAD_MISSION = AN()

    INPUT_COLLECTION_NAME = AN()
    INPUT_MISSION_NAME = AN()
    INPUT_AUTHOR = AN()
    INPUT_DESCRIPTION = AN()
    INPUT_NOTE = AN()
    INPUT_MISSION_FILE_NAME = AN()
    INPUT_OPTIMIZE_THRESHOLD = AN()

    CHECKBOX_ADDITIONAL_INFO = AN()

    SCOPE_SUPER_INFO = AN()

    SCOPE_POSSIBLE_ROUTE = AN()
    SCOPE_MISSION_INFO = AN()
    SCOPE_TLPP_INFO = AN()
    SCOPE_KYT_INFO = AN()

    TEXT_CURRENT_COLLECT_MODE = AN()

    BUTTON_GENERATE = AN()
    BUTTON_UPLOAD_FILE = t2t('Generate Mission')
    BUTTON_OPTIMIZE_PATH = AN()

    def __init__(self) -> None:
        super().__init__(
            document_link='https://genshinimpactassistant.github.io/GIA-Document/#/convert_tavern_route_to_mission')
        self.file_last_modify_time = 0
        self.route_dict = None
        self.tavern_dict = None
        self.tavern_positions = None
        self.python_mission_str = None
        self.python_mission_tlpp_contents = None
        self.gimap = MiniMapResource().RAWGIMAP

    def __draw_img(self, breaks, ads:t.List = None):
        """

        :param breaks: GIMAP format
        :return: cv Mat
        """
        areas_x, areas_y = [], []
        for i in breaks:
            areas_x.append(i[0])
            areas_y.append(i[1])
        OFFSET = 20
        area = [min(areas_x) - OFFSET, min(areas_y) - OFFSET, max(areas_x) + OFFSET, max(areas_y) + OFFSET]
        pos_leftup = np.array([area[0], area[1]])
        img = crop(self.gimap, area)
        last_pos = None
        RESIZE_RATE = 6
        def preprocess(i: np.ndarray):
            i -= pos_leftup
            i = i.astype('int')
            i = i.tolist()
            i: list
            return i

        if ads is not None:
            for i in ads:
                i = preprocess(i)
                cv2.circle(img, center=i, radius=2, color=(0, 0, 255), thickness=4)

        for i in breaks:
            i = preprocess(i)
            cv2.circle(img, center=i, radius=2, color=(255, 0, 0), thickness=1)
            if last_pos is not None:
                cv2.line(img, last_pos, i, (255, 255, 255), 1)
            last_pos = i.copy()



        img = cv2.resize(img, (0, 0), None, RESIZE_RATE, RESIZE_RATE)
        return img

    def _render_info(self):
        self._render_pymission_info()
        self._render_tavern_info()
        self._render_tlpp_info()


    def _calculate_distance(self, breaks):
        dist = 0
        last_i = breaks[0]
        for i in breaks:
            dist += euclidean_distance(last_i, i)
            last_i = i
        return round(dist,2)

    def _render_tlpp_info(self):
        output.clear(self.SCOPE_TLPP_INFO)
        with output.use_scope(self.SCOPE_TLPP_INFO):
            if self.route_dict is None:
                output.put_markdown('## '+t2t('TLPP Path is empty'))
                if self.tavern_positions is not None:
                    img = self.__draw_img([MapConverter.convert_cvAutoTrack_to_GIMAP(i) for i in self.tavern_positions])
                    img = np.ones_like(img)*255
                    output.put_image(Image.fromarray(img).convert('RGB'), title='preview')
                return
            output.put_markdown('# ' + t2t('TLPP Path'))
            output.put_row([
                output.put_button(t2t("Optimize Path"), onclick=self._onclick_optimize_path),
                output.put_button(t2t("Export as tavern curve and edit in tavern"), onclick=self._onclick_export_kyt),
                output.put_button(t2t("Generate Mission"), onclick=self._onclick_generate_mission),
            ], size='auto')

            breaks = self.route_dict["break_position"]
            output.put_markdown('### ' + t2t('Break Position num: ')+f'{len(breaks)}')
            output.put_markdown('### ' + t2t('Path Length: ') + f'{self._calculate_distance(breaks)}m')
            img = self.__draw_img([MapConverter.convert_cvAutoTrack_to_GIMAP(i) for i in breaks],
                              ads=[MapConverter.convert_cvAutoTrack_to_GIMAP(i) for i in self.route_dict['adsorptive_position']])
            output.put_image(Image.fromarray(img).convert('RGB'), title='preview')

            if 'manually_modified' not in self.route_dict['additional_info'].keys():
                self.route_dict['additional_info']['manually_modified'] = "true"
                logger.info('route has been marked as manually modified.')

    def _render_tavern_info(self):
        output.clear(self.SCOPE_KYT_INFO)
        with output.use_scope(self.SCOPE_KYT_INFO):
            if self.tavern_positions is None:
                output.put_markdown('### ' + t2t('Tavern Curve is empty'))
                return
            breaks = self.tavern_positions
            output.put_markdown('# ' + t2t('Tavern Curve'))
            output.put_row([
                output.put_button(t2t("Convert tavern curve to TLPP Path"),
                                  onclick=self._onclick_generate_tlpp_from_tavern),
                output.put_button(t2t("Use tavern curve to correct TLPP Path"),
                                  onclick=self._onclick_use_tavern_curve_to_correct_tlpp),
            ], size='auto')
            output.put_markdown('### ' + t2t('Control Points num: ')+f'{len(breaks)}')
            output.put_markdown('### ' + t2t('Path Length: ') + f'{self._calculate_distance(breaks)}m')
            img = self.__draw_img([MapConverter.convert_cvAutoTrack_to_GIMAP(i) for i in breaks])
            output.put_image(Image.fromarray(img).convert('RGB'), title='preview')

    def _render_pymission_info(self):
        output.clear(self.SCOPE_MISSION_INFO)
        with output.use_scope(self.SCOPE_MISSION_INFO):
            if self.python_mission_tlpp_contents is None:
                # output.put_markdown('### ' + t2t('Tavern Curve is empty'))
                return
            output.put_markdown('# ' + t2t('Python Mission TLPP Vars: '))
            output.put_button(t2t("Save Mission"), onclick=self._save_python_mission)
            for i in self.python_mission_tlpp_contents.keys():
                output.put_markdown('## ' + t2t('Mission TLPP Variable: ') + f"{i}")
                breaks = self.python_mission_tlpp_contents[i]['break_position']
                output.put_markdown('### ' + t2t('Control Points num: ') + f'{len(breaks)}')
                output.put_markdown('### ' + t2t('Path Length: ') + f'{self._calculate_distance(breaks)}m')
                img = self.__draw_img([MapConverter.convert_cvAutoTrack_to_GIMAP(i) for i in breaks])
                output.put_image(Image.fromarray(img).convert('RGB'), title='preview')
                output.put_button(t2t("Edit ") + f"{i} ", onclick=functools.partial(self._edit_specific_pymission_tlpp_variable, i))
                output.put_button(t2t("Save Current TLPP Path to variable ") + f"{i} ", onclick=functools.partial(self._save_current_tlpp_path_in_python_mission, i))

    def _edit_specific_pymission_tlpp_variable(self, var_name:str):
        self.route_dict = self.python_mission_tlpp_contents[var_name]
        self._render_info()

    def _save_pymission_tlpp_variable(self, var_name:str):
        self.python_mission_tlpp_contents[var_name] = self.route_dict
        self._render_info()

    def _save_python_mission(self):
        filename = "Edited_Mission " + datetime.datetime.now(pytz.timezone('Etc/GMT-8')).strftime("%Y%m%d-%H-%M-%S") + ".py"
        output.download(filename, self.python_mission_str.encode('utf-8'))

    @logger.catch
    def _save_current_tlpp_path_in_python_mission(self, var_name:str):
        for l in self.python_mission_str.split('\n'):
            if var_name in l and '=' in l and 'break_position' in l:
                rep_str = f"{var_name} = {self.route_dict}"
                self.python_mission_str = self.python_mission_str.replace(l, rep_str)
                break
        self.python_mission_tlpp_contents[var_name] = self.route_dict
        self._render_info()


    def _load(self):
        with output.use_scope(self.main_scope):
            pin.put_file_upload(self.FILE_UPLOAD_ROUTE, label=t2t('upload route json file'), accept='.json')
            pin.put_file_upload(self.FILE_UPLOAD_TAVERN, label=t2t('upload tavern curve json file'), accept='.json')
            pin.put_file_upload(self.FILE_UPLOAD_MISSION, label=t2t('Upload Python Mission File'), accept='.py')
            output.put_row([
                output.put_button(t2t("Upload TLPP file"), onclick=self._upload_file),
                output.put_button(t2t("Upload kongying tavern curve"), onclick=self._onclick_import_kyt),
                output.put_button(t2t("Upload Python Mission File"), onclick=self._onclick_upload_pymission),
            ], size='auto')

            output.put_scope(self.SCOPE_MISSION_INFO),
            output.put_scope(self.SCOPE_KYT_INFO),
            output.put_scope(self.SCOPE_TLPP_INFO),

            output.put_markdown("### " + t2t('Current Collect Mode: ') + f"{t2t(GIAconfig.Dev_RecordPath_CollectionType)}\n" + t2t('You can modify it at ConfigSettingPage->DevSettings'))
            # output.put_button('load file', onclick=self._)
            output.put_scope(self.SCOPE_POSSIBLE_ROUTE)
            pin.put_input(self.INPUT_COLLECTION_NAME, help_text=t2t('input collection name'))
            output.put_scope(name="PREDICT_AND_VERIFY_01_scope", content=[
                output.put_text("")
            ])
            pin.pin_on_change(self.INPUT_COLLECTION_NAME, onchange=self._onchange_collection_name, clear=False,
                              init_run=True)
            pin.put_input(self.INPUT_MISSION_FILE_NAME, help_text=t2t(
                'input mission file name, it should be `AuthorName`_`MissionName`_`id(1,2,3,etc.)` '))
            pin.put_input(self.INPUT_MISSION_NAME, help_text=t2t('input mission name'))
            pin.put_input(self.INPUT_AUTHOR, help_text=t2t('input author'))
            pin.put_input(self.INPUT_DESCRIPTION, help_text=t2t('input description'))
            pin.put_input(self.INPUT_NOTE, help_text=t2t('input note'))
            pin.put_checkbox(self.CHECKBOX_ADDITIONAL_INFO, options=[
                {'label': t2t('is collection in cliff'), 'value': "is_cliff_collection"},
                {'label': t2t('whether active pickup in waypoints'), 'value': "is_active_pickup_in_bp"},
                {'label': t2t('whether disable adsorptive positions'), 'value': "is_disable_ads_points"},
                {'label': t2t('whether Nahida is needed'), 'value': "is_nahida_needed"},
            ])
            pin.put_input(self.INPUT_OPTIMIZE_THRESHOLD, help_text=t2t('input optimize threshold. default is 1. The larger the threshold, the stronger the optimization.'),value="1")
            # output.put_button(self.BUTTON_GENERATE, onclick=self._generate_mission)

    def _summarize_collection(self, plist):
        rdict = {}
        ITA = collector_lib.load_all_dict()
        for p in plist:
            tl_p = MapConverter.convert_kongying_curve_to_cvAutoTrack(p)
            features_list = collector_lib.predict_feature_by_position(tl_p, ITA, threshold=35)
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
            r[i] = rdict[i]
        return r

                # output.put_buttons(buttons=[i[0] for i in buttons], onclick=[functools.partial(self._generate_mission, i[1]) for i in buttons])

    def _generate_mission(self, tlpp_pos: list):

        if pin.pin[self.INPUT_MISSION_NAME] == '' or pin.pin[self.INPUT_COLLECTION_NAME] == '' or pin.pin[
            self.INPUT_AUTHOR] == '' or pin.pin[self.INPUT_MISSION_FILE_NAME] == '':
            output.toast(t2t('mission name or collection name or author is/are empty, please check it.'), color='error')
            return

        tianli_posi_list = [i['position'] for i in tlpp_pos['position_list']]
        # 1 2- 2 2+ 3- 3 3+ 4- 4 4+ 5- 5 5+
        # typesss = ['true', 'control', 'unknow'], 0,1,2
        # for i in range(len(curve_poi)):
        #     if self.is_real_index(i):
        #         ky_posi = curve_poi[i]['x'], curve_poi[i]['y']
        #         tianli_posi_list.append(list(MapConverter.convert_kongying_curve_to_cvAutoTrack(ky_posi, decimal=2)))
        if DEBUG_MODE:
            print(len(tianli_posi_list))
            print(tianli_posi_list)

        verify_path(fr'{ROOT_PATH}/local_edit_missions')
        path = fr'{ROOT_PATH}/local_edit_missions/{pin.pin[self.INPUT_MISSION_FILE_NAME]}.py'
        position_list = tlpp_pos['position_list']
        # i = 0
        # for p in tianli_posi_list:
        #     position_list.append(
        #         {
        #             "id": i + 1,
        #             "motion": "ANY",
        #             "position": tianli_posi_list[i],
        #             "special_key": None
        #         }
        #     )
        #     i += 1
        if len(tlpp_pos['adsorptive_position']) > 0:
            adsorptive_position = tlpp_pos['adsorptive_position']
        else:
            adsorptive_position = []
        # if len(tlpp_pos['additional_info']['pickup_points']) > 0:
        #     pickup_points = tlpp_pos['additional_info']['pickup_points']
        # else:
        #     pickup_points = []

        # ita = collector_lib.load_items_position(pin.pin[self.INPUT_COLLECTION_NAME], ret_mode=2)

        # for p in tianli_posi_list:
        #     rita = collector_lib.predict_feature_by_position(p, ita, threshold=15)
        #     if len(rita) > 0:
        #         for i in rita:
        #             if len(curve_poi['adsorptive_position']) == 0:
        #                 adsorptive_position.append(list(MapConverter.convert_kongying_to_cvAutoTrack(
        #                     np.array(list(map(float, i["position"].split(',')))), decimal=2)))
        #         if len(curve_poi['additional_info']['pickup_points']) == 0:
        #             # pickup_points.append(tianli_posi_list.index(p))
        #             pass

        # 修正空荧酒馆误差
        # tianli_posi_list[0][1]+=10

        note = f'{pin.pin[self.INPUT_NOTE]}'
        if 'is_nahida_needed' in pin.pin[self.CHECKBOX_ADDITIONAL_INFO]:
            note += '\n 必须需要纳西妲 Nahida must be needed'

        META = {
            'name': {
                GLOBAL_LANG: f'{pin.pin[self.INPUT_MISSION_NAME]}'
            },
            'author': f"{pin.pin[self.INPUT_AUTHOR]}",
            'tags': {
                'zh_CN': [{"Plant":"采集","Artifact":"圣遗物","Combat":"战斗"}[GIAconfig.Dev_RecordPath_CollectionType]],
                'en_US': [{"Plant":"Collect","Artifact":"Artifact","Combat":"Combat"}[GIAconfig.Dev_RecordPath_CollectionType]]
            },
            'local_edit_mission': f'{pin.pin[self.INPUT_MISSION_NAME]}',
            'description': f'{pin.pin[self.INPUT_DESCRIPTION]}',
            'note': note
        }

        additional_info = {
            "path_recorder": "1.0",
            "manually_modified":'true'
        }
        if 'is_cliff_collection' in pin.pin[self.CHECKBOX_ADDITIONAL_INFO]:
            additional_info['is_cliff_collection'] = True
        if 'is_disable_ads_points' in pin.pin[self.CHECKBOX_ADDITIONAL_INFO]:
            adsorptive_position = []
        if 'is_active_pickup_in_bp' in pin.pin[self.CHECKBOX_ADDITIONAL_INFO]:
            additional_info['is_active_pickup_in_bp'] = True
            adsorptive_position = tianli_posi_list[1:]
        if 'is_nahida_needed' in pin.pin[self.CHECKBOX_ADDITIONAL_INFO]:
            additional_info['is_nahida_needed'] = True

        bps = tlpp_pos["break_position"]

        with open(path, 'w', encoding='utf-8') as f:
            tlpp_path = {
                "start_position": bps[0],
                "end_position": bps[-1],
                "position_list": tlpp_pos["position_list"],
                "break_position": bps,
                "time": "",
                "additional_info": additional_info,
                "adsorptive_position": adsorptive_position,
                'generate_from': 'path recorder 1.0'

            }

            mission_import = {
                "Artifact":"from source.mission.template.mission_just_collect import MissionCollectArtifact",
                "Plant":"from source.mission.template.mission_just_collect import MissionJustCollect",
                "Combat":"from source.mission.template.mission_combat import MissionCombat"
            }[GIAconfig.Dev_RecordPath_CollectionType]

            s = \
f'''{mission_import}

tlp2m_default_value = {str(tlpp_path)}

META={META}

class MissionMain({mission_import.split(' ')[-1]}):
    def __init__(self):
        super().__init__(tlp2m_default_value, "tlp2m_default_name")

if __name__ == '__main__':
    mission = MissionMain()
    mission.start()

'''

            f.write(s)

        # verify_path(fr"{ROOT_PATH}/config/mission")
        local_meta = load_json('local_edit_mission_meta.json', fr"{ROOT_PATH}/config/mission", auto_create=True)
        JSON_META = META
        JSON_META['title'] = META['name']
        JSON_META['name'] = META['name'][GLOBAL_LANG]
        JSON_META['tags'] = META['tags'][GLOBAL_LANG]
        local_meta.update({pin.pin[self.INPUT_MISSION_FILE_NAME]: JSON_META})
        save_json(local_meta, 'local_edit_mission_meta.json', fr"{ROOT_PATH}/config/mission")
        output.toast(t2t('mission has saved to ') + f'{path}', duration=6)

    def _upload_file(self):
        if pin.pin[self.FILE_UPLOAD_ROUTE] is not None:
            self._load_dict()
            self._render_info()
            output.toast(t2t('Upload successfully'), duration=4, color='success')

    def _onclick_generate_mission(self):
        self._generate_mission(self.route_dict)

    def _event_thread(self):
        if self.loaded:
            while 1:
                time.sleep(0.1)

    collection_names = load_json("ITEM_NAME.json", f"assets\\POI_JSON_API\\{GLOBAL_LANG}")

    def _onchange_collection_name(self, x):
        if x == '':
            output.clear("PREDICT_AND_VERIFY_01_scope")
            output.put_text(t2t("Waiting..."), scope="PREDICT_AND_VERIFY_01_scope").style(
                f'color: black; font_size: 20px')
            return
        if x in self.collection_names:
            output.clear("PREDICT_AND_VERIFY_01_scope")
            output.put_text(t2t("Verified!"), scope="PREDICT_AND_VERIFY_01_scope").style(
                f'color: green; font_size: 20px')
            return
        else:
            f1 = False
            sl = []
            for i in self.collection_names:
                if x in i:
                    f1 = True
                    output.clear("PREDICT_AND_VERIFY_01_scope")
                    output.put_text(t2t("Waiting..."), scope="PREDICT_AND_VERIFY_01_scope").style(
                        f'color: black; font_size: 20px')
                    if len(sl) <= 15:
                        sl.append(i)

        if f1:
            output.put_text(t2t("You may want to enter: "), scope="PREDICT_AND_VERIFY_01_scope").style(
                f'color: black; font_size: 20px')
            for i in sl:
                output.put_text(i, scope="PREDICT_AND_VERIFY_01_scope").style(
                    f'color: black; font_size: 12px; font-style:italic')
        else:
            output.clear("PREDICT_AND_VERIFY_01_scope")
            output.put_text(t2t("Not a valid name"), scope="PREDICT_AND_VERIFY_01_scope").style(
                f'color: red; font_size: 20px')

    def _load_dict(self):
        if pin.pin[self.FILE_UPLOAD_ROUTE] is not None:
            self.route_dict = eval(pin.pin[self.FILE_UPLOAD_ROUTE]['content'].decode('utf-8').replace('null', '\"\"'))

    def _load_tavern_dict(self):
        if pin.pin[self.FILE_UPLOAD_TAVERN] is not None:
            self.tavern_dict = eval(pin.pin[self.FILE_UPLOAD_TAVERN]['content'].decode('utf-8').replace('null', '\"\"'))

    def _check_tavern_available(self):
        x = len(self.tavern_dict['curve_list'])
        if x==0:
            output.toast(t2t("no curve has been found in json file."), color="error", duration=4)
            return False
        elif x>1 :
            output.toast(t2t("more than 1 curve has been found in json file. Only the first curve will be used."), color="warning", duration=4)
            return True
        else:
            return True

    def _onclick_optimize_path(self):
        if self.route_dict is not None:
            output.toast(f'RDP optimizing')
            curr_breaks = self.route_dict['break_position']
            old_len = len(curr_breaks)
            from source.rdp import rdp
            curr_breaks = rdp(curr_breaks, epsilon=float(pin.pin[self.INPUT_OPTIMIZE_THRESHOLD]))
            output.toast(f'optimized: {old_len} -> {len(curr_breaks)}')
            self.route_dict['break_position'] = curr_breaks
            self._render_info()

    def _onclick_export_kyt(self):
        curr_breaks = self.route_dict['break_position']
        kyts = convert_cvat_to_tavern_curve(curr_breaks)
        date = datetime.datetime.now(pytz.timezone('Etc/GMT-8')).strftime("%Y%m%d-%H-%M-%S")
        default_path = f"{ROOT_PATH}\\dev_assets\\tavern_edit"
        verify_path(default_path)
        _ = t2t("GIA Export Curve")
        save_json(x=kyts, json_name=f"{_}-{date}.json", default_path=default_path)
        toast_succ(t2t("The kongying tavern curve has been saved to ") + f"{default_path}\\{_}-{date}.json", duration=10)

    def _onclick_import_kyt(self):
        if pin.pin[self.FILE_UPLOAD_TAVERN] is not None:
            output.toast(t2t("Uploading tavern curve"))
            self._load_tavern_dict()
            if not self._check_tavern_available():
                return
            self.tavern_positions = convert_tavern_curve_to_cvat(self.tavern_dict['curve_list'][0]['curve_poi'])
            self._render_info()
            toast_succ(f'Upload tavern file success')
            # if self.route_dict is not None:
            #     curr_breaks = self.route_dict['break_position']
            #     old_len = len(curr_breaks)
            #     self.route_dict['break_position'] = tl_pos
            #     toast_succ(f'Edit original path file success: Break Position: {old_len} -> {len(tl_pos)}')
            # else:
            #     self._generate_tlpp_from_tavern(self.tavern_dict['curve_list'][0]['curve_poi'])
            #     toast_succ(f'Import tavern file success')

    def _onclick_upload_pymission(self):
        if pin.pin[self.FILE_UPLOAD_MISSION] is not None:
            output.toast(t2t("Uploading pymission"))
            self.python_mission_str = pin.pin[self.FILE_UPLOAD_MISSION]['content'].decode('utf-8')
            self._analyse_py_mission(self.python_mission_str)
            self._render_info()
            toast_succ(f'Upload pymission success')

    def _onclick_generate_tlpp_from_tavern(self):
        if pin.pin[self.INPUT_COLLECTION_NAME] == '':
            output.toast(t2t('collection name is empty, please check it.'), color='error')
            return

        tianli_posi_list = self.tavern_positions
        # 1 2- 2 2+ 3- 3 3+ 4- 4 4+ 5- 5 5+
        # typesss = ['true', 'control', 'unknow'], 0,1,2
        if DEBUG_MODE:
            print(len(tianli_posi_list))
            print(tianli_posi_list)
        position_list = []
        i = 0
        for p in tianli_posi_list:
            position_list.append(
                {
                "id": i + 1,
                "motion": "ANY",
                    "position": tianli_posi_list[i],
                    "special_key": None
                }
            )
            i += 1
        adsorptive_position = []
        # pickup_points = []

        from source.integration_json.funclib import correction_collection_position
        for p in tianli_posi_list:
            possible_collection = collector_lib.predict_feature_by_pos_v2(p, pin.pin[self.INPUT_COLLECTION_NAME], threshold=15)
            if len(possible_collection) > 0:
                for i in possible_collection:
                    pos = collector_lib.conv_kongying_str_pos_to_cvat_pos(i.position)
                    pos = list(correction_collection_position(pos, name=pin.pin[self.INPUT_COLLECTION_NAME]))
                    if len(adsorptive_position)  == 0:
                        adsorptive_position.append(pos)
                    elif quick_euclidean_distance_plist(pos, adsorptive_position).min() > 2:
                        adsorptive_position.append(pos)
                # pickup_points.append(tianli_posi_list.index(p))

        additional_info = {
            "kyt2tlpp_version": "1.0"
        }
        tlpp_path = {
            "start_position": tianli_posi_list[0],
            "end_position": tianli_posi_list[-1],
            "position_list": position_list,
            "break_position": tianli_posi_list,
            "time": f"{time.time()}",
            "additional_info": additional_info,
            "adsorptive_position": adsorptive_position,
        }
        self.route_dict = tlpp_path
        self._render_info()
        toast_succ(t2t('Successfully convert KYT curve to TLPP. Please check.'))

    def _onclick_use_tavern_curve_to_correct_tlpp(self):
        if self.route_dict is not None and self.tavern_positions is not None:
            curr_breaks = self.route_dict['break_position']
            old_len = len(curr_breaks)
            self.route_dict['break_position'] = self.tavern_positions
            self._render_info()
            toast_succ(f'Edit original TLPP path file success: Break Position: {old_len} -> {len(self.tavern_positions)}')

    def _analyse_py_mission(self, python_mission_content_str):
        lines = python_mission_content_str.split('\n')
        possible_tlpps = {}
        for l in lines:
            if 'break_position' in l:
                var_name = l.split('=')[0].replace(' ', '')
                tlpp_content = l.split('=')[-1]
                possible_tlpps[var_name] = eval(tlpp_content)
        self.python_mission_tlpp_contents = possible_tlpps



