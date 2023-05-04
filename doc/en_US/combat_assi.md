# Auto Combat Assist

## Introduction

- Location: `config/settings/tactic` or CombatSetting in GUI.

- Auto Combat Assist can automatic switch characters, do attack, use E and Q skill accroding to set character name, tactic group, priorities, tiggers, etc.

- Suitable for characters who do not need to manually aim and use with shield characters. (Barely works with those who need to aim, just barely)

- Require the Genshin to run in 1080p windowing. Not recommend to set color filters.

- Need to set `team.json` file. The setting method is shown below.

- Recommend to bring Zhongli, if not can bring 3~4 shield characters.
## tactic_group

Auto Combat Assist support the following tactic:

| Tactic Keyword | Description |
|---------------|--------------------------------|
| `>` | Skip to next group immediately |
| `@e?A:B` | Detect whether the Elemental Skill is in effetc. If it take effect, execute A. Otherwise, execute B. |
| `e?A:B`       | 元素战技是否就绪。就绪执行A，否则执行B。          |
| `q?A:B`       | 元素爆发是否就绪。就绪执行A，否则执行B。          |
| `#@e?A:B`     | 元素战技是否正在持续，如果正在持续，循环执行A,否则执行B。 |
| `#@q?A:B`     | 元素爆发是否正在持续，如果正在持续，循环执行A,否则执行B。 |
| `a`/`a~`/`da` | 普通攻击/重击/下落攻击                   |
| `e`/`e~`      | 使用元素战技（点按/长按）                  |
| `j`           | 跳跃                             |
| `ja`          | 跳跃攻击                           |
| `sp`          | 冲刺                             |
| 数字            | 延时，单位为`毫秒`                     |

每个策略关键字用`,`分隔；不同策略组用`;`分隔。当一组策略执行完毕后，执行下一个策略组。

注意：

- 瞄准射箭的角色可以用重击代替。
- 自动瞄准在射箭蓄力状态下，会被巨大的蓄力特效所干扰，导致识别混乱。所以尽量少使用单体伤害弓箭类角色，甘雨等范围伤害角色除外。
- 不能添加空格。

- 在判断表达式中，策略关键字之间用`.`分隔。
- 在判断表达式中，策略关键字之间用`.`分隔。
- 在判断表达式中，策略关键字之间用`.`分隔。

含有`?`的策略关键字用法与三元运算符相近，如：

`@e?e:a;`：当元素战技准备时执行e，否则执行a。

`@e?e.a.a:none;`：当元素战技准备时执行`e,a,a`，否则不执行。

其中，`none` 可以为其他任何无意义字符，表示不执行任何动作。

注意：

- 判断表达式中，不能嵌套判断表达式；
- 判断表达式最好以分号结束，后面不再接策略关键字。

示例：

| 角色      | 策略                   |
|---------|----------------------|
| zhongli | `e?e~:none;q?q:none` |
| yunjin  | `e?e~:none;q?q:none` |
| yoimiya | `e?e:none;#@e?a:q;`  |

## 触发器 trigger

触发器条件成立时，允许切换至该角色。

| 触发器       | 说明                 |
|-----------|--------------------|
| `e_ready` | 当角色的元素战技准备就绪时，可以切换 |
| `q_ready` | 当角色的元素爆发准备就绪时，可以切换 |
| `idle`    | 始终触发               |

可以使用多个触发器，触发器之间用逗号分隔。不能有空格。
当多个角色的触发条件成立时，切换角色的顺序由优先级决定。

## 角色定位 position

角色定位是角色在队伍中的作用。
| 类型       | 说明|
|-----------|--------------------|
| `Main` | 当角色的元素战技准备就绪时，可以切换 |
| `Shield` | 当角色的元素爆发准备就绪时，可以切换 |
| `Support`    | 始终触发|
| `Recovery` | 回血类角色|

角色定位的设置会影响自动战斗的部分功能。
## 优先级 priority

优先级从小到大依次降低，0为最高优先级。
优先级可以同级。

这是GIA的默认优先级配置：

n=角色在队伍中的位置, n∈{1,2,3,4}

- `Shield`:1000+n
- `Recovery`:1500+n
- `Support`:3000+n
- `Main`:2000+n

你可以不使用基于千位数的值，这只是用于区分配置是否自动生成。

## 其他设置

| 设置项               | 介绍                       |
|-------------------|--------------------------|
| `Elast_time`      | E技能持续时间，没有则为0            |
| `Qlast_time`      | Q技能持续时间，没有则为0            |
| `E_short_cd_time` | 短Ecd时间，不能为0              |
| `Epress_time`     | 长按E的时间，没有则为0             |
| `E_long_cd_time`  | 长Ecd时间，没有则为0             |
| `Qcd_time`| Q技能冷却时间|
| `n`               | 角色在队伍中的位置（1~4），不可重复，不可为0 |

## 自动配置team文件

在GUI中，新建team文件，输入角色名后按下自动填充，所有空输入框和标记为-1的输入框会被自动填充。

角色在队伍中的位置、角色优先级和部分角色的触发器不会自动填充。

[支持的角色列表](../../assets/characters_data/characters_parameters.json)

[角色名文件 感谢xicri/genshin-dictionary](../../assets/characters_data/characters_name.json)

欢迎贡献角色参数(ﾉﾟ∀ﾟ)ﾉ

## 自动生成team文件

如果在设置中启用了自动生成team文件，则会在战斗开始前扫描角色列表并扫描tactic下的所有策略文件，选择符合的策略文件。

如果没有符合的策略文件吗，则根据[支持的角色列表](../../assets/characters_data/characters_parameters.json)自动生成一套战斗策略。

如果角色不存在于[支持的角色列表](../../assets/characters_data/characters_parameters.json)则会使用默认的team文件。

## 角色元素战技、元素爆发图片设置

自新版本起，无需设置图片。

## 其他注意事项

- 角色名称可在`config/character_dist.json`中查找，每个角色的首项即为该角色名称，其余为角色别名，如：

`["albedo","Albedo","阿贝多","アルベド"]`中，角色名称为`albedo`，其他为别名。

- 角色血量过低或有角色死亡时，程序可能暂停运行。
- 不在合适的界面时，程序可能暂停运行。

由于~~是个非酋~~能力有限，角色较少，上述配置并非最优方案，如果你有更好的方案，随时`issue`

如果遇到无法解决的问题，也可提交`issue`。

如果有好的角色输出手法可以发`issue`或者在q群分享~

## team.json文件示例

你可以新建新的策略文件并将设置中的`teamfile`修改为你自己的文件.

不能在`示例json`中直接修改，否则你的修改将在下一次启动后清除。

文件示例：

[文件示例1 宵宫 钟离 班尼特 云堇](./team_example1.json)

[文件示例2 凝光 钟离 班尼特 云堇](./team_example2.json)

[文件示例3 凌人 钟离 班尼特 纳西妲](./team_example3.json)

在tactic文件夹中也有该示例文件。


