from source.util import *
import source.config


def unzip():
    pass
    # if not os.path.exists(os.path.join('assets\\AutoTrackDLLAPI', 'cvAutoTrack_7.2.3', 'CVAUTOTRACK.dll')):
    #     import zipfile
    #     with zipfile.ZipFile(os.path.join('source', 'cvAutoTrack_7.2.3', 'CVAUTOTRACK.zip')) as f:
    #         f.extractall(os.path.join('source', 'cvAutoTrack_7.2.3'))
    #     return 'unzip successfully'
    # return 'no operation required'


def auto_setup():
    print(unzip())
    # print(source.config.template_translator())
    # print(source.config.template_translator_tactic())

if __name__ == '__main__':
    auto_setup()