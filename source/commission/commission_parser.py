from source.map.map import genshin_map
from source.map.position.position import *
from source.ui.ui import ui_control
from source.ui import page as UIPages
from source.commission.util import *
from source.interaction.interaction_core import itt
from source.manager import asset
from source.commission.commission_index import COMMISSION_INDEX
from source.commission.commission_acquisition import get_commission_object
from source.api.pdocr_complete import ocr
from source.common.timer_module import FileTimer


class CommissionParser():
    TRAVERSE_MONDSTADT_POSITION=[TianLiPosition([783.450352, -6943.497652]),
                                 TianLiPosition([2489.331552, -6101.094052]),
                                 TianLiPosition([3101.988752, -6431.458452]),
                                 TianLiPosition([2860.607952, -5526.280452]),
                                 TianLiPosition([2289.885552, -5515.029652]),
                                 TianLiPosition([1698.707152, -5273.648852]),
                                 TianLiPosition([2224.426352, -4798.046852]),
                                 TianLiPosition([2156.921552, -3923.552852]),
                                 TianLiPosition([2423.872352, -3427.494852]),
                                 TianLiPosition([3367.916752, -4196.640452]),
                                 TianLiPosition([3328.027552, -5106.932452])]
    
    
    
    def __init__(self) -> None:
        self.commission_dicts = []

    def traverse_mondstant(self):
        self.commission_dicts = []
        commission_positions = []
        ui_control.ensure_page(UIPages.page_bigmap)
        genshin_map.get_bigmap_posi()
        genshin_map._switch_to_area("Mondstadt")
        for posi in self.TRAVERSE_MONDSTADT_POSITION:
            genshin_map.get_bigmap_posi()
            genshin_map._move_bigmap(posi.tianli, force_center = True)
            cap_posi = [220,240,1920-200,1080-150]
            img = itt.capture(jpgmode=0)
            img = crop(img, cap_posi)
            img = recorp(img,cap_posi)
            positions = itt.match_multiple_img(img, template=asset.IconBigmapCommission.image)
            if len(positions)>0:
                curr_posi = genshin_map.get_bigmap_posi()
                for i in positions:
                    target_px_posi = np.array(list(i))+np.array([8,8])
                    delta_posi = genshin_map.convert_InGenshinMapPX_to_GIMAP(target_px_posi-np.array([SCREEN_CENTER_X,SCREEN_CENTER_Y]))
                    target_gimap_posi = curr_posi.gimap + delta_posi
                    target_tianli_posi = GIMAPPosition(target_gimap_posi).tianli
                    
                    if len(commission_positions)>0:
                        if not min(euclidean_distance_plist(target_tianli_posi, commission_positions)) >= 60:
                            continue
                    commission_positions.append(target_tianli_posi)
                    
                    itt.move_and_click(list(i))
                    itt.delay("animation")
                    itt.delay("animation")
                    itt.delay("animation")
                    com_type = self._detect_commission_type()
                    itt.delay("animation")
                    itt.key_press('esc')
                    if com_type is None:
                        continue
                    else:
                        self.commission_dicts.append({
                            "type":com_type,
                            "position":list(target_tianli_posi),
                            "done":False
                        })
                        logger.info(f"commission has been added: {self.commission_dicts[-1]}")
        return self.commission_dicts
    
    def _set_and_save_and_load_commission_dicts(self) -> bool:
        g4t = FileTimer("daily_commission")
        if g4t.get_diff_time()>=3600:
            logger.info(f"new genshin day, traverse mondstant commissions")
            self.traverse_mondstant()
            save_json(self.commission_dicts, json_name="commission_dict.json", default_path=rf"{CONFIG_PATH}\commission")
            g4t.reset()
            return True
        else:
            self.commission_dicts = load_json(json_name="commission_dict.json", default_path=rf"{CONFIG_PATH}\commission")
            for i in self.commission_dicts:
                if i["done"] != True:
                    return False
            logger.info(f"commission dicts all have been done. researching.")
            self.traverse_mondstant()
            save_json(self.commission_dicts, json_name="commission_dict.json", default_path=rf"{CONFIG_PATH}\commission")
            return True
    def _detect_commission_type(self)->str:
        img = itt.capture(jpgmode=0)
        img_choose = crop(img.copy(), asset.AreaBigmapChoose.position)
        img_sidebar = crop(img.copy(), asset.AreaBigmapSidebarCommissionName.position)
        
        if itt.get_img_existence(asset.IconBigmapSidebarIsCommissionExist, cap = img_sidebar):
            ocr_res = ocr.get_all_texts(img_sidebar)
        else:
            ocr_res = ocr.get_all_texts(img_choose)
        
        for ocr_i in ocr_res:
            for com_i in COMMISSION_NAMES:
                if com_i.text in ocr_i:
                    return com_i.name
        
        logger.warning(f"Unknown commission type: {ocr_res}")
        
        
        return None
        
    
    def get_commissions_list(self):
        return self._set_and_save_and_load_commission_dicts()
      
    # def get_commission_objects(self):
    #     if len(self.commission_dicts) == 0:
    #         self.traverse_mondstant()
    #     if len(self.commission_dicts) == 0:
    #         return False
    #     commission_objects = []
    #     # commission_index_positions = [COMMISSION_INDEX[i]["position"] for i in COMMISSION_INDEX]
    #     for i in self.commission_dicts:
    #         for ii in COMMISSION_INDEX:
    #             if euclidean_distance(i, COMMISSION_INDEX[ii]["position"]) <= 30:
    #                 commission_objects.append(ii)
    #     return commission_objects
                    
            
if __name__ == '__main__':
    cp = CommissionParser()
    # cp.commission_dicts.append([-999,999])
    a = cp.traverse_mondstant()
    print()
