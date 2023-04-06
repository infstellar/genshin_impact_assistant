import os

for root, dirs, files in os.walk(os.path.abspath(r'source')):
    for file in files:
        if file.endswith('.py'):
            print(file)
            os.system(f'python translation\\pygettext.py -d zh_CN -o pott.pot {os.path.join(root, file)}')
            # os.system(f'python translation\\pygettext.py -d en_US -p translation\\locale\\en_US\\LC_MESSAGES {os.path.join(root, file)}')