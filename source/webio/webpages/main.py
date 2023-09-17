from source.util import *
from pywebio import *
from source.webio.util import *

import socket
import threading
import time

from source import listening
from source.webio.advance_page import AdvancePage
from source.common import timer_module
from source.webio.update_notice import upd_message
from source.config.cvars import *
from source.generic_event import generic_event



class MainPage(AdvancePage):
    
    PROCESSBAR_PERFORMANCE = AN()
    SCOPE_PERFORMANCE = AN()
    
    def __init__(self):
        super().__init__()
        self.log_list = []
        self.log_history = []
        self.log_list_lock = threading.Lock()
        self.ui_statement = -1
        self.refresh_flow_info_timer = timer_module.Timer()
        self.ui_mission_select = ""
        self.is_task_start = False

    # todo:多语言支持

    def _on_load(self):  # 加载事件
        super()._on_load()
        pin.pin['FlowMode'] = listening.current_flow

    def _event_thread(self):
        while self.loaded:  # 当界面被加载时循环运行
            try:
                pin.pin['isSessionExist']
            except SessionNotFoundException:
                logger.info(t2t("未找到会话，可能由于窗口关闭。请刷新页面重试。"))
                return
            except SessionClosedException:
                logger.info(t2t("未找到会话，可能由于窗口关闭。请刷新页面重试。"))
                return
            if pin.pin['FlowMode'] != listening.current_flow:  # 比较变更是否被应用
                listening.current_flow = pin.pin['FlowMode']  # 应用变更
                self.log_list_lock.acquire()
                output.put_text(t2t("正在导入模块, 可能需要一些时间。"), scope='LogArea').style(
                    f'color: black; font_size: 20px')
                output.put_text(t2t("在导入完成前，请不要切换页面。"), scope='LogArea').style(
                    f'color: black; font_size: 20px')
                self.log_list_lock.release()
                listening.call_you_import_module()
                                # if pin.pin["MissionSelect"] != self.ui_mission_select:
                                #     self.ui_mission_select = pin.pin["MissionSelect"]
                                #     output.clear_scope("SCOPEMissionIntroduction")
                                #     if self.ui_mission_select is None:
                                #         continue
                                    # output.put_text(self._get_mission_groups_dict()["introduction"][GLOBAL_LANG],scope="SCOPEMissionIntroduction")
            
            # Output log
            
            self.log_list_lock.acquire()
            for text, color in self.log_list:
                if text == "$$end$$":
                    output.put_text("", scope='LogArea')
                else:
                    output.put_text(text, scope='LogArea', inline=True).style(f'color: {color}; font_size: 20px') # ; background: aqua
            
            self.log_list.clear()
            self.log_list_lock.release()

            # refresh task state
            
            if self.refresh_flow_info_timer.get_diff_time() >= 0.2:
                self.refresh_flow_info_timer.reset()
                if listening.TASK_MANAGER.get_task_statement() != self.ui_statement:
                    self.ui_statement = listening.TASK_MANAGER.get_task_statement()
                    output.clear(scope="StateArea")
                    # if isinstance(self.ui_statement, list):
                    #     for i in self.ui_statement:
                    #         output.put_text(f'{i["name"]}: {i["statement"]}: {i["rfc"]}', scope="StateArea")
                    # elif isinstance(self.ui_statement, str):
                    output.put_text(f'{self.ui_statement}', scope="StateArea")

                if listening.TASK_MANAGER.start_tasklist_flag != self.is_task_start:
                    self.is_task_start = listening.TASK_MANAGER.start_tasklist_flag
                    output.clear('Button_StartStop')
                    output.put_button(label=str(listening.TASK_MANAGER.start_tasklist_flag), onclick=self.on_click_startstop,
                          scope='Button_StartStop')

            # refresh performance bar
            
            
            output.set_progressbar(name=self.PROCESSBAR_PERFORMANCE, value=generic_event.dilation_rate, label=f'{generic_event.dilation_rate_note}     {t2t("running speed")}: {round(generic_event.dilation_rate,2)*100}%')
            # output.clear(self.SCOPE_PERFORMANCE)
            if generic_event.dilation_rate<=0.6:
                output.toast(t2t("Warning: Extremely low performance, if you see this message for a long time, please check if your computer meets the lowest requirements."), color='red')
                time.sleep(0.5)
                
            time.sleep(0.1)
    
    def _load(self):
        # 标题
        # 获得链接按钮
        with output.use_scope(self.main_scope):
            output.put_row([
                output.put_button(label=t2t("Get IP address"), onclick=self.on_click_ip_address, scope=self.main_scope),
                output.put_button(label=t2t("Open log folder"), onclick=self._onclick_open_log_folder, scope=self.main_scope),
                output.put_processbar(name=self.PROCESSBAR_PERFORMANCE, init = 1),
                output.put_scope(name=self.SCOPE_PERFORMANCE),
                output.put_link(t2t('View Document'), url='https://genshinimpactassistant.github.io/GIA-Document', new_window = True).style('font-size: 20px')
            ])
            

            task_options = [
                    {
                        "label":t2t("Launch genshin"),
                        "value":"LaunchGenshinTask"
                    },
                    {
                        "label":t2t("Domain Task"),
                        "value":"DomainTask"
                    },
                    {
                        "label":t2t("Daily Commission"),
                        "value":"CommissionTask"
                    },
                    {
                        "label":t2t("Claim Reward"),
                        "value":"ClaimRewardTask"
                    },
                    {
                        "label":t2t("Ley Line Outcrop"),
                        "value":"LeyLineOutcropTask"
                    },
                    {
                        "label":t2t("Mission"),
                        "value":"MissionTask"
                    }
                ]
            output.put_row([  # 横列
                output.put_column([  # 左竖列
                    output.put_markdown('## '+t2t("Task List")),
                    output.put_markdown(t2t("Can only be activated from the button")),
                    pin.put_checkbox(name="task_list", options=task_options),
                    output.put_row([output.put_text(t2t('启动/停止Task')), None, output.put_scope('Button_StartStop')],size='40% 10px 60%'),
                    
                    output.put_markdown(t2t('## Statement')),
                    output.put_row([output.put_text(t2t('任务状态')), None, output.put_scope('StateArea')],size='40% 10px 60%'),
                    output.put_markdown(t2t('## Semi-automatic Functions')),
                    output.put_markdown(t2t("Can only be activated from the hotkey \'[\'")),
                    output.put_text(t2t('Do not enable semi-automatic functions and tasks at the same time')),
                    output.put_row([  # FlowMode
                        output.put_text(t2t('Semi-automatic Functions')),
                        
                        pin.put_select(('FlowMode'), [
                            {'label': t2t('Idle'), 'value': listening.FLOW_IDLE},
                            {'label': t2t('Auto Combat'), 'value': listening.FLOW_COMBAT}
                        ])
                        ],
                    ),
                    output.put_markdown(t2t('## Ingame assist')),
                    output.put_row([  # FlowMode
                        output.put_button(t2t('apply'), onclick=self._onclick_apply_ingame_assist),
                        pin.put_checkbox(name="ingame_assist", options=[
                            {
                                'label':t2t('Pickup assist'),
                                'value':'pickup_assist'
                            },
                            {
                                'label':t2t('Auto story assist'),
                                'value':'story_skip_assist'
                            }]
                        )
                        ]),
                ], size='auto'), None,
                output.put_scope('Log')

            ], scope=self.main_scope, size='40% 10px 60%')

            # PickUpButton
            output.put_button(label=str(listening.FEAT_PICKUP), onclick=self.on_click_pickup, scope='Button_PickUp')
            # Button_StartStop
            output.put_button(label=str(listening.startstop_flag), onclick=self.on_click_startstop,
                            scope='Button_StartStop')

            # Log
            output.put_markdown(t2t('## Log'), scope='Log')
            output.put_scrollable(output.put_scope('LogArea'), height=600, keep_bottom=True, scope='Log')
            '''self.main_pin_change_thread = threading.Thread(target=self._main_pin_change_thread, daemon=False)
            self.main_pin_change_thread.start()'''

            m = upd_message()
            if m!="":
                output.popup(t2t('Update Notice'), m, implicit_close=False)
        
    # def _get_mission_groups_config(self):
    #     jsons = load_json_from_folder(f"{CONFIG_PATH}\\mission_groups")
    #     r = [i["label"] for i in jsons]
    #     return r

    # def _get_mission_groups_dict(self):
    #     jsonname = pin.pin["MissionSelect"]
    #     if jsonname is None:
    #         raise FileNotFoundError
    #     return load_json(str(jsonname),default_path=f"{CONFIG_PATH}\\mission_groups")
    
    def on_click_pickup(self):
        output.clear('Button_PickUp')
        listening.FEAT_PICKUP = not listening.FEAT_PICKUP
        output.put_button(label=str(listening.FEAT_PICKUP), onclick=self.on_click_pickup, scope='Button_PickUp')
    
    def on_click_startstop(self):
        # listening.MISSION_MANAGER.set_mission_list(list(pin.pin["MissionSelect"]))
        listening.TASK_MANAGER.set_tasklist(pin.pin["task_list"])
        listening.TASK_MANAGER.start_stop_tasklist()
        # if pin.pin["MissionSelect"] != None and pin.pin["MissionSelect"] != "":
        #     cj = load_json()
        #     cj["MissionGroup"] = pin.pin["MissionSelect"]
        #     save_json(cj)
        #     GIAconfig.update()

        time.sleep(0.2)
        output.clear('Button_StartStop')
        output.put_button(label=str(listening.TASK_MANAGER.start_tasklist_flag), onclick=self.on_click_startstop,
                          scope='Button_StartStop')

    def on_click_ip_address(self):
        LAN_ip = f"{socket.gethostbyname(socket.gethostname())}{session.info.server_host[session.info.server_host.index(':'):]}"
        WAN_ip = t2t("Not Enabled")
        output_text = t2t('LAN IP') + " : " + LAN_ip + '\n' + t2t("WAN IP") + ' : ' + WAN_ip
        output.popup(f'ip address', output_text, size=output.PopupSize.SMALL)

    def _onclick_apply_ingame_assist(self):
        listening.INGAME_ASSIST_MANAGER.apply_change(pin.pin['ingame_assist'])

    @logger.catch
    def _onclick_open_log_folder(self):
        os.startfile(os.path.join(ROOT_PATH, "Logs"))

    def logout(self, text: str, color='black'):
        if self.loaded:
            self.log_list_lock.acquire()
            self.log_list.append((text, color))
            self.log_list_lock.release()