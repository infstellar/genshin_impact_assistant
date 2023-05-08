import os
os.path.abspath("translation\\pygettext")
pyfile = os.path.abspath('translation\\pygettext.py')
command_head_en = f"python translation\\pygettext.py -k t2t -d en_US -p translation\\locale\\en_US\\LC_MESSAGES"
command_head_zh = f'python translation\\pygettext.py -k t2t -d zh_CN -p translation\\locale\\zh_CN\\LC_MESSAGES'
command=r'genshin_assistant.py '
for root, dirs, files in os.walk(r'source'):
    for d in dirs:
        if '__pycache__' in root or d == '__pycache__':
            continue
        print(os.path.join(root,d))
        command+=f"{os.path.join(root,d)}\\*.py "
print(f'{command_head_en} {command}')
os.system(f'{command_head_en} {command}')
print(f'{command_head_zh} {command}')
os.system(f'{command_head_zh} {command}')