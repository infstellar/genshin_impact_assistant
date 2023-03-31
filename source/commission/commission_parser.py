from source.map.map import genshin_map
from source.map.position.position import *
from source.ui.ui import ui_control
from source.ui import page as UIPages
from source.util import *
from source.interaction.interaction_core import itt
from source.manager import asset
from source.commission.commission_index import COMMISSION_INDEX, get_commission_object


class CommissionParser():
    TRAVERSE_MONDSTADT_POSITION=[TianLiPosition([976, -6710]),
                                 TianLiPosition([2488, -6448]),
                                 TianLiPosition([3797, -6344]),
                                 TianLiPosition([811, -5590]),
                                 TianLiPosition([2571, -5485]),
                                 TianLiPosition([1110, -4568]),
                                 TianLiPosition([2733, -4542]),
                                 TianLiPosition([4148, -4330]),
                                 TianLiPosition([1670, -3418])]
    
    def __init__(self) -> None:
        self.commission_positions = []

    def traverse_mondstant(self):
        self.commission_positions = []
        commission_positions = []
        ui_control.ensure_page(UIPages.page_bigmap)
        for posi in self.TRAVERSE_MONDSTADT_POSITION:
            genshin_map._move_bigmap(posi.tianli)
            cap_posi = [220,240,1920-200,1080-150]
            img = itt.capture(jpgmode=0)
            img = crop(img, cap_posi)
            img = recorp(img, [1920,1080,3],cap_posi)
            positions = itt.match_multiple_img(img, template=asset.CommissionIcon.image)
            if len(positions)>0:
                curr_posi = genshin_map.get_bigmap_posi()
                for i in positions:
                    target_px_posi = np.array(list(i))
                    delta_posi = genshin_map.convert_InGenshinMapPX_to_GIMAP(target_px_posi-np.array([SCREEN_CENTER_X,SCREEN_CENTER_Y]))
                    target_gimap_posi = curr_posi.gimap + delta_posi
                    target_tianli_posi = GIMAPPosition(target_gimap_posi).tianli
                    if len(commission_positions)>0:
                        if min(euclidean_distance_plist(target_tianli_posi, commission_positions)) >= 50:
                            commission_positions.append(target_tianli_posi)
                    else:
                        commission_positions.append(target_tianli_posi)
        self.commission_positions = commission_positions
        return commission_positions
    
    def get_commission_objects(self):
        if len(self.commission_positions) == 0:
            self.traverse_mondstant()
        if len(self.commission_positions) == 0:
            return False
        commission_objects_name = []
        # commission_index_positions = [COMMISSION_INDEX[i]["position"] for i in COMMISSION_INDEX]
        for i in self.commission_positions:
            for ii in COMMISSION_INDEX:
                if euclidean_distance(i, COMMISSION_INDEX[ii]["position"]) <= 30:
                    commission_objects_name.append(ii)
        return commission_objects_name
                    
            
if __name__ == '__main__':
    cp = CommissionParser()
    cp.commission_positions.append([-999,999])
    a = cp.get_commission_objects()
    print()
