import subprocess
import os, sys
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

sys.argv.pop(0)

if len(sys.argv) == 1:
    if sys.argv[0] == 'install':
        if not os.path.exists('DTISTREQ'):
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '-i',
                                   'https://pypi.tuna.tsinghua.edu.cn/simple'])
            open('DTISTREQ', 'x')
        import installer_setup

        installer_setup.auto_setup()

    elif sys.argv[0] == 'update':
        subprocess.check_call(['git', 'pull'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '-i',
                               'https://pypi.tuna.tsinghua.edu.cn/simple'])
        if not os.path.exists('DTISTREQ'):
            open('DTISTREQ', 'x')
        import installer_setup

        installer_setup.auto_setup()

    elif sys.argv[0] == 'build':
        import source.config.config_updater
        import source.manager.asset_index_generator


