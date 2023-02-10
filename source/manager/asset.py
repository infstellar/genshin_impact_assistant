from source.manager import img_manager, text_manager, button_manager
from source.util import *
from source.manager.img_manager import LOG_WHEN_TRUE, LOG_ALL, LOG_NONE, LOG_WHEN_FALSE, ImgIcon

# import scene_manager

LEAVINGIN = text_manager.TextTemplate(text=
{
    'zh_CN': '自动退出',
    "en_US": 'Leaving in'
}, cap_area = get_bbox(cv2.imread(os.path.join(root_path, "assets\\imgs\\common\\area\\LEAVINGIN.jpg"))))
claim_rewards = text_manager.TextTemplate(text=
{
    'zh_CN': '领取奖励',
    "en_US": "Claim Rewards"
})
use_20x2resin = text_manager.TextTemplate(text=
{
    'zh_CN': '使用浓缩树脂',
    "en_US": "Use Condensed Resin"
})
use_20resin = text_manager.TextTemplate(text=
{
    'zh_CN': '使用原粹树脂',
    "en_US": "Use Original Resin"
})
LEYLINEDISORDER = text_manager.TextTemplate(text=
{
    'zh_CN': '地脉异常',
    "en_US": "Ley Line Disorder"
}, cap_area = get_bbox(cv2.imread(os.path.join(root_path, "assets\\imgs\\common\\area\\LEYLINEDISORDER.jpg"))))
conti_challenge = text_manager.TextTemplate(text=
{
    'zh_CN': '继续挑战',
    "en_US": "Continue Challenge"
})
exit_challenge = text_manager.TextTemplate(text=
{
    'zh_CN': '退出秘境',
    "en_US": "Leave Domain"
})
domain_obtain = text_manager.TextTemplate(text=
{
    'zh_CN': '获得',
    "en_US": "Obtained"
})
use_revival_item = text_manager.TextTemplate(text=
{
    'zh_CN': '使用道具',
    "en_US": "Use revival item"
})
revival = text_manager.TextTemplate(text=
{
    'zh_CN': '复苏',
    "en_US": "Revive"
})
character_died = img_manager.ImgIcon(name="character_died", path="assets\\imgs\\$lang$\\character_died.jpg",
                                     is_bbg=True, cap_posi='bbg', win_text=use_revival_item.text, threshold=0.98, print_log=LOG_WHEN_TRUE)
button_all_character_died = button_manager.Button(name="all_character_died", path="assets\\imgs\\$lang$\\all_character_died.jpg",
                                                  threshold=0.988, win_text=revival.text, print_log=LOG_WHEN_TRUE)
button_esc_page = button_manager.Button(name="button_esc_page", path="assets\\imgs\\common\\ui\\emergency_food.jpg", print_log=LOG_WHEN_TRUE)
button_time_page = button_manager.Button(name="button_time_page",path="assets\\imgs\\common\\ui\\switch_to_time_menu.jpg", black_offset = 15, print_log=button_manager.LOG_WHEN_TRUE)
button_exit = button_manager.Button(path="assets\\imgs\\common\\button\\button_exit.jpg", print_log=LOG_WHEN_TRUE)
button_all_character_died = button_manager.Button( name="all_character_died", path="assets\\imgs\\$lang$\\all_character_died.jpg", 
                                   threshold=0.988, win_text="复苏", print_log=LOG_WHEN_TRUE)
button_ui_cancel = button_manager.Button(name="button_ui_cancel", path="assets\\imgs\\common\\ui\\ui_cancel.jpg",  print_log=LOG_WHEN_TRUE)

COMING_OUT_BY_SPACE = ImgIcon(name="coming_out_by_space", path="assets\\imgs\\common\\coming_out_by_space.jpg",
                              is_bbg=True, bbg_posi=[1379,505,  1447,568, ], cap_posi='bbg', threshold=0.8, print_log=LOG_WHEN_TRUE)
IN_DOMAIN = ImgIcon(name="IN_DOMAIN", path="assets\\imgs\\common\\IN_DOMAIN.jpg",
                    is_bbg=True, bbg_posi=[25,112,  52, 137, ], cap_posi='bbg', print_log=LOG_WHEN_TRUE)
USE_20RESIN_DOBLE_CHOICES = ImgIcon(name="USE_20RESIN_DOBLE_CHOICES",
                                    path="assets\\imgs\\$lang$\\USE_20RESIN_DOBLE_CHOICES.jpg",
                                    is_bbg=True, bbg_posi=[985, 724, 1348, 791 ], cap_posi='bbg', print_log=LOG_WHEN_TRUE)
USE_20X2RESIN_DOBLE_CHOICES = ImgIcon(name="USE_20X2RESIN_DOBLE_CHOICES",
                                      path="assets\\imgs\\$lang$\\USE_20X2RESIN_DOBLE_CHOICES.jpg",
                                      is_bbg=True, bbg_posi=[567,726 ,934, 793 ], cap_posi='bbg', print_log=LOG_WHEN_TRUE)
F_BUTTON = ImgIcon(name="F_BUTTON", path="assets\\imgs\\common\\F_BUTTON.jpg",
                   is_bbg=True, bbg_posi=[1104,526 , 1128,550 ], cap_posi=[1079,350 ,1162, 751 ],
                   threshold=0.92, print_log=LOG_WHEN_TRUE)
bigmap_TeleportWaypoint = ImgIcon(name="bigmap_TeleportWaypoint",
                                  path="assets\\imgs\\map\\big_map\\points\\TeleportWaypoint.jpg",
                                  is_bbg=False)
bigmap_GodStatue = ImgIcon(name="bigmap_GodStatue",
                                  path="assets\\imgs\\map\\big_map\\points\\GodStatue.jpg",
                                  is_bbg=False)
smallmap_AbyssMage = ImgIcon(name="smallmap_AbyssMage", path="assets\\imgs\\map\\small_map\\enemies\\AbyssMage.jpg",
                             is_bbg=False)
bigmap_AbyssMage = ImgIcon(name="bigmap_AbyssMage", path="assets\\imgs\\map\\big_map\\enemies\\AbyssMage.jpg",
                           is_bbg=False)
motion_swimming = ImgIcon(name="motion_swimming", path="assets\\imgs\\common\\motion_swimming.jpg",
                          is_bbg=True, bbg_posi=[1808,968,  1872,1016 ], cap_posi='bbg')
motion_climbing = ImgIcon(name="motion_climbing", path="assets\\imgs\\common\\motion_climbing.jpg",
                          is_bbg=True, bbg_posi=[1706,960,1866, 1022 ], cap_posi='bbg')
motion_flying = ImgIcon(name="motion_flying", path="assets\\imgs\\common\\motion_flying.jpg",
                        is_bbg=True, bbg_posi=[1706,960, 1866, 1022 ], cap_posi='bbg')
ui_main_win = ImgIcon(name="ui_main_win", path="assets\\imgs\\common\\ui\\emergency_food.jpg",
                      is_bbg=True, bbg_posi=[39,34, 73, 78 ], cap_posi='bbg', print_log=LOG_WHEN_TRUE, threshold=0.96)
ui_bigmap_win = ImgIcon(name="ui_bigmap_win", path="assets\\imgs\\common\\ui\\bigmap.jpg",
                        is_bbg=True, bbg_posi=[1591,36,1614, 59 ], cap_posi=[1300,36,1750, 59 ], print_log=LOG_WHEN_TRUE, threshold=0.95, offset=10)
ui_esc_menu = ImgIcon(name="ui_esc_menu", path="assets\\imgs\\common\\ui\\esc_menu.jpg",
                        is_bbg=True, cap_posi='bbg', jpgmode=0, print_log=LOG_WHEN_TRUE, threshold=0.96)
ui_switch_to_time_menu = ImgIcon(name="ui_switch_to_time_menu", path="assets\\imgs\\common\\ui\\switch_to_time_menu.jpg",
                        is_bbg=True, cap_posi='bbg', print_log=LOG_WHEN_TRUE)
ui_time_menu_core = ImgIcon(name="ui_time_menu_core", path="assets\\imgs\\common\\ui\\time_menu_core.jpg",
                        is_bbg=True, cap_posi='bbg', print_log=LOG_WHEN_TRUE, threshold=0.89)
bigmap_choose_area = ImgIcon(name="bigmap_choose_area", path="assets\\imgs\\common\\ui\\bigmap_choose_area.jpg", is_bbg=True, cap_posi='bbg')
bigmap_tp = ImgIcon(name="bigmap_tp", path="assets\\imgs\\$lang$\\bigmap_tp.jpg", is_bbg=True, cap_posi='bbg')

QTSX = text_manager.TextTemplate(text=
{
    "zh_CN":"七天神像",
    "en_US":"Statues of The Seven"
}, cap_area = bigmap_choose_area.cap_posi)
CSMD = text_manager.TextTemplate(text=
{
    "zh_CN":"传送锚点",
    "en_US": "Teleport Waypoint"
}, cap_area = bigmap_choose_area.cap_posi)