# config

此页面介绍config文件夹中的各个文件用途。

config.json文件位置：`genshin_assistant\config`

## config.json

| 项目                | 内容                                                                                                    |
|-------------------|-------------------------------------------------------------------------------------------------------|
| `version`         | 版本号                                                                                                   |
| `teamfile`        | 自动战斗使用的`team.json`文件，可在`config`目录下新建新的`teamjson`文件并设置。                                                |
| `domain_times`    | 刷秘境的次数                                                                                                |
| `isLiYueDomain`   | 挑战部分石化古树被墙壁阻挡视野的秘境(大多位于璃月)时，设置为`true`，否则为`false`                                                      |
| `device_torch`    | yolox运算使用的设备，如果安装了cudnn则设为`'gpu'`，否则设为`'cpu'` 。 设置为`auto`时可以自动检测GPU可用性并自动切换。                          |
| `device_paddle`   | paddleocr运算使用的设备，如果安装了cudnn则设为`'gpu'`，否则设为`'cpu'`。 设置为`auto`时，会自动检测GPU可用性，但不会自动切换GPU，需要根据是否可用的提示手动切换。 |
| `debug`           | 是否启用debug模式                                                                                           |
| `env_floder_path` | envirenment文件夹位置                                                                                      |
| `resin`           | 领取奖励时选择的原萃树脂模式，`20`代表小树脂，`40`代表浓缩                                                                     |
| `corr_degree`     | 秘境内视角校准时的辅助参数。若在秘境内视角偏左则增大该值，反之亦然。                                                                    |

## keymap.json

可以自定义按键。详情如下：
| 项目 | 内容 |
| --------------- | ------------------------------------------------------------ |
| `autoCombat`   | 开关自动战斗的按键|
| `autoDomain`| 开关自动秘境的按键|

## character.json

包含了一些预设的角色策略组参数，`verify`属性可以查看该角色操作是否被验证通过。

## character_dist.json

角色名称对照表，每个角色的首项即为该角色名称，其余为角色别名，如：

`["albedo","Albedo","阿贝多","アルベド"]`中，角色名称为`albedo`，其他为别名。

## team.json

默认出战队伍配置文件，在第一次使用前需要根据自己情况更改，或按文件中的配置更改自己的队伍，注意出战顺序要相符。

如配置文件与实际出战队伍角色不符或顺序不符，会造成角色乱放技能、乱切换等问题。

原始文件中的队伍配置为：宵宫，钟离，班尼特，云堇

| 设置项               | 介绍                                                                                                                 |
|-------------------|--------------------------------------------------------------------------------------------------------------------|
| `name`            | 根据`character_dist.json`填写角色名称                                                                                      |
| `priority`        | 出战优先级，从小到大依次降低，0为最高优先级。优先级可以同级                                                                                     |
| `n`               | 角色在队伍中的位置（1~4），不可重复，不可为0                                                                                           |
| `trigger`         | 触发器，触发器条件成立时，允许切换至该角色                                                                                              |
| `autofill`        | 自动填充，在`character.json`文件中有一些已经配置好的角色,此时在`team.json`文件中只需要将`autofill`设置为`true`,并配置`name`,`priority`,`n`,`trigger`即可 |
| `Elast_time`      | E技能持续时间，没有则为0                                                                                                      |
| `Qlast_time`      | Q技能持续时间，没有则为0                                                                                                      |
| `E_short_cd_time` | 短Ecd时间，不能为0                                                                                                        |
| `E_long_cd_time`  | 长Ecd时间，没有则为0                                                                                                       |
| `Ecd_float_time`  | 在E技能冷却还有x秒前即切换至该角色，可以为0，建议设置的值比预计值偏小一点                                                                             |
| `Ecd_press_time`  | 按E技能的时间                                                                                                            |
| `tastic_group`    | 策略组，配置角色战斗策略，详细说明见[combat_assi.md](./combat_assi.md)                                                               |

如`autofill`参数为`true`，且`character.json`文件中有此角色的配置参数时，则无需在`team.jsom`中填写`Elast_time`、`Qlast_time`
、`E_short_cd_time`、`E_long_cd_time`、`Ecd_float_time`、`Ecd_press_time`、`tastic_group`参数。

如`autofill`参数为`false`，则需要在`team.json`中填写战斗相关参数。

关于参数配置的填写说明见[combat_assi.md](./combat_assi.md)

## tastic.json

暂无用途
