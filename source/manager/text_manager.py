from source.manager.util import *


class TextTemplate(AssetBase):
    def __init__(self, text:dict, cap_area=None, name=None, match_mode=CONTAIN_MATCHING, print_log=LOG_WHEN_TRUE):
        if name is None:
            super().__init__(get_name(traceback.extract_stack()[-2]))
        else:
            super().__init__(name)
            
        if cap_area == None:
            cap_area = [0,0,1920,1080]
        elif isinstance(cap_area, str):
            path = self.get_img_path()
            cap_area = asset_get_bbox(cv2.imread(os.path.join(ROOT_PATH, path)))
        self.origin_text = text
        self.cap_area = cap_area
        self.text = self.origin_text[GLOBAL_LANG]
        self.match_mode = match_mode
        self.print_log = print_log
    def gettext(self):
        return self.origin_text[GLOBAL_LANG]

    def match_results(self, res:list):
        if isinstance(res, str):
            res = [res]
        for inp in res:
            #TODO: add match rules
            if res == '':
                return False
            if self.match_mode == CONTAIN_MATCHING:
                return self.text in res
            elif self.match_mode == ACCURATE_MATCHING:
                return self.text == res

class Text(TextTemplate):
    def __init__(self, name=None, cap_area=None, zh=None,en=None, print_log = LOG_WHEN_TRUE) -> None:
        if name is None:
            name = get_name(traceback.extract_stack()[-2])
        d={}
        if zh != None:
            d["zh_CN"]=zh
        if en != None:
            d["en_US"]=en
        super().__init__(d, cap_area=cap_area, name=name, print_log=print_log)


# if __name__ == '__main__':  
#     print(text(conti_challenge))