import re

from source.device.alas.exception import RequestHumanTakeover
from source.device.alas.utils import area_offset
from source.device.genshin.base import AppBase, func_debug
from source.device.method.utils import AreaButton
from source.util import logger

# 每日登录奖励的弹窗，每天首次登录奖励15分钟时长
LOGIN_REWARD = '//*[@resource-id="com.miHoYo.cloudgames.ys:id/mTvPopTitle"]'
# 点击任意地方登录
LOGIN_BUTTON = '//*[@resource-id="com.miHoYo.cloudgames.ys:id/btnLogin"]'
# 登录界面，进入游戏按钮
LOGIN_CONFIRM = '//*[@text="进入游戏"]'
# 免费游戏时长
STATUS_FREE = '//*[@resource-id="com.miHoYo.cloudgames.ys:id/tvRemainingFreeTimeNum"]'
# 米云币
STATUS_PAID = '//*[@resource-id="com.miHoYo.cloudgames.ys:id/tvRemainingMiCoinNum"]'
# 开始游戏
GAME_START = '//*[@resource-id="com.miHoYo.cloudgames.ys:id/btnLauncher"]'
# 排队详情
# 目前正排在第 540 / 3295 名，预计等待>10分钟
QUEUE_INFO = '//*[@resource-id="com.miHoYo.cloudgames.ys:id/tvQueueInfo"]'
# 弹窗标题
TITLE = '//*[@resource-id="com.miHoYo.cloudgames.ys:id/titleTv"]'
# 弹窗的确认按钮
CONFIRM = '//*[@resource-id="com.miHoYo.cloudgames.ys:id/confirmTv"]'
# 云原神悬浮窗
FLOAT_WINDOW = '//*[@class="android.widget.ImageView"]'
# 悬浮窗界面，用退出按钮检查
FLOAT_CHECK = '//*[@resource-id="com.miHoYo.cloudgames.ys:id/iv_exit"]'
# 悬浮窗内的延迟
# 将这个区域向右偏移作为退出悬浮窗的按钮
FLOAT_DELAY = '//*[@resource-id="com.miHoYo.cloudgames.ys:id/tv_delay"]'


class CloudGenshin(AppBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config.Emulator_PackageName = 'com.miHoYo.cloudgames.ys'

    @func_debug
    def _cloud_start(self):
        """
        Start genshin cloud and enter main page.

        Pages:
            in: Any
            out: GAME_START
        """
        while 1:
            self.dump_hierarchy()

            if self.appear(GAME_START):
                break

            if self.appear_then_click(LOGIN_REWARD, interval=3):
                continue
            if self.interval_get(TITLE).reached():
                title = self.xpath(TITLE).text
                # 连接中断，长时间未操作断开游戏
                if title == '连接中断':
                    self.click(self.xpath(CONFIRM))
                    self.interval_reset(TITLE)
                    continue
            if self.appear_then_click(LOGIN_BUTTON, interval=3):
                continue
            if self.appear(LOGIN_CONFIRM):
                logger.error('请先在云原神上登录你的帐号')
                raise RequestHumanTakeover

    def _cloud_get_duration(self) -> int:
        """
        Returns:
            int: Total minutes of remaining duration

        Pages:
            in: GAME_START
        """
        # 6 小时 54 分钟
        free = self.xpath(STATUS_FREE).text.strip()
        logger.attr('免费时长', free)

        # 7500
        paid = self.xpath(STATUS_PAID).text.strip()
        logger.attr('米云币', paid)

        duration = 0
        res = re.search(r'(\d+).*?小时.*?(\d+).*?分钟', free)
        if res:
            h = int(res.group(1))
            m = int(res.group(2))
            duration += h * 60 + m
        else:
            logger.warning(f'无法解析云原神免费时长: {free}')

        try:
            # 10米云币=1分钟游戏时长
            m = int(paid) // 10
            duration += m
        except ValueError:
            logger.warning(f'无法解析米云币数量: {paid}')

        logger.attr('云原神剩余时长', f'{duration} min')
        return duration

    @func_debug
    def _cloud_enter_game(self):
        """
        Pages:
            in: GAME_START
            out:
        """
        logger.info('进入游戏')
        prev_info = ''
        while 1:
            self.dump_hierarchy()

            if self.appear(FLOAT_WINDOW):
                logger.info('云原神排队结束')
                break

            # Watch queue info
            queue_info = self.xpath(QUEUE_INFO)
            if queue_info:
                text = queue_info.text.replace('\n', '')
                if text != prev_info:
                    logger.info(text)
                    prev_info = text
                    self.stuck_record_clear()
                self.interval_reset(GAME_START)

            if self.appear_then_click(GAME_START, interval=3):
                continue
            if self.interval_get(TITLE).reached():
                title = self.xpath(TITLE).text
                if title == '当前网络环境较差':
                    # 重新测速
                    self.click(self.xpath(CONFIRM))
                    self.interval_reset(TITLE)
                    continue
                if title == '计费提示':
                    # 本次游戏将使用畅玩卡无限畅玩
                    self.click(self.xpath(CONFIRM))
                    self.interval_reset(TITLE)
                    continue

    @func_debug
    def _cloud_setting_enter(self, skip_first=True):
        while 1:
            if skip_first:
                skip_first = False
            else:
                self.dump_hierarchy()

            if self.appear(FLOAT_CHECK):
                break

            if self.appear_then_click(FLOAT_WINDOW, interval=3):
                continue

    @func_debug
    def _cloud_setting_exit(self, skip_first=True):
        while 1:
            if skip_first:
                skip_first = False
            else:
                self.dump_hierarchy()

            if self.appear(FLOAT_WINDOW):
                break

            if self.appear(FLOAT_DELAY, interval=3):
                area = self.xpath(FLOAT_DELAY).area
                area = area_offset(area, offset=(150, 0))
                button = AreaButton(area=area, name='CLOUD_SETTING_EXIT')
                self.click(button)
                continue

    @func_debug
    def _cloud_settings_set(self, skip_first=True):
        """
        Configure stream settings
        """
        pass

    def cloud_ensure_ingame(self):
        """
        Pages:
            in: Any
            out: FLOAT_WINDOW, in-game
        """
        logger.info('云原神启动')
        if self.app_is_running():
            logger.info('云原神已在运行')
            self.dump_hierarchy()
        else:
            logger.info('云原神未在运行，启动云原神')
            self.app_start()

        if self.appear(GAME_START):
            logger.info('云原神在主界面')
            self._cloud_get_duration()
            self._cloud_enter_game()
        elif self.appear(FLOAT_WINDOW):
            logger.info('云原神在游戏中')
        elif self.appear(FLOAT_CHECK):
            self._cloud_setting_exit()
            logger.info('云原神在游戏中')
        else:
            self._cloud_start()
            logger.info('云原神在主界面')
            self._cloud_get_duration()
            self._cloud_enter_game()

    def cloud_keep_alive(self):
        while 1:
            logger.info('操作云原神防止被踢出')
            self._cloud_setting_enter()
            self._cloud_setting_exit()
            self.stuck_record_clear()
            self.click_record_clear()
            self.sleep((45, 90))


if __name__ == '__main__':
    self = CloudGenshin('127.0.0.1:5555')
    self.cloud_ensure_ingame()
    self.cloud_keep_alive()
