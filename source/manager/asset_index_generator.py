from source.util import *


class AssetsIndexGenerator():
    def __init__(self) -> None:
        pass

    def traversal(self):
        index_dict = {}
        folder_path = "assets\\imgs\\Windows"
        for root, dirs, files in os.walk(folder_path):
            for f in files:
                index_dict.setdefault(f"{f.split('.')[0]}",{})
                index_dict[f"{f.split('.')[0]}"][root.split('\\')[-1]]=os.path.join(root,f)
        # logger.error(f"SearchPathError:{filename}")
        return index_dict

    def generate(self):
        save_json(self.traversal(), json_name="imgs_index.json", default_path=fr"{ASSETS_PATH}/imgs")

if __name__ == '__main__':
    AssetsIndexGenerator().generate()