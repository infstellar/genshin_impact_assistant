from source.util import *
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
        filename+=".jpg"
        folder_path = os.path.join(ASSETS_PATH)
        for root, dirs, files in os.walk(folder_path):
            if filename in files:
                return os.path.abspath(os.path.join(root, filename))
        logger.error(f"SearchPathError:{filename}")
        return None