import logger
from source.util import *
from source.common.timer_module import *
from source.funclib import generic_lib, movement
from source.interaction.interaction_core import itt
from source.pickup.pickup_operator import PickupOperator
from source.funclib.err_code_lib import ERR_PASS, ERR_STUCK
from source.map.map import genshin_map
from source.flow.utils.flow_template import FlowConnector, FlowController, FlowTemplate, EndFlowTemplate
from source.flow.utils import flow_state as ST
from source.flow.utils import flow_code as FC
from source.ui.ui import ui_control
import source.ui.page as UIPage
from source.map.tianli_navigator import TianliNavigator
from source.funclib import combat_lib
from source.flow.utils.cvars import *
from source.teyvat_move.teyvat_move_optimizer import B_SplineCurve_GuidingHead_Optimizer
from source.funclib.combat_lib import CSDL
from source.combat.switch_character_operator import SwitchCharacterOperator, SHIELD
from multiprocessing import Process


class TeyvatMoveFlowConnector(FlowConnector):
    def __init__(self):
        super().__init__()
        self.checkup_stop_func = None
        self.stop_rule = 0
        self.target_posi = [0, 0]
        self.reaction_to_enemy = 'RUN'
        self.MODE = "PATH"
        self.path_dict = {}
        self.to_next_posi_offset = 6  # For precision
        self.skip_move_rotation_offset = self.to_next_posi_offset / 2
        self.special_keys_posi_offset = 3
        self.is_tp = False
        self.tp_type = None
        self.ignore_space = True
        self.is_reinit = True
        self.is_precise_arrival = False
        self.stop_offset = None
        self.is_tianli_navigation = True
        self.is_auto_pickup = False
        self.is_use_shield = True
        self.PUO = PickupOperator()
        self.SCO = SwitchCharacterOperator()
        self.is_nahida = None


        self.motion_state = IN_MOVE
        self.jump_timer = Timer()
        self.current_state = ST.INIT_TEYVAT_TELEPORT

        self.priority_waypoints = load_json("priority_waypoints.json", folder_path='assets')
        self.priority_waypoints_array = []
        for i in self.priority_waypoints:
            self.priority_waypoints_array.append(i["position"])
        self.priority_waypoints_array = np.array(self.priority_waypoints_array)

    def reset(self):
        self.stop_rule = STOP_RULE_ARRIVE
        self.target_posi = [0, 0]
        self.reaction_to_enemy = 'RUN'
        self.MODE = "PATH"
        self.path_dict = {}
        self.to_next_posi_offset = 6  # For precision
        self.skip_move_rotation_offset = self.to_next_posi_offset / 2
        self.special_keys_posi_offset = 3
        self.is_tp = False
        self.tp_type = None
        self.ignore_space = True
        self.is_reinit = True
        self.is_precise_arrival = False
        self.stop_offset = None
        self.is_tianli_navigation = True
        self.is_auto_pickup = False

        self.motion_state = IN_MOVE
        self.jump_timer = Timer()
        self.current_state = ST.INIT_TEYVAT_TELEPORT


class TeyvatTeleport(FlowTemplate):
    def __init__(self, upper: TeyvatMoveFlowConnector):
        super().__init__(upper, flow_id=ST.INIT_TEYVAT_TELEPORT, next_flow_id=ST.INIT_TEYVAT_MOVE)
        self.upper = upper

    def state_init(self):
        if not self.upper.is_tp:
            self._set_rfc(FC.END)
        else:
            self._next_rfc()

    def state_before(self):
        ui_control.ui_goto(UIPage.page_main)
        self._next_rfc()

    def state_in(self):
        genshin_map.bigmap_tp(self.upper.target_posi, tp_type=self.upper.tp_type, csf=self.upper.checkup_stop_func)
        self._next_rfc()

    def state_end(self):
        ui_control.ui_goto(UIPage.page_main)
        return super().state_end()

from source.common.base_threading import AdvanceThreading
class MoveController(AdvanceThreading):
    def __init__(self):
        super().__init__()
        self.while_sleep = 0
        self.move_ahead_timer = AdvanceTimer(1).start()
        self.w_pressed = False

    def move_ahead(self, duration: float = 1):
        self.move_ahead_timer = AdvanceTimer(duration).start()
        itt.key_down('w')

    def switch_w(self, mode = 'all', sleep=True):
        # logger.trace('mc switching')
        if self.move_ahead_timer.reached():
            if mode in ['all', 'stop']:
                if self.w_pressed:
                    itt.key_up('w')
                    self.w_pressed = False
                if sleep:
                    time.sleep(0.05)
        else:
            if mode in ['all', 'start']:
                itt.key_down('w')
                self.w_pressed = True
                self.move_ahead_timer.wait(additional_time=-0.15)

    def stop_move_ahead(self):
        self.move_ahead_timer = AdvanceTimer(0).start()
        itt.key_up('w')

    def loop(self):
        self.switch_w()

class TeyvatMoveCommon():
    def __init__(self, upper: TeyvatMoveFlowConnector):
        self.motion_state = IN_MOVE
        self.jil = movement.JumpInLoop(2)
        self.jump_timer3 = Timer()
        self.history_position = []
        self.history_position_timer = AdvanceTimer(limit=1).start()
        self.last_w_position = [0, 0]
        self.press_w_timer = AdvanceTimer(limit=1).start()
        self.upper = upper
        self.mc = MoveController()
        self.offset_timer = Timer()
        self.offset_timer_flag = False




    def switch_motion_state(self, jump=True):
        self.motion_state = movement.get_current_motion_state()
        # if itt.get_img_existence(asset.IconGeneralMotionClimbing):
        #     self.motion_state = IN_CLIMB
        # elif itt.get_img_existence(asset.IconGeneralMotionFlying):
        #     self.motion_state = IN_FLY
        # elif itt.get_img_existence(asset.IconGeneralMotionSwimming):
        #     self.motion_state = IN_WATER
        # else:
        #     self.motion_state = IN_MOVE
        if self.motion_state == IN_CLIMB:
            jump_dt = 20
        elif self.motion_state == IN_MOVE:
            jump_dt = 1.6
        else:
            jump_dt = 99999
        if jump:
            self.jil.jump_in_loop(jump_dt=jump_dt)

    def try_fly(self):
        if self.motion_state == IN_MOVE:
            if self.jump_timer3.get_diff_time() >= 0.3:
                itt.key_press('spacebar')
                self.jump_timer3.reset()

    def is_stuck(self, posi, threshold=40):
        if self.history_position_timer.reached_and_reset():
            self.history_position.append(posi)
        if len(self.history_position) >= threshold:
            if euclidean_distance(self.history_position[-threshold + 1], self.history_position[-1]) <= 10:
                logger.warning(f"MOVE STUCK")
                return True
        return False

    def auto_w(self, curr_posi):
        if self.press_w_timer.reached_and_reset():
            if list(self.last_w_position) == list(curr_posi):
                logger.info(f"position duplication, press w")
                itt.key_press('w')

    def detect_stop_rule(self, stop_rule, is_precise_arrival, target_posi, curr_posi, stop_offset):
        if stop_rule == STOP_RULE_ARRIVE:
            if is_precise_arrival:
                threshold = 1
            else:
                threshold = 6
            if euclidean_distance(target_posi, curr_posi) <= threshold:
                logger.info(t2t("已到达目的地附近，本次导航结束。"))
                itt.key_up('w')
                return True
        elif stop_rule == STOP_RULE_F:
            if stop_offset is None:
                # TODO: fine tuning it
                threshold = 50
            else:
                threshold = stop_offset
            if euclidean_distance(target_posi, curr_posi) <= threshold:
                if generic_lib.f_recognition():
                    itt.key_up('w')
                    itt.delay('2animation')
                    if generic_lib.f_recognition():
                        logger.info(t2t("已到达F附近，本次导航结束。"))
                        return True
                    else:
                        logger.info(f"fake f")
                        itt.key_down('w')
        elif stop_rule == STOP_RULE_COMBAT:
            if stop_offset is None:
                threshold = 25
            else:
                threshold = stop_offset
            if euclidean_distance(target_posi, curr_posi) <= threshold:
                if combat_lib.CSDL.get_combat_state():
                    logger.info(t2t("准备打架，本次导航结束。"))
                    itt.key_up('w')
                    return True
        return False

    def use_shield_if_needed(self):
        if self.upper.is_use_shield:
            if self.motion_state == IN_MOVE and CSDL.get_combat_state():
                self.upper.SCO.continue_threading()
                # self.upper.SCO.switch_character(SHIELD)
            else:
                self.upper.SCO.pause_threading()

    def start_shield_if_needed(self):
        if self.upper.is_use_shield:
            self.upper.SCO.mode = SHIELD
            self.upper.SCO.start_threading()

    def move_ahead(self, duration: float = 1):
        self.mc.move_ahead(duration=duration)

    def switch_w(self, mode = 'all'):
        if self.mc.pause_threading_flag:
            self.mc.continue_threading()

    def stop_move_ahead(self):
        self.mc.stop_move_ahead()

    OFFSET_PRE_SECOND = 0.2
    MIN_OFFSET_APPEND_TIME = 1.5

    def _get_offset(self, diff:float, max_offset=6, min_offset=2):
        offset = min_offset
        if diff < max_offset:
            if not self.offset_timer_flag:
                self.offset_timer_flag = True
                self.offset_timer = Timer()

            dt = self.offset_timer.get_diff_time()
            if dt > self.MIN_OFFSET_APPEND_TIME:
                offset = min_offset + (dt-self.MIN_OFFSET_APPEND_TIME)*self.OFFSET_PRE_SECOND
                logger.trace(f'{offset} = {min_offset} + {dt} - {self.MIN_OFFSET_APPEND_TIME}*{self.OFFSET_PRE_SECOND}')
                return offset
            else:
                return offset
        else:
            self.offset_timer_flag = False
            return offset
class Navigation(TianliNavigator):
    def __init__(self, start, end) -> None:
        super().__init__()
        # 千万不要对这里的列表的顺序进行修改！！！
        self._curr_posi = [0, 0]
        self.all_navigation_posi = [p[1].position for p in self.NAVIGATION_POINTS.items()]  # READ ONLY
        self.navigation_path = []
        self.init_path(start, end)

    def _get_closest_node(self, position, threshold=150):
        plist = quick_euclidean_distance_plist(position, self.all_navigation_posi)
        min_index = np.argmin(plist)
        if euclidean_distance(self.all_navigation_posi[min_index], position) > threshold:
            return None
        else:
            return list(self.NAVIGATION_POINTS.items())[min_index][1]

    def init_path(self, start, end):
        start_node = self._get_closest_node(start)
        end_node = self._get_closest_node(end)
        if start_node != None and end_node != None:
            self.navigation_path = list(self.astar(start_node, end_node))
            if len(self.navigation_path) == 0:
                logger.debug(f"未找到路径")
                self.navigation_path = None
            else:
                logger.debug(f"navigation_path: {list(map(str, self.navigation_path))}")
        else:
            logger.debug(t2t("不在服务区"))
            self.navigation_path = None

    def set_curr_posi(self, posi):
        self._curr_posi = posi

    def get_navigation_positions(self, end_p):
        if self.navigation_path is None:
            return [end_p]
        else:
            return [i.position for i in self.navigation_path]

    def get_navigation_info(self, i):
        if self.navigation_path is None: return None
        if i >= len(self.navigation_path):
            return f""
        return f"{self.navigation_path[i]}"

    def print_TLPS_info(self, i, cp, speak=False):
        if self.navigation_path is None: return None
        r = self.get_navigation_info(i)
        if r != '':
            output_id = r
            output_distance = euclidean_distance(cp, self.navigation_path[i].position)
            output_remaining_navigation = f"{i + 1} in {len(self.navigation_path)}"
            # logger.info(f"TianLi Positioning System")
            logger.info(f"Moving to Navigation {output_id}")
            logger.info(f"Distance: {output_distance}")
            logger.info(f"Remaining navigation: {output_remaining_navigation}")


class TeyvatMove_Automatic(FlowTemplate, TeyvatMoveCommon, Navigation):
    def __init__(self, upper: TeyvatMoveFlowConnector):
        FlowTemplate.__init__(self, upper, flow_id=ST.INIT_TEYVAT_MOVE, next_flow_id=ST.END_TEYVAT_MOVE_PASS)
        TeyvatMoveCommon.__init__(self, upper=upper)
        Navigation.__init__(self, genshin_map.get_position(), self.upper.target_posi)
        self.upper = upper
        self.auto_move_timeout = AdvanceTimer(limit=300).start()
        self.in_flag = False
        self.posi_list = []
        self.posi_index = 0

    # def _calculate_next_priority_point(self, currentp, targetp):
    #     float_distance = 35
    #     # 计算当前点到所有优先点的曼哈顿距离
    #     md = manhattan_distance_plist(currentp, self.upper.priority_waypoints_array)
    #     nearly_pp_arg = np.argsort(md)
    #     # 计算当前点到距离最近的50个优先点的欧拉距离
    #     nearly_pp = self.upper.priority_waypoints_array[nearly_pp_arg[:50]]
    #     ed = euclidean_distance_plist(currentp, nearly_pp)
    #     # 将点按欧拉距离升序排序
    #     nearly_pp_arg = np.argsort(ed)
    #     nearly_pp = nearly_pp[nearly_pp_arg]
    #     # 删除距离目标比现在更远的点
    #     fd = euclidean_distance_plist(targetp, nearly_pp)
    #     c2t_distance = euclidean_distance(currentp, targetp)
    #     nearly_pp = np.delete(nearly_pp, (np.where(fd+float_distance >= (c2t_distance) )[0]), axis=0)
    #     # 获得最近点
    #     if len(nearly_pp) == 0:
    #         return targetp
    #     closest_pp = nearly_pp[0]
    #     '''加一个信息输出'''
    #     # print(currentp, closest_pp)
    #     return closest_pp

    def state_before(self):
        genshin_map.reinit_smallmap()
        self.auto_move_timeout.reset()
        self.history_position_timer.reset()
        self.history_position = []
        self.upper.while_sleep = 0.05
        self.in_flag = False
        self.current_posi = genshin_map.get_position()
        if self.upper.is_tianli_navigation:
            self.init_path(self.current_posi, self.upper.target_posi)
            self.posi_list = self.get_navigation_positions(self.upper.target_posi)
            self.posi_list.append(self.upper.target_posi)
            if euclidean_distance(self.posi_list[0], self.upper.target_posi) > euclidean_distance(self.current_posi,
                                                                                                  self.upper.target_posi):
                logger.info(f"the distance to target is closer than TLPS, give up using TLPS.")
                self.posi_list = [self.upper.target_posi]
        else:
            self.posi_list = [self.upper.target_posi]

        self.start_shield_if_needed()

        self._next_rfc()

    def state_in(self):
        self.current_posi = genshin_map.get_position()
        distance = euclidean_distance(self.current_posi, self.upper.target_posi)
        if distance <= 8:
            self.switch_motion_state(jump=False)
        else:
            self.switch_motion_state(jump=True)

        # p1 = self.upper.target_posi

        if self.is_stuck(self.current_posi, threshold=60):
            self._set_nfid(ST.END_TEYVAT_MOVE_STUCK)
            self._set_rfc(FC.END)

        # print(p1)
        if movement.move_to_posi_LoopMode(self.posi_list[self.posi_index], self.upper.checkup_stop_func):
            self.posi_index += 1
            self.posi_index = min(len(self.posi_list) - 1, self.posi_index)
            if self.upper.is_tianli_navigation:
                self.print_TLPS_info(self.posi_index, self.current_posi)
        # movement.change_view_to_posi(p1, self.upper.checkup_stop_func)
        # if not self.in_flag:
        #     itt.key_down('w')
        #     self.in_flag = True

        r = self.detect_stop_rule(self.upper.stop_rule, self.upper.is_precise_arrival, self.upper.target_posi,
                                  self.current_posi, self.upper.stop_offset)
        if r:
            self._next_rfc()
            return

        self.use_shield_if_needed()

        move_duration = min(distance * 0.08, 0.8)
        logger.trace(f'Move Automatic: Duration: {move_duration}')
        self.move_ahead(duration=move_duration)

        # if len(genshin_map.history_posi) >= 29:
        #     p1 = genshin_map.history_posi[0][1:]
        #     p2 = genshin_map.history_posi[-1][1:]
        #     if euclidean_distance(p1,p2)<=30:
        #         logger.warning("检测到移动卡住，正在退出")
        #         self._set_nfid(ST.END_TEYVAT_MOVE_STUCK)
        #         self._next_rfc()

    def state_after(self):
        self.upper.while_sleep = 1
        self.switch_motion_state(jump=False)
        if self.motion_state == IN_FLY:
            logger.info(f"landing")
            itt.left_click()
        self.mc.pause_threading()
        self._next_rfc()




class TeyvatMove_FollowPath(FlowTemplate, TeyvatMoveCommon):
    """_summary_

    Args:
        FlowTemplate (_type_): _description_
        TeyvatMoveCommon (_type_): _description_

    BP: break point. 程序行走使用的点。
    CP: current point. 执行SK，切换Motion使用的点。
    """

    is_nahida = False
    ENABLE_OPTIMIZER = True
    last_adsorptive_position = [10000000, 10000000]

    def __init__(self, upper: TeyvatMoveFlowConnector):
        FlowTemplate.__init__(self, upper, flow_id=ST.INIT_TEYVAT_MOVE, next_flow_id=ST.END_TEYVAT_MOVE_PASS)
        TeyvatMoveCommon.__init__(self, upper=upper)

        self.upper = upper
        self.curr_path_index = 0
        self.last_ten_index = 0
        self.special_key_points = None

        self.curr_path = []
        self.curr_break_point_index = 0
        self.last_ten_posi = []
        self.last_ten_delta = []

        self.ready_to_end = False
        self.end_times = 0
        self.init_start = False

        self.landing_timer = Timer(2)
        self.sprint_timer = AdvanceTimer(2.5).reset()
        if not DEBUG_MODE:
            self.in_pt = Performance(output_cycle=25)
        else:
            self.in_pt = Performance(output_cycle=1)

    def predict_tdo_degree(self, curr_posi, target_posi):
        nx, ny, nz = self.TDO.predict_nearest_point(curr_posi[0], curr_posi[1], self.curr_break_point_index)
        nz = max(0, nz)
        dx, dy, dz = self.TDO.predict_gradient(nz)
        if DEBUG_MODE:
            print('tdo: nearest point:', nx, ny, nz)
            print('tdo: nearest point gradient:', dx, dy, dz)
        tdo_final_degree = generic_lib.points_angle([0, 0], [dx, dy], coordinate=generic_lib.NEGATIVE_Y)
        final_rate = round(euclidean_distance(curr_posi, [nx, ny]), 2)
        if final_rate >= 15:
            movement.move_to_position([nx, ny])
            # tdo_final_degree = generic_lib.points_angle(curr_posi, [nx,ny], coordinate=generic_lib.NEGATIVE_Y)
        else:
            final_rate = final_rate / 30
        tdo_final_degree = add_angle(tdo_final_degree, generic_lib.points_angle(curr_posi, [nx, ny],
                                                                                coordinate=generic_lib.NEGATIVE_Y) * final_rate)
        if DEBUG_MODE:
            print(f"tdo: degree: {generic_lib.points_angle([0, 0], [dx, dy], coordinate=generic_lib.NEGATIVE_Y)}"
                  "\n"
                  f"target posi degree: {generic_lib.points_angle(curr_posi, target_posi, coordinate=generic_lib.NEGATIVE_Y)}"
                  "\n"
                  f"tdo distance: {round(euclidean_distance(curr_posi, [nx, ny]), 2)}"
                  "\n"
                  f"tdo final rate: {final_rate}"
                  "\n"
                  f"tdo final degree: {tdo_final_degree}"
                  )
        self.curr_break_point_index = int(nz)
        return tdo_final_degree

    def _low8up9(self, x):
        decimals = math.modf(x)[0]
        if decimals >= 0.9:
            return math.ceil(x)
        else:
            return math.floor(x)

    def predict_tdo_position(self, curr_posi, target_posi):
        nx, ny, nz = self.TDO.predict_nearest_point(curr_posi[0], curr_posi[1], self.curr_break_point_index)
        nz = max(0, nz)
        r_posi = self.TDO.predict_guiding_head_position(nz)
        if DEBUG_MODE:
            logger.trace(
                "\n"
                f"curr posi: {curr_posi}"
                "\n"
                f"target posi: {target_posi}"
                "\n"
                f"guiding head posi: {r_posi}"
                "\n"
                f"nz: {nz}"
                "\n"
                f"bp_index: {self.curr_break_point_index}"
            )
        self.curr_break_point_index = int(self._low8up9(nz))
        if self.curr_break_point_index > len(self.curr_breaks) - 1:
            logger.info('index out of range')
            self.curr_break_point_index = len(self.curr_breaks) - 1
        return r_posi

    def _exec_special_key(self, special_key):
        """Not In Use

        Args:
            special_key (_type_): _description_
        """
        # key_name = special_key

        itt.key_press(special_key)
        logger.info(f"key {special_key} exec.")

    # @timer
    def _refresh_curr_posi_index(self, curr_posi):
        posi_list = []
        for i in self.upper.path_dict["position_list"][
                 self.curr_path_index:min(self.curr_path_index + 10, len(self.upper.path_dict["position_list"]) - 1)
                 ]:
            posi_list.append(i["position"])
        if not len(posi_list) == 0:
            self.curr_path_index += np.argmin(euclidean_distance_plist(curr_posi, posi_list))
        else:
            self.curr_path_index = 0

    def state_before(self):
        self.curr_path = self.upper.path_dict["position_list"]
        self.curr_breaks = self.upper.path_dict["break_position"]
        if 'adsorptive_position' in self.upper.path_dict:
            self.adsorptive_position = self.upper.path_dict["adsorptive_position"]
        else:
            self.adsorptive_position = []
        if "additional_info" in self.upper.path_dict.keys():
            self.additional_info = self.upper.path_dict["additional_info"]
        else:
            self.additional_info = {}
        self.ready_to_end = False
        self.init_start = False
        self.curr_path_index = 0
        self.curr_break_point_index = 0
        self.end_times = 0
        # itt.key_down('w')
        if self.upper.is_reinit:
            genshin_map.reinit_smallmap()
        self.upper.while_sleep = 0

        if self.upper.is_auto_pickup:
            self.upper.PUO.continue_threading()

        if self.upper.is_nahida is None:
            self.is_nahida = 'Nahida' in combat_lib.get_characters_name()
        else:
            self.is_nahida = self.upper.is_nahida

        if 'kyt2m_version' in self.additional_info.keys():
            self.curr_break_point_index = 1
            self.ENABLE_OPTIMIZER = False
        else:
            self.ENABLE_OPTIMIZER = True

        if len(self.curr_breaks) < 6:
            logger.info('bp too little, disable optimizer.')
            self.ENABLE_OPTIMIZER = False
        if 'generate_from' in self.upper.path_dict.keys():
            if self.upper.path_dict['generate_from'] == 'path recorder 1.0':
                self.ENABLE_OPTIMIZER = False

        if self.ENABLE_OPTIMIZER:
            self.TDO = B_SplineCurve_GuidingHead_Optimizer(self.upper.path_dict)

        self.start_shield_if_needed()
        self.mc.start_threading()
        self._next_rfc()

    def _land(self, enforce=False):
        retry_timer = AdvanceTimer(10)
        if self.landing_timer.get_diff_time() > 2 or enforce:
            if self.landing_timer.get_diff_time() < 5 or enforce:
                logger.info("landing")
                itt.key_press('x')
                itt.left_click()
                retry_timer.reset()
                while 1:
                    if self.upper.checkup_stop_func():
                        break
                    self.switch_motion_state()
                    if (self.motion_state != IN_FLY) and (self.motion_state != IN_CLIMB):
                        break
                    time.sleep(0.1)

                    if retry_timer.reached_and_reset():
                        itt.key_press('x')
                        itt.left_click()
            else:
                self.landing_timer.reset()

    climb_until_walk_to_ads_flag = False
    delay_ads = False
    switch_bp_flag = False
    switch_bp_flag_for_ads = False

    # any_jump_timer = AdvanceTimer()




    def state_in(self):
        print(f"re in cost {self.in_pt.get_diff_time()}")
        self.switch_w(mode='stop')
        self.in_pt.reset()
        # print(f"time0: {self.in_pt.get_diff_time()}")
        # 如果循环太慢而走的太快就会回头 可能通过量化移动时间和距离解决

        # 更新BP和CP
        while 1:
            # print(f"time0.1: {self.in_pt.get_diff_time()}")
            target_posi = self.curr_breaks[self.curr_break_point_index]
            curr_posi = genshin_map.get_position()

            # 刷新当前position index
            self._refresh_curr_posi_index(list(curr_posi))
            # special_key = self.curr_path[self.curr_path_index]["special_key"]
            # if self.upper.ignore_space and special_key == "space": # ignore space
            #     special_key = None
            # if special_key is None: # 设定offset
            #     offset = 6 # NO SK
            # else:
            #     offset = 6 # SK
            offset = 2
            if self.curr_path[self.curr_path_index]["motion"] == "FLYING":
                offset = 12
            elif self.motion_state == SWIMMING:
                offset = 8
            if "additional_info" in self.upper.path_dict.keys():
                if "pickup_points" in self.upper.path_dict["additional_info"].keys():
                    if self.curr_break_point_index in self.upper.path_dict["additional_info"]["pickup_points"]:
                        logger.debug('bp is pp, o=3.5.')
                        offset = 2
            if self.ready_to_end:
                offset = 1 # min(1, max(1, (self.end_times) / 10))

            # 如果两个BP距离小于offset就会瞬移，排除一下。
            if self.curr_break_point_index < len(self.curr_breaks) - 1:
                dist = euclidean_distance(self.curr_breaks[self.curr_break_point_index],
                                          self.curr_breaks[self.curr_break_point_index + 1])
                if dist <= offset:
                    logger.trace(f"BPs too close: dist: {dist}")
                    offset = dist / 2
                    logger.trace(f"offset: {offset}")

            offset = self._get_offset(diff=euclidean_distance(target_posi, curr_posi), max_offset=6, min_offset=offset)
            logger.trace(f"offset: {offset}")
            # print(f"time0.2: {self.in_pt.get_diff_time()}")

            # 执行SK
            # if special_key != None: 
            #     self._exec_special_key(special_key)
            # 检测是否要切换到下一个BP
            # TODO: 好丑，能重构吗[・ヘ・?]
            if not self.ENABLE_OPTIMIZER:
                if euclidean_distance(target_posi, curr_posi) <= offset:
                    if len(self.curr_breaks) - 1 > self.curr_break_point_index:
                        # if not self.curr_break_point_index == 0:
                        #     self.switch_bp_flag_for_ads = True
                        self.curr_break_point_index += 1  # BP+1
                        logger.debug(
                            f"index {self.curr_break_point_index} posi {self.curr_breaks[self.curr_break_point_index]}")
                        # pass
                    elif not self.ready_to_end:
                        if self.upper.is_precise_arrival:
                            logger.info("path ready to end")
                            self.ready_to_end = True
                            break
                        else:
                            logger.info("path end")
                            self._next_rfc()
                            itt.key_up('w')
                            return
                    else:
                        logger.info("path end")
                        self._next_rfc()
                        itt.key_up('w')
                        return
                else:
                    break
            else:
                if euclidean_distance(target_posi, curr_posi) <= offset:
                    if not len(self.curr_breaks) - 1 > self.curr_break_point_index:
                        if not self.ready_to_end:
                            if self.upper.is_precise_arrival:
                                logger.info("path ready to end")
                                self.ready_to_end = True
                                break
                            else:
                                logger.info("path end")
                                self._next_rfc()
                                itt.key_up('w')
                                return
                        else:
                            logger.info("path end")
                            self._next_rfc()
                            itt.key_up('w')
                            return
                    else:
                        break
                else:
                    break

            # print(f"time0.3: {self.in_pt.get_diff_time()}")

        logger.trace(f"time: refresh bp: {self.in_pt.get_diff_time()}")

        # 动作识别
        is_jump = False
        is_nearby = euclidean_distance(curr_posi, target_posi) < 2
        check_jump = self.curr_path[self.curr_path_index:min(self.curr_path_index + 5, len(self.curr_path) - 1)]  # 起跳
        for i in check_jump:
            if 'special_key' in i:
                if i["special_key"] == "space":
                    is_jump = True

        self.switch_motion_state(jump=((not self.ready_to_end) and is_jump))
        fly_flag = False
        check_fly = self.curr_path[self.curr_path_index:min(self.curr_path_index + 10, len(self.curr_path) - 1)]  # 起飞
        for i in check_fly:
            if i["motion"] == "FLYING":
                self.try_fly()
                fly_flag = True

        if self.motion_state == IN_FLY and self.curr_path[self.curr_path_index]["motion"] == "WALKING" and (not fly_flag):  # 降落
            self._land()
            # if self.landing_timer.get_diff_time()>2:
            #     if self.landing_timer.get_diff_time()<5:
            #         logger.info("landing")
            #         itt.left_click()
            #         while 1:
            #             if self.upper.checkup_stop_func():
            #                 break
            #             self.switch_motion_state()
            #             time.sleep(0.1)
            #             if self.motion_state != IN_FLY:
            #                 break
            #     else:
            #         self.landing_timer.reset()

        if self.curr_path[self.curr_path_index]["motion"] == "ANY":
            movement.jump_in_loop()

        logger.trace(f"time2: switch motion: {self.in_pt.get_diff_time()}")

        def is_ads(threshold):
            return min(euclidean_distance_plist(curr_posi, self.adsorptive_position)) < threshold

        # 吸附模式: 当当前距离小于允许吸附距离，开始向目标吸附点移动
        if len(self.adsorptive_position) > 0:
            adsorptive_threshold = 10
            if is_ads(adsorptive_threshold):
                if self.motion_state == IN_FLY:
                    self._land()
                if self.motion_state == IN_CLIMB:
                    logger.info('climb_until_walk_to_ads_flag: True')
                    self.climb_until_walk_to_ads_flag = True
                    if 'is_cliff_collection' in self.additional_info.keys():
                        if self.additional_info['is_cliff_collection']:
                            self._land()
                            itt.delay(0.5)
                if self.motion_state == IN_MOVE:
                    self._exec_ads(curr_posi, adsorptive_threshold)

        # self._exec_active_pickup()
        curr_posi = genshin_map.get_position()

        logger.trace(f"time3: check absorptive position {self.in_pt.get_diff_time()}")

        # 自动拾取
        if self.upper.is_auto_pickup:
            if generic_lib.f_recognition():
                while self.upper.PUO.pickup_recognize(): pass
                curr_posi = genshin_map.get_position()

        logger.trace(f"time4.1:  {self.in_pt.get_diff_time()}")

        # 检测移动是否卡住
        if self.is_stuck(curr_posi, threshold=10):
            if self.motion_state == WALKING:
                logger.debug(f"move stuck, try jumping")
                itt.key_press('spacebar')
        if self.is_stuck(curr_posi, threshold=45):
            itt.key_press('spacebar')
        elif self.is_stuck(curr_posi, threshold=60):
            self._set_nfid(ST.END_TEYVAT_MOVE_STUCK)
            self._set_rfc(FC.END)

        # 是否准备结束
        if self.ready_to_end:
            self.end_times += 1
            logger.debug(f"ready to end: {self.end_times} {offset}")
        if self.end_times >= 80:
            logger.warning(f"TMF PATH FAIL: CANNOT APPROACH TO END POSITION")
            self._set_nfid(ST.END_TEYVAT_MOVE_STUCK)
            self._set_rfc(FC.END)

        logger.trace(f"time4.2:  {self.in_pt.get_diff_time()}")

        r = self.detect_stop_rule(self.upper.stop_rule, self.upper.is_precise_arrival,
                                  self.upper.path_dict["end_position"], curr_posi, self.upper.stop_offset)
        if r:
            self._next_rfc()

        logger.trace(f"time4.3:  {self.in_pt.get_diff_time()}")

        self.use_shield_if_needed()

        logger.trace(f"time4: pickup, stuck checks, shield and ready_to_end check: {self.in_pt.get_diff_time()}")

        # 输出日志
        distance = euclidean_distance(target_posi, curr_posi)
        move_duration =  min(distance*0.05 , 0.8)  # estimate loop time: 0.1s estimate move speed: 10m/s when walking
        logger.trace(f"move_duration: {move_duration}")
        logger.debug(f"next break position distance: {distance}")

        # delta_distance = self.CalculateTheDistanceBetweenTheAngleExtensionLineAndTheTarget(curr_posi,target_posi)

        # 移动视角
        tx, ty = curr_posi[0], curr_posi[1]
        logger.trace(f"time5.1.1: change_view_to_angle:  {self.in_pt.get_diff_time()}")
        if not self.ENABLE_OPTIMIZER:
            target_degree = movement.calculate_posi2degree(target_posi, tx, ty)
        else:
            target_degree = movement.calculate_posi2degree(self.predict_tdo_position(curr_posi, target_posi), tx, ty)
            # target_degree = self.predict_tdo_degree(curr_posi, target_posi)
        delta_degree = abs(movement.calculate_delta_angle(genshin_map.get_rotation(), target_degree))

        def set_move():
            if self.ready_to_end:
                self.move_ahead(duration=move_duration * 0.5)
            else:
                self.move_ahead(duration=move_duration)

        if delta_degree >= 45:
            logger.trace(f"time5.2.1: change_view_to_angle:  {self.in_pt.get_diff_time()}")
            self.stop_move_ahead()
            # movement.change_view_to_posi(target_posi, stop_func = self.upper.checkup_stop_func)
            movement.change_view_to_angle(target_degree, offset=15)
            logger.trace(f"time5.2.2: change_view_to_angle:  {self.in_pt.get_diff_time()}")
        # elif delta_degree >= 10:
        #     # movement.change_view_to_posi(target_posi, stop_func = self.upper.checkup_stop_func, max_loop=4, offset=2, print_log = False)
        #     logger.trace(f"time5.3.1: change_view_to_angle:  {self.in_pt.get_diff_time()}")
        #     movement.change_view_to_angle(target_degree, loop_sleep=0, maxloop=4)
        #     logger.trace(f"time5.3.2: change_view_to_angle:  {self.in_pt.get_diff_time()}")
        else:
            movement.change_view_to_angle(target_degree, loop_sleep=0, maxloop=2, precise_mode=False)
        set_move()



        if self.init_start == False:
            # itt.key_down('w')
            self.init_start = True

        # 冲
        # if self.sprint_timer.reached():
        #     if euclidean_distance(curr_posi, target_posi)>=30:
        #         if self.motion_state == IN_MOVE:
        #             logger.debug(f'sprint {euclidean_distance(curr_posi, target_posi)}')
        #             itt.key_press('left_shift')
        #             self.sprint_timer.reset()

        # w
        # self.auto_w(curr_posi)
        # self.switch_w()

        print(f"time5: a loop cost {self.in_pt.get_diff_time()}")
        self.in_pt.output_log(mess='TMF Path Performance:')

    def state_after(self):
        self.next_flow_id = self.flow_id
        # movement.move_to_position(posi=self.upper.path_dict["end_position"], offset=1,delay=0.01)
        logger.info("path end")
        if self.motion_state == IN_FLY:
            logger.info(f"landing")
            itt.left_click()
        self._exec_active_pickup(force=True)
        self._set_nfid(ST.END_TEYVAT_MOVE_PASS)
        self.upper.while_sleep = 0.2
        if self.upper.is_auto_pickup:
            self.upper.PUO.pause_threading()
        self.mc.pause_threading()
        self._next_rfc()

    def state_end(self):
        itt.key_up('w')
        return super().state_end()

    def _exec_active_pickup(self, force=False):
        if 'is_active_pickup_in_bp' in self.additional_info.keys():
            if self.additional_info['is_active_pickup_in_bp']:
                if self.is_nahida:
                    self._land(enforce=True)
                    self.switch_motion_state()
                    if self.motion_state == WALKING:
                        self.upper.PUO.active_pickup(is_nahida=True)

    def _exec_ads(self, curr_posi, absorptive_threshold):
        for adsorb_p in self.adsorptive_position:
            if euclidean_distance(adsorb_p, curr_posi) < absorptive_threshold:
                logger.info(f"adsorption: {adsorb_p} start")
                if self.upper.is_auto_pickup:
                    pickup_item_num = len(self.upper.PUO.pickup_item_list)
                for i in range(5):
                    if CSDL.get_combat_state():
                        if not self.upper.is_use_shield:
                            break
                    else:
                        self.upper.SCO.pause_threading()
                    if movement.move_to_posi_LoopMode(adsorb_p, self.upper.checkup_stop_func, threshold=0.5): break
                    if self.upper.PUO.auto_pickup() > 0:
                        logger.info("adsorption: finding blink: start")
                        while 1:
                            movement.move(direction=movement.MOVE_AHEAD, distance=1)
                            if self.upper.PUO.auto_pickup() == 0: break
                        logger.info("adsorption: finding blink: end")
                    if self.upper.is_auto_pickup:
                        if self.is_nahida:
                            if euclidean_distance(self.last_adsorptive_position, curr_posi) < 15:
                                logger.info('in nahida mode & scanned once, skip the ads')
                                break
                        if i > 2 and self.is_nahida:
                            self.upper.PUO.active_pickup(is_nahida=True)
                            self.last_adsorptive_position = adsorb_p
                            break
                        if len(self.upper.PUO.pickup_item_list) > pickup_item_num:
                            logger.info('picked, adsorption stopping')
                            break
                    time.sleep(0.2)
                    if i % 5 == 0:
                        logger.debug(f"adsorption: {i}")
                logger.info(f"adsorption: {adsorb_p} end")
                self.use_shield_if_needed()
                # self.climb_until_walk_to_ads_flag = False
                self.adsorptive_position.pop(self.adsorptive_position.index(adsorb_p))
                break


class TeyvatMoveStuck(EndFlowTemplate):
    def __init__(self, upper: FlowConnector):
        super().__init__(upper, flow_id=ST.END_TEYVAT_MOVE_STUCK, err_code_id=ERR_STUCK)


class TeyvatMovePass(EndFlowTemplate):
    def __init__(self, upper: FlowConnector):
        super().__init__(upper, flow_id=ST.END_TEYVAT_MOVE_PASS, err_code_id=ERR_PASS)


class TeyvatMoveFlowController(FlowController):
    def __init__(self):
        flow_connector = TeyvatMoveFlowConnector()
        super().__init__(flow_connector=flow_connector,
                         current_flow_id=ST.INIT_TEYVAT_TELEPORT,
                         flow_name="TeyvatMoveFlow")
        self.flow_connector = flow_connector
        self.get_while_sleep = self.flow_connector.get_while_sleep
        self.append_flow(TeyvatTeleport(self.flow_connector))
        self._add_sub_threading(self.flow_connector.PUO)
        self._add_sub_threading(self.flow_connector.SCO)

    def start_flow(self):
        self.flow_dict = {}
        self.append_flow(TeyvatTeleport(self.flow_connector))
        if self.flow_connector.MODE == "AUTO":
            tma = TeyvatMove_Automatic(self.flow_connector)
            self.append_flow(tma)
            self._add_sub_threading(tma.mc, start=False)
        else:
            tfp = TeyvatMove_FollowPath(self.flow_connector)
            self.append_flow(tfp)
            self._add_sub_threading(tfp.mc, start=False)

        self.append_flow(TeyvatMoveStuck(self.flow_connector))
        self.append_flow(TeyvatMovePass(self.flow_connector))

        if self.flow_connector.is_tp and self.flow_connector.target_posi == [0, 0] and self.flow_connector.MODE == "PATH":
            self.flow_connector.target_posi = self.flow_connector.path_dict["start_position"]

        self.continue_threading()

    def reset(self):
        self.current_flow_id = ST.INIT_TEYVAT_TELEPORT
        self.flow_connector.reset()

    def get_working_statement(self):
        return not self.pause_threading_flag

    def set_target_posi(self, tp: list):
        self.flow_connector.target_posi = tp

    def pause_threading(self):
        if self.pause_threading_flag == False:
            itt.key_up('w')
        return super().pause_threading()

    def set_parameter(self,
                      MODE: str = None,
                      target_posi: list = None,
                      path_dict: dict = None,
                      stop_rule: int = None,
                      is_tp: bool = None,
                      to_next_posi_offset: float = None,
                      special_keys_posi_offset: float = None,
                      reaction_to_enemy: str = None,
                      tp_type: list = None,
                      is_reinit: bool = None,
                      is_precise_arrival: bool = None,
                      stop_offset=None,
                      is_auto_pickup: bool = None,
                      is_use_shield: bool = None,
                      is_nahida: bool=None):
        """设置参数，如果不填则使用上次的设置。

        Args:
            MODE (str, optional): 选择移动模式。可选为“AUTO”自动移动或“PATH”沿路径移动. Defaults to None.\n
            target_posi (list, optional): 目标坐标。TianLi格式. Defaults to None.\n
            path_dict (dict, optional): 路径字典。PATH模式时必填. Defaults to None.\n
            stop_rule (int, optional): 停止条件. Defaults to None.\n
            is_tp (bool, optional): 是否在移动前TP. Defaults to None.\n
            to_next_posi_offset (float, optional): 到下一个posi的offset。一般无需设置. Defaults to None.\n
            special_keys_posi_offset (float, optional): SK的offset。无需设置. Defaults to None.\n
            reaction_to_enemy (str, optional): 对敌反应。无效设置. Defaults to None.\n
            tp_type (list, optional): tp类型。列表可包含`Domain` `Teleporter` `Statue`. Defaults to None.\n
            is_reinit (bool, optional): 是否重初始化TLPS小地图. Defaults to None.\n
            is_precise_arrival (bool, optional): 是否需要准确到达移动终点. Defaults to None.\n
            stop_offset (_type_, optional): 停止范围，小于时停止. Defaults to None.\n
            is_auto_pickup (bool, optional): 是否自动拾取可采集物. Defaults to None.
        """
        if MODE != None:
            self.flow_connector.MODE = MODE
        if stop_rule != None:
            self.flow_connector.stop_rule = stop_rule
        if target_posi != None:
            self.flow_connector.target_posi = target_posi
        if path_dict != None:
            self.flow_connector.path_dict = path_dict
        if to_next_posi_offset != None:
            self.flow_connector.to_next_posi_offset = to_next_posi_offset
        if special_keys_posi_offset != None:
            self.flow_connector.special_keys_posi_offset = special_keys_posi_offset
        if reaction_to_enemy != None:
            self.flow_connector.reaction_to_enemy = reaction_to_enemy
        if is_tp != None:
            self.flow_connector.is_tp = is_tp
        if tp_type != None:
            self.flow_connector.tp_type = tp_type
        if is_reinit != None:
            self.flow_connector.is_reinit = is_reinit
        if is_precise_arrival != None:
            self.flow_connector.is_precise_arrival = is_precise_arrival
        if stop_offset != None:
            self.flow_connector.stop_offset = stop_offset
        if is_auto_pickup != None:
            self.flow_connector.is_auto_pickup = is_auto_pickup
        if is_use_shield != None:
            self.flow_connector.is_use_shield = is_use_shield
        if is_nahida != None:
            self.flow_connector.is_nahida = is_nahida


if __name__ == '__main__':
    # genshin_map.reinit_smallmap()
    # while 1:
    #     time.sleep(0.2)

    #     tx, ty = genshin_map.get_position()
    #     degree = generic_lib.points_angle([tx, ty], [2083, -4844], coordinate=generic_lib.NEGATIVE_Y)
    #     movement.change_view_to_angle(degree, lambda:False)

    TMFC = TeyvatMoveFlowController()
    TMFC.set_parameter(MODE="PATH", path_dict=load_json("QXV220230513090727i0.json", "assets\\TeyvatMovePath"),
                       is_tp=True)
    # TMFC.set_parameter(MODE="AUTO", target_posi=[2032,-4879], is_tp=False)
    TMFC.start_flow()
    TMFC.start()

    while 1:
        time.sleep(1)
