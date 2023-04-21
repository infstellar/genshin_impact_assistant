from util import *

class CleanFiles():
    def __init__(self, folder) -> None:
        self.folder_path = folder

    def run(self):
        for root, dirs, files in os.walk(self.folder_path+'\\base'):
            for f in files:
                if f.split('.')[-1] in ['pygettext', 'py']:
                    os.remove(f"{root}/{f}")
                    print(f'remove {root}/{f}')