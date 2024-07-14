from source.manager.util import *
from source.manager.text_manager import TextTemplate
from source.manager.img_manager import ImgIcon, AssetBase

class TextIconTemplate(TextTemplate, ImgIcon, AssetBase):
    """
    截取出一个图片，但不是匹配图片而是匹配图片中的文字。
    仅支持GIA-BBG格式图片。参考：# TODO: add link
    """
    def __init__(self,text:dict, name=None, match_mode=CONTAIN_MATCHING, print_log=LOG_WHEN_TRUE, offset=0):
        if name is None:
            name = get_name(traceback.extract_stack()[-2])
        path = self.get_img_path()
        AssetBase.__init__(self, name=name)
        ImgIcon.__init__(self, path=path, name=name, is_bbg=True, offset=offset)
        TextTemplate.__init__(self, name=name, cap_area=self.cap_posi, text=text, match_mode=match_mode, print_log=print_log)


class TextIcon(TextIconTemplate):
    def __init__(self,name=None, zh=None,en=None,match_mode=CONTAIN_MATCHING, print_log=LOG_WHEN_TRUE, offset=0):
        if name is None:
            name = get_name(traceback.extract_stack()[-2])
        d = {}
        if zh != None:
            d["zh_CN"] = zh
        if en != None:
            d["en_US"] = en
        super().__init__(d, name=name, match_mode=match_mode, print_log=print_log, offset=offset)
