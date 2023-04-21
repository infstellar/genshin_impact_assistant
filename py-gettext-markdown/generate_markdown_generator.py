import gettext
import re
import os
from util import *

class GenerateMarkdownGenerator():
    def __init__(self, folder_path, LANG):
        self.folder_path = folder_path
        self.LANG = LANG

    def _write_file(self, file_path):
        origin_file = open(file_path, 'r', encoding='utf-8').read()
        text_list = re.split('  \n|\n\n|<br>',origin_file)
        text_list = [i.replace('\n', '\\n').replace('\"', '\\"') for i in text_list]
        with open(file_path.replace('.md','.pygettext'), 'w', encoding='utf-8') as f:
            f.write(f'import gettext, sys\n')
            f.write(f"sys.argv.pop(0)\n")
            f.write(f"LANG = sys.argv[0]\n")
            f.write(f'l10n = gettext.translation(LANG, localedir = r"{self.folder_path}/markdown_i18n/locale", languages=[LANG])\n')
            f.write('l10n.install()\n')
            f.write(f'_ = l10n.gettext\n')
            md_path = f'{file_path.replace("base",self.LANG)}'
            verify_path(os.path.dirname(md_path))
            f.write(f'f = open(r"{md_path}", "w", encoding="utf-8")\n')
            def write_gettext(x):
                f.write(f'f.write(_("{x}")+str(\'\\n\'))\n')
            def write_origin(x):
                f.write(f'f.write("{x}"+str(\'\\n\'))\n')
            def write_newline():
                f.write(f'f.write("\\n")\n')
            i=0
            while 1:
                if i>=len(text_list):break
                if "<!-- ignore gettext -->" in text_list[i]:
                    write_origin(text_list[i])
                elif "----|----" in text_list[i]:
                    for ii in text_list[i].split('\\n'):
                        if "----|----" in ii:
                            write_origin(ii)
                        else:
                            write_gettext(ii)
                elif "```" in text_list[i]:
                    if text_list[i].count("```")>=2:
                        write_origin(text_list[i])
                    else:
                        while 1:
                            write_origin(text_list[i])
                            write_newline()
                            i+=1
                            if "```" in text_list[i]:
                                write_origin(text_list[i])
                                break
                elif text_list[i] == "":
                    pass
                elif text_list[i] == "\n":
                    write_newline()    
                elif text_list[i] == "\\n":
                    write_newline()   
                else:
                    write_gettext(text_list[i])
                write_newline()
                i+=1
            f.write(f'f.close()')
    
    def run(self):
        for root, dirs, files in os.walk(self.folder_path+'\\base'):
            for f in files:
                if f.split('.')[-1] in ['md', 'markdown']:
                    print(f"generate pygettext {root}/{f}")
                    self._write_file(f"{root}/{f}")
      
if __name__ == "__main__":
    gmg = GenerateMarkdownGenerator(os.path.abspath('doc'), "zh_CN")
    gmg.run()