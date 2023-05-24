from source.util import *
from source.webio.pages import *
import subprocess
import pywebio
import source.webio.log_handler
from source.logger import add_logger_to_GUI
from source.webio.webpages.mission import MissionPage

status = True
global first_run
first_run = False
def get_branch_commit_id():
    res = subprocess.Popen('git rev-parse --short HEAD', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    res.wait()
    commit_id = res.stdout.read().decode('utf8').replace('\n', '')

    res = subprocess.Popen('git symbolic-ref --short -q HEAD', shell=True, stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    res.wait()
    branch = res.stdout.read().decode('utf8').replace('\n', '')
    return branch,commit_id
def main():
    global first_run
    pywebio.session.set_env(output_max_width='80%', title=f"GIA {GIA_VERSION} {get_branch_commit_id()[1]}")
    session.run_js(f'document.querySelector("body > footer").innerHTML+="| GIA: {"-".join(get_branch_commit_id())}"')
    webio.manager.reg_page('MainPage', MainPage())
    webio.manager.reg_page('SettingPage', SettingPage())
    webio.manager.reg_page('CombatSettingPage', CombatSettingPage())
    webio.manager.reg_page("CollectorSettingPage", CollectorSettingPage())
    webio.manager.reg_page("MissionPage", MissionPage())
    webio.manager.load_page('MainPage')
    if not first_run:
        add_logger_to_GUI(source.webio.log_handler.webio_poster)
        first_run = True
    logger.info(t2t("webio启动完成"))
    if DEMO_MODE:
        logger.demo(f"DEMO START!")


'''    handler = log_handler.WebioHandler()

    logging.getLogger().addHandler(handler)'''

'''    t = threading.Thread(target=session_check_thread, daemon=False)
    pywebio.session.register_thread(t)
    t.start()
    threading.Thread(target=session_check_thread_t, daemon=False).start()


def session_check_thread_t():
    global status
    while True:
        if not status:
            sys.exit()
        status = False
        time.sleep(0.3)


def session_check_thread():
    global status
    while True:
        pywebio.session.get_current_session()
        status = True
        time.sleep(0.1)'''

if __name__ == '__main__':
    platform.tornado.start_server(main, auto_open_webbrowser=True, debug=True)
