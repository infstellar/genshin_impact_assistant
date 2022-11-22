import os.path
import shutil
import subprocess
import sys

sys.argv.pop(0)
if len(sys.argv) == 1:
    if sys.argv[0] == 'install':
        if not os.path.exists('DTISTREQ'):
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '-i',
                                   'https://pypi.tuna.tsinghua.edu.cn/simple'])
            open('DTISTREQ', 'x')
        if not os.path.exists(os.path.join('source', 'cvAutoTrack_7.2.3', 'CVAUTOTRACK.dll')):
            import py7zr

            with py7zr.SevenZipFile(os.path.join('source', 'cvAutoTrack_7.2.3', 'CVAUTOTRACK.7z'), mode='r') as z:
                z.extractall()
                shutil.move('CVAUTOTRACK.dll', os.path.join('source', 'cvAutoTrack_7.2.3', 'CVAUTOTRACK.dll'))

    elif sys.argv[0] == 'update':
        subprocess.check_call(['git', 'pull'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '-i',
                               'https://pypi.tuna.tsinghua.edu.cn/simple'])
        if not os.path.exists('DTISTREQ'):
            open('DTISTREQ', 'x')
