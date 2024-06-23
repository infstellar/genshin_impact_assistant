from source.util import *
from source.api.utils import *
import traceback

class IMG_NOT_FOUND(Exception):pass
class NAME_NOT_FOUND(Exception):pass
ASSETS_INDEX_JSON = load_json("imgs_index.json", fr"{ASSETS_PATH}/imgs")


def get_name(x):
    (filename, line_number, function_name, text) = x
    # = traceback.extract_stack()[-2]
    return text[:text.find('=')].strip()

class AssetBase():
    def __init__(self, name:str) -> None:
        if name is None:
            raise NAME_NOT_FOUND
        self.name = name

    def get_img_path(self):
        if self.name in ASSETS_INDEX_JSON:
            if 'common' in ASSETS_INDEX_JSON[self.name]:
                return ASSETS_INDEX_JSON[self.name]['common']
            elif GLOBAL_LANG in ASSETS_INDEX_JSON[self.name]:
                return ASSETS_INDEX_JSON[self.name][GLOBAL_LANG]
        r = self.search_path(self.name)
        if r != None:
            return r
        else:
            raise IMG_NOT_FOUND(self.name)
                
    def search_path(self, filename) -> str:
        for comp_filename in [filename+'.png',filename+'.jpg']:
            folder_path = os.path.join(ASSETS_PATH)
            for root, dirs, files in os.walk(folder_path):
                if comp_filename in files:
                    return os.path.abspath(os.path.join(root, comp_filename))
            logger.error(f"SearchPathError:{comp_filename}")
            return None


class Bbox():
    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.center = [(x1+x2)/2,(y1+y2)/2]
        pass

    def get_center_posi(self):
        pass

class TextReplaceRule():
    #TODO: add more modes
    rep_rules = {}
    def __init__(self):
        pass

    def rep(self, x):
        return self.rep_rules[x]