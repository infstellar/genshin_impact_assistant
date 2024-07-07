from source.manager.util import *


class TextTemplate(AssetBase):
    def __init__(self, text:dict, cap_area=None, name=None, match_mode=CONTAIN_MATCHING, is_log:bool=False) -> None:
        if name is None:
            super().__init__(get_name(traceback.extract_stack()[-2]))
        else:
            super().__init__(name)
            
        if cap_area == None:
            cap_area = [0,0,1920,1080]
        elif isinstance(cap_area, str):
            path = self.get_img_path()
            cap_area = get_bbox(cv2.imread(os.path.join(ROOT_PATH, path)))
        self.origin_text = text
        self.cap_area = cap_area
        self.text = self.origin_text[GLOBAL_LANG]
        self.match_mode = match_mode
        self.is_log = is_log
    def gettext(self):
        return self.origin_text[GLOBAL_LANG]

    def match_results(self, res:list):
        if isinstance(res, str):
            res = [res]
        for inp in res:
            #TODO: add match rules
            if inp in self.text or self.text in inp:
                return True
            else:
                return False

class Text(TextTemplate):
    def __init__(self, name=None, cap_area=None, zh=None,en=None) -> None:
        if name is None:
            name = get_name(traceback.extract_stack()[-2])
        d={}
        if zh != None:
            d["zh_CN"]=zh
        if en != None:
            d["en_US"]=en
        super().__init__(d, cap_area=cap_area, name=name)


# if __name__ == '__main__':  
#     print(text(conti_challenge))