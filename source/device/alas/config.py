class AzurLaneConfig:
    # TODO: Alas 配置文件里要求的全局设置，以后再改（

    """
    module.device
    """
    DEVICE_OVER_HTTP = False
    FORWARD_PORT_RANGE = (20000, 21000)
    REVERSE_SERVER_PORT = 7903

    # ASCREENCAP_FILEPATH_LOCAL = './bin/ascreencap'
    # ASCREENCAP_FILEPATH_REMOTE = '/data/local/tmp/ascreencap'

    # 'DroidCast', 'DroidCast_raw'
    DROIDCAST_VERSION = 'DroidCast'
    DROIDCAST_FILEPATH_LOCAL = './assets/Android/DroidCast/DroidCast-debug-1.1.0.apk'
    DROIDCAST_FILEPATH_REMOTE = '/data/local/tmp/DroidCast.apk'
    DROIDCAST_RAW_FILEPATH_LOCAL = './assets/Android/DroidCast/DroidCastS-release-1.1.5.apk'
    DROIDCAST_RAW_FILEPATH_REMOTE = '/data/local/tmp/DroidCastS.apk'

    MINITOUCH_FILEPATH_REMOTE = '/data/local/tmp/minitouch'

    # HERMIT_FILEPATH_LOCAL = './bin/hermit/hermit.apk'

    # SCRCPY_FILEPATH_LOCAL = './bin/scrcpy/scrcpy-server-v1.20.jar'
    # SCRCPY_FILEPATH_REMOTE = '/data/local/tmp/scrcpy-server-v1.20.jar'

    MAATOUCH_FILEPATH_LOCAL = './assets/Android/MaaTouch/maatouch'
    MAATOUCH_FILEPATH_REMOTE = '/data/local/tmp/maatouch'

    # Group `Emulator`
    Emulator_Serial = 'auto'
    Emulator_PackageName = 'com.miHoYo.cloudgames.ys'
    # Emulator_ServerName = 'disabled'  # disabled, cn_android-0, cn_android-1, cn_android-2, cn_android-3, cn_android-4, cn_android-5, cn_android-6, cn_android-7, cn_android-8, cn_android-9, cn_android-10, cn_android-11, cn_android-12, cn_android-13, cn_android-14, cn_android-15, cn_android-16, cn_android-17, cn_android-18, cn_android-19, cn_android-20, cn_android-21, cn_android-22, cn_ios-0, cn_ios-1, cn_ios-2, cn_ios-3, cn_ios-4, cn_ios-5, cn_ios-6, cn_ios-7, cn_ios-8, cn_ios-9, cn_ios-10, cn_channel-0, cn_channel-1, cn_channel-2, cn_channel-3, en-0, en-1, en-2, en-3, en-4, jp-0, jp-1, jp-2, jp-3, jp-4, jp-5, jp-6, jp-7, jp-8, jp-9, jp-10, jp-11, jp-12, jp-13, jp-14, jp-15, jp-16, jp-17
    Emulator_ScreenshotMethod = 'DroidCast_raw'  # auto, ADB, ADB_nc, uiautomator2, aScreenCap, aScreenCap_nc, DroidCast, DroidCast_raw, scrcpy
    Emulator_ControlMethod = 'MaaTouch'  # ADB, uiautomator2, minitouch, Hermit, MaaTouch
    Emulator_ScreenshotDedithering = False
    Emulator_AdbRestart = False

    # Group `Error`
    Error_HandleError = True
    Error_SaveError = False
    Error_OnePushConfig = 'provider: null'
    Error_ScreenshotLength = 1

    # Group `Optimization`
    Optimization_ScreenshotInterval = 0.1
    Optimization_CombatScreenshotInterval = 1.0
    Optimization_TaskHoardingDuration = 0
    Optimization_WhenTaskQueueEmpty = 'goto_main'  # stay_there, goto_main, close_game
