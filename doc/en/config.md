# config

```
Portions of this document may be machine translated.
```

This page describes the json configuration files in the config folder.

Can be changed in json file or GUI.

All configuration files location: `genshin_assistant\config\*.json`

## It is recommended to modify in the GUI

The GUI is currently available. The setting modification in the GUI is more stable, accurate and fast, and some
configuration files that the GUI does not support need to manually modify the source file.

## config.json

Location: config/settings/config.json

| Items              | Contents                                                                                                                                                                                                                                                                                                                          |
|--------------------|----------------------------------------------------|
| `version`          | version number                                                                                                                                                                                                                                                                                                                    |
| `teamfile`         | The `team.json` file used by automatic battles, you can create a new `teamjson` file and set it in the `config` directory.                                                                                                                                                                                                        |
| `device_torch`     | The device used for yolox calculations, if cudnn is installed, it is set to `'gpu'`, otherwise it is set to `'cpu'`. When set to `auto`, it can automatically detect GPU availability and switch automatically.                                                                                                                   |
| `device_paddle`    | The device used for paddleocr operation, set to `'gpu'` if cudnn is installed, otherwise set to `'cpu'`. When set to `auto`, the availability of the GPU will be detected automatically, but the GPU will not be switched automatically, and it needs to be switched manually according to the prompt of whether it is available. |
| `debug`            | Whether to enable debug mode                                                                                                                                                                                                                                                                                                      |
| `env_floder_path`  | environment folder location                                                                                                                                                                                                                                                                                                       |
| `corr_degree`      | Auxiliary parameter for viewing angle calibration in Rift. Increase this value if the view angle is to the left in the Rift, and vice versa.                                                                                                                                                                                      |
| `ChromelessWindow` | Set to true if it is a borderless window or full screen.                                                                                                                                                                                                                                                                          |

## auto_domain.json

Set automatic rift assist.

| Items           | Contents                                                                                                                                   |
|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| `domain_times`  | The number of times to farm the Rift                                                                                                       |
| `isLiYueDomain` | Set to `true` when challenging a secret realm where some petrified ancient trees are blocked by walls (mostly in Liyue), otherwise `false` |
| `resin`         | The original resin extraction mode selected when receiving rewards, `20` represents small resin, `40` represents concentrated              |
| `fast_mode`     | Set this to false if challenges cannot be started normally                                                                                 |

## keymap.json

Customized keys are available. Details are as follows:

| Items        | Contents                                               |
|--------------|--------------------------------------------------------|
| `startstop`  | The start-stop button for the function set in the GUI. |
| `autoCombat` | Button to switch auto combat                           |
| `autoDomain` | The button to switch the automatic realm               |

## character_dist.json

Role name comparison table, the first item of each role is the role name, and the rest are role aliases, such as:

In `["albedo","Albedo","Albedo","アルベド"]`, the character name is `albedo`, and the others are aliases.

## team.json

The default team configuration file needs to be changed according to your own situation before the first use, or you can
change your team according to the configuration in the file. Note that the order of battle must be consistent.

If the configuration file does not match the actual team roles or the order does not match, it will cause problems such
as random placement of skills and random switching of characters.

The team configuration in the original file is: Xiaogong, Zhongli, Bennett, Yunjin

| Settings          | Introduction                                                                                                                                                                                                            |
|:------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `name`            | Fill in the character name according to `character_dist.json`                                                                                                                                                           |
| `priority`        | Battle priority, decreasing from small to large, 0 is the highest priority. Priority can be the same level                                                                                                              |
| `n`               | The position of the character in the team (1~4), cannot be repeated, cannot be 0                                                                                                                                        |
| `trigger`         | trigger, when the trigger condition is met, it is allowed to switch to this role                                                                                                                                        |
| `autofill`        | Autofill, there are some characters already configured in the `character.json` file, at this time in the `team.json` file you only need to set `autofill` to `true`, and configure `name `,`priority`,`n`,`trigger` can |
| `Elast_time`      | The duration of the E skill, if there is no, it will be 0                                                                                                                                                               |
| `Qlast_time`      | The duration of the Q skill, if there is no, it will be 0                                                                                                                                                               |
| `E_short_cd_time` | Short Ecd time, cannot be 0                                                                                                                                                                                             |
| `E_long_cd_time`  | long Ecd time, 0 if no                                                                                                                                                                                                  |
| `Ecd_float_time`  | Switch to this character before the cooldown of E skill x seconds, it can be 0, it is recommended to set the value a little smaller than the expected value                                                             |
| `Ecd_press_time`  | Time to press Ecd skill                                                                                                                                                                                                 |
| `Qcd_time`        | Q skill cooldown time                                                                                                                                                                                                   |
| `tactic_group`    | Strategy group, configure the combat strategy of characters, see [combat_assi.md](./combat_assi.md) for details                                                                                                         |

Please refer to [combat_assi.md](./combat_assi.md) for instructions on filling in parameter configuration

## tactic.json

No use at the moment

## character.json

Contains some preset role policy group parameters, `verify` attribute can check whether the role operation is verified.

## auto_aim

Auto aim profile.

| Settings                    | Introduction                                         |
|-----------------------------|------------------------------------------------------|
| `auto_distan`               | Keep distance automatically, default is false        |
| `auto_move`                 | Automatically move the camera, the default is true   |
| `fps`                       | recognition frequency, default is 20                 |
| `max_number_of_enemy_loops` | The maximum number of enemy hunts, the default is 50 |
| `reset_time`                | Cooldown time after failed tracking, default is 40   |

## auto_pickup

Automatically pick up configuration files.

| Settings    | Introduction          |
|-------------|-----------------------|
| `blacklist` | Pickup item blacklist |