import os
import sys

class GenerateMarkdown():
    def __init__(self, folder_path, LANG) -> None:
        self.folder_path = folder_path
        self.LANG = LANG
    
    def run(self):
        command_head = "python"
        for root, dirs, files in os.walk(f"{self.folder_path}\\base"):
            for f in files:
                if f.split('.')[-1] == 'py':
                    command = os.path.join(root, f)
                    print(f'{command_head} {command} {self.LANG}')
                    os.system(f'{command_head} {command} {self.LANG}')

if __name__ == "__main__":
    rf = GenerateMarkdown(r"md_test", "en_US")
    rf.run()