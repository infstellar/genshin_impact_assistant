from source.manager import img_manager, posi_manager
from source.util import *
from source.manager.img_manager import LOG_WHEN_TRUE, LOG_ALL, LOG_NONE, LOG_WHEN_FALSE, ImgIcon
from path_lib import ASSETS_IMG, ASSETS_COMMON_IMG
from source.manager.button_manager import Button
from source.manager.text_manager import TextTemplate
from source.manager.posi_manager import PosiTemplate

# import scene_manager

LEAVINGIN = TextTemplate(text={'zh_CN': '自动退出',"en_US": 'Leaving in'}, cap_area = f"{ASSETS_IMG}\\common\\area\\LEAVINGIN.jpg")
claim_rewards = TextTemplate(text={'zh_CN': '领取奖励',"en_US": "Claim Rewards"})
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

character_died = img_manager.ImgIcon(path=f"{ASSETS_IMG}\\{GLOBAL_LANG}\\character_died.jpg",
                                     win_text = use_revival_item.text, threshold=0.98, print_log=LOG_WHEN_TRUE)
button_all_character_died = Button(path=f"{ASSETS_IMG}\\{GLOBAL_LANG}\\all_character_died.jpg",
                                                  threshold=0.988, win_text=revival.text, print_log=LOG_WHEN_TRUE)
button_esc_page = Button(path=f"{ASSETS_COMMON_IMG}\\ui\\emergency_food.jpg", print_log=LOG_WHEN_TRUE)
button_time_page = Button(path=f"{ASSETS_COMMON_IMG}\\ui\\switch_to_time_menu.jpg", black_offset = 15, print_log=LOG_WHEN_TRUE)
button_exit = Button(path=f"{ASSETS_COMMON_IMG}\\button\\button_exit.jpg", print_log=LOG_WHEN_TRUE)
button_all_character_died = Button(path=f"{ASSETS_IMG}\\{GLOBAL_LANG}\\all_character_died.jpg", 
                                   threshold=0.988, win_text=revival.text, print_log=LOG_WHEN_TRUE)
button_ui_cancel = Button(path=f"{ASSETS_COMMON_IMG}\\ui\\ui_cancel.jpg",  print_log=LOG_WHEN_TRUE)

COMING_OUT_BY_SPACE = ImgIcon(path=f"{ASSETS_COMMON_IMG}\\coming_out_by_space.jpg",
                               bbg_posi=[1379,505,  1447,568, ], cap_posi='bbg', threshold=0.8, print_log=LOG_WHEN_TRUE)
IN_DOMAIN = ImgIcon(path=f"{ASSETS_COMMON_IMG}\\IN_DOMAIN.jpg",
                     print_log=LOG_WHEN_TRUE)
USE_20RESIN_DOUBLE_CHOICES = ImgIcon(path=f"{ASSETS_IMG}\\{GLOBAL_LANG}\\USE_20RESIN_DOBLE_CHOICES.jpg",
                                     print_log=LOG_WHEN_TRUE)
USE_20X2RESIN_DOUBLE_CHOICES = ImgIcon(path=f"{ASSETS_IMG}\\{GLOBAL_LANG}\\USE_20X2RESIN_DOBLE_CHOICES.jpg",
                                        print_log=LOG_WHEN_TRUE)
F_BUTTON = ImgIcon(path=f"{ASSETS_COMMON_IMG}\\F_BUTTON.jpg",
                    bbg_posi=[1104,526 , 1128,550 ], cap_posi=[1079,350 ,1162, 751 ],
                   threshold=0.92, print_log=LOG_WHEN_TRUE)
bigmap_TeleportWaypoint = ImgIcon(path=f"{ASSETS_IMG}\\map\\big_map\\points\\TeleportWaypoint.jpg",
                                  is_bbg=False)
bigmap_GodStatue = ImgIcon(path=f"{ASSETS_IMG}\\map\\big_map\\points\\GodStatue.jpg",
                                  is_bbg=False)
bigmap_Domain = ImgIcon(path=f"{ASSETS_IMG}\\map\\big_map\\points\\Domain.jpg",
                                  is_bbg=False)
motion_swimming = ImgIcon(path=f"{ASSETS_COMMON_IMG}\\motion_swimming.jpg",
                           bbg_posi=[1808,968,  1872,1016 ], cap_posi='bbg')# 不能删bbg
motion_climbing = ImgIcon(path=f"{ASSETS_COMMON_IMG}\\motion_climbing.jpg",
                           bbg_posi=[1706,960,1866, 1022 ], cap_posi='bbg')# 不能删bbg
motion_flying = ImgIcon(path=f"{ASSETS_COMMON_IMG}\\motion_flying.jpg",
                         bbg_posi=[1706,960, 1866, 1022 ], cap_posi='bbg')# 不能删bbg
ui_main_win = ImgIcon(path=f"{ASSETS_COMMON_IMG}\\ui\\emergency_food.jpg",
                        print_log=LOG_WHEN_TRUE, threshold=0.98)
ui_bigmap_win = ImgIcon(path=f"{ASSETS_COMMON_IMG}\\ui\\bigmap.jpg",
                         cap_posi=[1300,36,1750, 59 ], print_log=LOG_WHEN_TRUE, threshold=0.95, offset=10)
ui_esc_menu = ImgIcon(path=f"{ASSETS_COMMON_IMG}\\ui\\esc_menu.jpg",
                          jpgmode=0, print_log=LOG_WHEN_TRUE, threshold=0.97)
ui_switch_to_time_menu = ImgIcon(path=f"{ASSETS_COMMON_IMG}\\ui\\switch_to_time_menu.jpg",
                          print_log=LOG_WHEN_TRUE)
ui_time_menu_core = ImgIcon(path=f"{ASSETS_COMMON_IMG}\\ui\\time_menu_core.jpg",
                          print_log=LOG_WHEN_TRUE, threshold=0.89)
BigmapChooseArea = PosiTemplate(img_path=f"{ASSETS_COMMON_IMG}\\ui\\bigmap_choose_area.jpg")
bigmap_tp = ImgIcon(path=f"{ASSETS_IMG}\\{GLOBAL_LANG}\\bigmap_tp.jpg",  cap_posi='bbg')
start_challenge = Button(path=f"{ASSETS_IMG}\\{GLOBAL_LANG}\\start_challenge.jpg", print_log=LOG_WHEN_TRUE, threshold=0.98)
switch_domain_area = posi_manager.PosiTemplate(img_path=f"{ASSETS_COMMON_IMG}\\area\\switch_challenge_area.jpg")
solo_challenge = Button(path=f"{ASSETS_IMG}\\{GLOBAL_LANG}\\solo_challenge.jpg", print_log=LOG_WHEN_TRUE, threshold=0.98)
character_q_skills = posi_manager.PosiTemplate(img_path=f"{ASSETS_COMMON_IMG}\\area\\QSkill\\c1.jpg")
character_q_skills.add_posi(img_path=f"{ASSETS_COMMON_IMG}\\area\\QSkill\\c2.jpg")
character_q_skills.add_posi(img_path=f"{ASSETS_COMMON_IMG}\\area\\QSkill\\c3.jpg")
character_q_skills.add_posi(img_path=f"{ASSETS_COMMON_IMG}\\area\\QSkill\\c4.jpg")
ButtonEgg = Button(path=f"{ASSETS_COMMON_IMG}\\button\\Foods\\ButtonEgg.jpg", cap_posi='all', is_bbg = False)
confirm = Button(path=f"{ASSETS_IMG}\\{GLOBAL_LANG}\\confirm.jpg", cap_posi='all', is_bbg = False)
Area_revival_foods = posi_manager.PosiTemplate(img_path=f"{ASSETS_COMMON_IMG}\\area\\revival_foods.jpg")
ButtonSwitchDomainModeOn = Button(path=f"{ASSETS_IMG}\\map\\big_map\\switch_domain_mode_on.jpg",threshold=0.97)
ButtonSwitchDomainModeOff = Button(path=f"{ASSETS_IMG}\\map\\big_map\\switch_domain_mode_off.jpg",threshold=0.97)
SwitchMapArea = posi_manager.PosiTemplate(img_path=f"{ASSETS_COMMON_IMG}\\area\\SwitchMapArea.jpg")
SwitchMapAreaButton = Button(f"{ASSETS_COMMON_IMG}\\button\\SwitchMapAreaButton.jpg")
BigMapScaling = ImgIcon(f"{ASSETS_COMMON_IMG}\\ui\\BigMapScaling.jpg", threshold=0.98, print_log = LOG_ALL, offset=0)
CloseMarkTableInTP = Button(f"{ASSETS_COMMON_IMG}\\button\\CloseMarkTableInTP.jpg")
BloodBar = posi_manager.PosiTemplate(img_path = f"{ASSETS_COMMON_IMG}\\area\\BloodBar.jpg")
CharacterName1 = posi_manager.PosiTemplate(img_path = f"{ASSETS_COMMON_IMG}\\area\\CharacterName1.jpg")
CharacterName2 = posi_manager.PosiTemplate(img_path = f"{ASSETS_COMMON_IMG}\\area\\CharacterName2.jpg")
CharacterName3 = posi_manager.PosiTemplate(img_path = f"{ASSETS_COMMON_IMG}\\area\\CharacterName3.jpg")
CharacterName4 = posi_manager.PosiTemplate(img_path = f"{ASSETS_COMMON_IMG}\\area\\CharacterName4.jpg")
TeamCharactersName = posi_manager.PosiTemplate()
ConfigureTeam = Button()
GoToFight = Button()
SwitchTeamLeft = Button(threshold=0)
SwitchTeamRight = Button(threshold=0)
UIConfigureTeam = ImgIcon()
PartySetupCharaName1=posi_manager.PosiTemplate()
PartySetupCharaName2=posi_manager.PosiTemplate()
PartySetupCharaName3=posi_manager.PosiTemplate()
PartySetupCharaName4=posi_manager.PosiTemplate()
CommissionIcon = ImgIcon(path=fr"{ROOT_PATH}\assets\imgs\Windows\map\big_map\points\commission.jpg")
AreaSidebarCommissionName = PosiTemplate()
SidebarIsCommissionExist = ImgIcon()

QTSX = TextTemplate(text=
{
    "zh_CN":"七天神像",
    "en_US":"Statues of The Seven"
}, cap_area = BigmapChooseArea.position)
CSMD = TextTemplate(text=
{
    "zh_CN":"传送锚点",
    "en_US": "Teleport Waypoint"
}, cap_area = BigmapChooseArea.position)
ASmallStepForHilichurls = TextTemplate(text={"zh_CN":"丘丘人的一小步", "en_US": "A small step for hilichurls"})
IncreasingDanger = TextTemplate(text={"zh_CN":"攀高危险", "en_US": "Increasing danger"})
Emergency = TextTemplate(text={"zh_CN":"临危受命", "en_US": "Emergency"})
IcyIssues = TextTemplate(text={"zh_CN":"冷冰冰的大麻烦", "en_US": "Icy Issues"})
ForTheHarbingers = TextTemplate(text={"zh_CN":"为了执行官大人", "en_US": "For The Harbingers"})
MapAreaMD = TextTemplate(text={
    "zh_CN":"蒙德"
}, cap_area = SwitchMapArea.position)
MapAreaLY = TextTemplate(text={
    "zh_CN":"璃月"
}, cap_area = SwitchMapArea.position)
MapAreaDQ = TextTemplate(text={
    "zh_CN":"稻妻"
}, cap_area = SwitchMapArea.position)
MapAreaXM = TextTemplate(text={
    "zh_CN":"须弥"
}, cap_area = SwitchMapArea.position)
MapAreaCYJY = TextTemplate(text={
    "zh_CN":"层岩巨渊"
}, cap_area = SwitchMapArea.position)

if __name__ == '__main__':
    ConfigureTeam.show_image()