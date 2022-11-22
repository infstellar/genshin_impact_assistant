import os.path
import subprocess
import sys

sys.argv.pop(0)
if len(sys.argv) == 1:
    if sys.argv[0] == 'install':
        if not os.path.exists('DTISTREQ'):
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            open('DTISTREQ', 'x')
    elif sys.argv[0] == 'update':
        subprocess.check_call(['git', 'pull'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        if not os.path.exists('DTISTREQ'):
            open('DTISTREQ', 'x')
