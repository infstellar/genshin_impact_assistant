from util import *

class GeneratePot():
    def __init__(self, folder_path, LANG) -> None:
        self.folder_path = folder_path
        self.LANG = LANG
    
    def run(self):
        command=''
        verify_path(self.folder_path)
        for root, dirs, files in os.walk(f"{self.folder_path}\\base"):
            for d in dirs:
                if '__pycache__' in d: continue
                print(os.path.join(root,d))
                command += f"{os.path.join(root,d)}\\*.pygettext "
        command += f"{self.folder_path}\\base\\*.pygettext "
        pot_path = f"{self.folder_path}\\markdown_i18n\\locale\\{self.LANG}\\LC_MESSAGES"
        verify_path(pot_path)
        command_head = f"python pygettext.py -k t2t -d {self.LANG} -p {pot_path}"
        print(f'{command_head} {command}')
        os.system(f'{command_head} {command}')

if __name__ == "__main__":
    rf = GeneratePot(r"md_test", "en_US")
    rf.run()