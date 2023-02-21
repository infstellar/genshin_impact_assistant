from source.manager import img_manager, posi_manager
from source.util import *
from source.manager.img_manager import LOG_WHEN_TRUE, LOG_ALL, LOG_NONE, LOG_WHEN_FALSE, ImgIcon
from path_lib import ASSETS_IMG, ASSETS_COMMON_IMG
from source.manager.button_manager import Button
from source.manager.text_manager import TextTemplate

# import scene_manager

LEAVINGIN = TextTemplate(text=
{
    'zh_CN': '自动退出',
    "en_US": 'Leaving in'
}, cap_area = f"{ASSETS_IMG}\\common\\area\\LEAVINGIN.jpg")
claim_rewards = TextTemplate(text=
{
    'zh_CN': '领取奖励',
    "en_US": "Claim Rewards"
})
use_20x2resin = TextTemplate(text=
{
    'zh_CN': '使用浓缩树脂',
    "en_US": "Use Condensed Resin"
})
use_20resin = TextTemplate(text=
{
    'zh_CN': '使用原粹树脂',
    "en_US": "Use Original Resin"
})
LEYLINEDISORDER = TextTemplate(text=
{
    'zh_CN': '地脉异常',
    "en_US": "Ley Line Disorder"
}, cap_area = f"{ASSETS_IMG}\\common\\area\\LEYLINEDISORDER.jpg")
conti_challenge = TextTemplate(text=
{
    'zh_CN': '继续挑战',
    "en_US": "Continue Challenge"
})
exit_challenge = TextTemplate(text=
{
    'zh_CN': '退出秘境',
    "en_US": "Leave Domain"
})
domain_obtain = TextTemplate(text=
{
    'zh_CN': '获得',
    "en_US": "Obtained"
})
use_revival_item = TextTemplate(text=
{
    'zh_CN': '使用道具',
    "en_US": "Use revival item"
})
revival = TextTemplate(text=
{
    'zh_CN': '复苏',
    "en_US": "Revive"
})
confirm = TextTemplate(text=
{
    'zh_CN': '确认',
    "en_US": "Confirm"
})
character_died = img_manager.ImgIcon(name="character_died", path=f"{ASSETS_IMG}\\{GLOBAL_LANG}\\character_died.jpg",
                                     is_bbg=True, cap_posi='bbg', win_text=use_revival_item.text, threshold=0.98, print_log=LOG_WHEN_TRUE)
button_all_character_died = Button(name="all_character_died", path=f"{ASSETS_IMG}\\{GLOBAL_LANG}\\all_character_died.jpg",
                                                  threshold=0.988, win_text=revival.text, print_log=LOG_WHEN_TRUE)
button_esc_page = Button(name="button_esc_page", path=f"{ASSETS_COMMON_IMG}\\ui\\emergency_food.jpg", print_log=LOG_WHEN_TRUE)
button_time_page = Button(name="button_time_page",path=f"{ASSETS_COMMON_IMG}\\ui\\switch_to_time_menu.jpg", black_offset = 15, print_log=LOG_WHEN_TRUE)
button_exit = Button(path=f"{ASSETS_COMMON_IMG}\\button\\button_exit.jpg", print_log=LOG_WHEN_TRUE)
button_all_character_died = Button( name="all_character_died", path=f"{ASSETS_IMG}\\{GLOBAL_LANG}\\all_character_died.jpg", 
                                   threshold=0.988, win_text=revival.text, print_log=LOG_WHEN_TRUE)
button_ui_cancel = Button(name="button_ui_cancel", path=f"{ASSETS_COMMON_IMG}\\ui\\ui_cancel.jpg",  print_log=LOG_WHEN_TRUE)

COMING_OUT_BY_SPACE = ImgIcon(name="coming_out_by_space", path=f"{ASSETS_COMMON_IMG}\\coming_out_by_space.jpg",
                              is_bbg=True, bbg_posi=[1379,505,  1447,568, ], cap_posi='bbg', threshold=0.8, print_log=LOG_WHEN_TRUE)
IN_DOMAIN = ImgIcon(name="IN_DOMAIN", path=f"{ASSETS_COMMON_IMG}\\IN_DOMAIN.jpg",
                    is_bbg=True, cap_posi='bbg', print_log=LOG_WHEN_TRUE)
USE_20RESIN_DOUBLE_CHOICES = ImgIcon(name="USE_20RESIN_DOBLE_CHOICES",
                                    path=f"{ASSETS_IMG}\\{GLOBAL_LANG}\\USE_20RESIN_DOBLE_CHOICES.jpg",
                                    is_bbg=True, cap_posi='bbg', print_log=LOG_WHEN_TRUE)
USE_20X2RESIN_DOUBLE_CHOICES = ImgIcon(name="USE_20X2RESIN_DOBLE_CHOICES",
                                      path=f"{ASSETS_IMG}\\{GLOBAL_LANG}\\USE_20X2RESIN_DOBLE_CHOICES.jpg",
                                      is_bbg=True, cap_posi='bbg', print_log=LOG_WHEN_TRUE)
F_BUTTON = ImgIcon(name="F_BUTTON", path=f"{ASSETS_COMMON_IMG}\\F_BUTTON.jpg",
                   is_bbg=True, bbg_posi=[1104,526 , 1128,550 ], cap_posi=[1079,350 ,1162, 751 ],
                   threshold=0.92, print_log=LOG_WHEN_TRUE)
bigmap_TeleportWaypoint = ImgIcon(name="bigmap_TeleportWaypoint",
                                  path=f"{ASSETS_IMG}\\map\\big_map\\points\\TeleportWaypoint.jpg",
                                  is_bbg=False)
bigmap_GodStatue = ImgIcon(name="bigmap_GodStatue",
                                  path=f"{ASSETS_IMG}\\map\\big_map\\points\\GodStatue.jpg",
                                  is_bbg=False)
bigmap_Domain = ImgIcon(name="bigmap_Domain",
                                  path=f"{ASSETS_IMG}\\map\\big_map\\points\\Domain.jpg",
                                  is_bbg=False)
motion_swimming = ImgIcon(name="motion_swimming", path=f"{ASSETS_COMMON_IMG}\\motion_swimming.jpg",
                          is_bbg=True, bbg_posi=[1808,968,  1872,1016 ], cap_posi='bbg')# 不能删bbg
motion_climbing = ImgIcon(name="motion_climbing", path=f"{ASSETS_COMMON_IMG}\\motion_climbing.jpg",
                          is_bbg=True, bbg_posi=[1706,960,1866, 1022 ], cap_posi='bbg')# 不能删bbg
motion_flying = ImgIcon(name="motion_flying", path=f"{ASSETS_COMMON_IMG}\\motion_flying.jpg",
                        is_bbg=True, bbg_posi=[1706,960, 1866, 1022 ], cap_posi='bbg')# 不能删bbg
ui_main_win = ImgIcon(name="ui_main_win", path=f"{ASSETS_COMMON_IMG}\\ui\\emergency_food.jpg",
                      is_bbg=True, cap_posi='bbg', print_log=LOG_WHEN_TRUE, threshold=0.96)
ui_bigmap_win = ImgIcon(name="ui_bigmap_win", path=f"{ASSETS_COMMON_IMG}\\ui\\bigmap.jpg",
                        is_bbg=True, cap_posi=[1300,36,1750, 59 ], print_log=LOG_WHEN_TRUE, threshold=0.95, offset=10)
ui_esc_menu = ImgIcon(name="ui_esc_menu", path=f"{ASSETS_COMMON_IMG}\\ui\\esc_menu.jpg",
                        is_bbg=True, cap_posi='bbg', jpgmode=0, print_log=LOG_WHEN_TRUE, threshold=0.96)
ui_switch_to_time_menu = ImgIcon(name="ui_switch_to_time_menu", path=f"{ASSETS_COMMON_IMG}\\ui\\switch_to_time_menu.jpg",
                        is_bbg=True, cap_posi='bbg', print_log=LOG_WHEN_TRUE)
ui_time_menu_core = ImgIcon(name="ui_time_menu_core", path=f"{ASSETS_COMMON_IMG}\\ui\\time_menu_core.jpg",
                        is_bbg=True, cap_posi='bbg', print_log=LOG_WHEN_TRUE, threshold=0.89)
bigmap_choose_area = ImgIcon(name="bigmap_choose_area", path=f"{ASSETS_COMMON_IMG}\\ui\\bigmap_choose_area.jpg", is_bbg=True, cap_posi='bbg')
bigmap_tp = ImgIcon(name="bigmap_tp", path=f"{ASSETS_IMG}\\{GLOBAL_LANG}\\bigmap_tp.jpg", is_bbg=True, cap_posi='bbg')
start_challenge = Button(name="start_challenge", path=f"{ASSETS_IMG}\\{GLOBAL_LANG}\\start_challenge.jpg", print_log=LOG_WHEN_TRUE, threshold=0.98)
switch_domain_area = posi_manager.PosiTemplate(img_path=f"{ASSETS_COMMON_IMG}\\area\\switch_challenge_area.jpg")
solo_challenge = Button(name = "solo_challenge", path=f"{ASSETS_IMG}\\{GLOBAL_LANG}\\solo_challenge.jpg", print_log=LOG_WHEN_TRUE, threshold=0.98)
character_q_skills = posi_manager.PosiTemplate()
character_q_skills.add_posi(img_path=f"{ASSETS_COMMON_IMG}\\area\\QSkill\\c1.jpg")
character_q_skills.add_posi(img_path=f"{ASSETS_COMMON_IMG}\\area\\QSkill\\c2.jpg")
character_q_skills.add_posi(img_path=f"{ASSETS_COMMON_IMG}\\area\\QSkill\\c3.jpg")
character_q_skills.add_posi(img_path=f"{ASSETS_COMMON_IMG}\\area\\QSkill\\c4.jpg")
ButtonEgg = Button(path=f"{ASSETS_COMMON_IMG}\\button\\Foods\\ButtonEgg.jpg", cap_posi='all', is_bbg = False)

QTSX = TextTemplate(text=
{
    "zh_CN":"七天神像",
    "en_US":"Statues of The Seven"
}, cap_area = bigmap_choose_area.cap_posi)
CSMD = TextTemplate(text=
{
    "zh_CN":"传送锚点",
    "en_US": "Teleport Waypoint"
}, cap_area = bigmap_choose_area.cap_posi)