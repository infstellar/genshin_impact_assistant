from util import *

class GenerateMarkdown():
    def __init__(self, folder_path, LANG) -> None:
        self.folder_path = folder_path
        self.LANG = LANG

    def compile_po_file(self, po_file_path):
        po_file_path = os.path.abspath(po_file_path)
        mo_file_path = os.path.splitext(po_file_path)[0] + '.mo'
        print(f"complite po file:{po_file_path}")
        exec_cmd(fr"python msgfmt.py -o {mo_file_path} {po_file_path}")

    def run(self):
        command_head = "python"
        self.compile_po_file(rf"{self.folder_path}/markdown_i18n/locale/{self.LANG}/LC_MESSAGES/{self.LANG}.po")
        for root, dirs, files in os.walk(f"{self.folder_path}\\base"):
            for f in files:
                if f.split('.')[-1] == 'pygettext':
                    command = os.path.join(root, f)
                    print(f'{command_head} {command} {self.LANG}')
                    os.system(f'{command_head} {command} {self.LANG}')

if __name__ == "__main__":
    rf = GenerateMarkdown(r"md_test", "en_US")
    rf.run()