# Automatic combat assist

```
Portions of this document may be machine translated.
```

## Introduction

- Location: `config/settings/tactic`

- Automatic combat assistance can automatically switch roles and execute attacks according to the set roles, strategies, priorities, trigger conditions, etc., and use elemental combat skills and elemental bursts.

- Press `/` to start or end auto combat assist.

- Suitable for characters that don't need to manually aim and use with shield characters.

- Requires Genshin Impact to run windowed at 1080p. Color filters are not recommended.

- The `team.json` file needs to be set, and the setting method is as follows.

## strategy group tactic_group

Auto Combat Assist supports the following strategies:

| Strategy Keyword | Description |
|---------------|----------------------------------|
| `>` | Jump to the next group immediately |
| `@e?A:B` | Whether elemental combat skills are effective. Execute A if it takes effect, otherwise execute B. |
| `e?A:B` | Whether the elemental combat skills are ready. Execute A if ready, otherwise execute B. |
| `q?A:B` | Whether the element burst is ready. Execute A if ready, otherwise execute B. |
| `#@e?A:B` | Whether the elemental combat skill is continuing, if it is continuing, execute A in a loop, otherwise execute B. |
| `#@q?A:B` | Whether the element outbreak is continuing, if it is continuing, execute A in a loop, otherwise execute B. |
| `a`/`a~`/`da` | normal attack/heavy attack/drop attack |
| `e`/`e~` | Use elemental combat skills (tap/long press) |
| `j` | jump |
| `ja` | jump attack |
| `sp` | sprint |
| Number | Delay in `milliseconds` |

Each strategy keyword is separated by `,`; different strategy groups are separated by `;`. When a group of policies is executed, the next policy group is executed.

Notice:

```
waiting for translate
- 瞄准射箭的角色可以用重击代替。
- 自动瞄准在射箭蓄力状态下，会被巨大的蓄力特效所干扰，导致识别混乱。所以尽量少使用单体伤害弓箭类角色，甘雨等范围伤害角色除外。
```

- Spaces cannot be added.

- In the judgment expression, the strategy keywords are separated by `.`.
- In the judgment expression, the strategy keywords are separated by `.`.
- In the judgment expression, the strategy keywords are separated by `.`.

The usage of strategy keywords containing `?` is similar to the ternary operator, such as:

`@e?e:a;`: Execute e when the elemental skill is ready, otherwise execute a.

`@e?e.a.a:none;`: Execute `e,a,a` when the elemental combat technique is ready, otherwise do not execute.

Among them, `none` can be any other meaningless characters, which means no action will be performed.

Notice:

- Judgment expressions cannot be nested;
- It is better to end the judgment expression with a semicolon, and no strategy keyword after it.

Example:

| Roles | Strategies |
|---------|----------------------|
| zhongli | `e?e~:none;q?q:none` |
| yunjin | `e?e~:none;q?q:none` |
| yoimiya | `e?e:none;#@e?a:q;` |

## trigger trigger

Switching to this role is allowed when the trigger condition is met.

| Trigger | Description |
|-----------|-------------------|
| `e_ready` | When the character's elemental combat skills are ready, you can switch |
| `q_ready` | Can switch when the character's elemental burst is ready |
| `idle` | fires always |

The current version does not support multiple triggers.
When the trigger conditions of multiple roles are met, the order of switching roles is determined by the priority.

## priority priority

The priority decreases from small to large, and 0 is the highest priority.
Priority can be the same level.

## other settings

| Settings | Introduction |
|--------------------|--------------------------|
| `Elast_time` | The duration of the E skill, if not, it will be 0 |
| `Qlast_time` | Q skill duration, 0 if no |
| `E_short_cd_time` | Short Ecd time, cannot be 0 |
| `Epress_time` | The time of long pressing E, otherwise it will be 0 |
| `E_long_cd_time` | long Ecd time, 0 if no |
| `Qcd_time`| Q skill cooldown time|
| `n` | The position of the character in the team (1~4), cannot be repeated, cannot be 0 |

## Automatically configure the team file

There are some configured characters in the `character.json` file. At this time, in the `team.json` file, you only need to set `autofill` to `true` and configure `name`
,`priority`,`n`,`trigger` will do.
The `verify` attribute in `character.json` can check whether the character operation is verified.

- NOTE: This method is available but not recommended at this time. It is suitable for avoiding repeated configuration when there are multiple teams.

## Character element combat skills, element burst picture settings

As of the new version, there is no need to set an image.

## Other considerations

- If there is no response after the program starts, press Enter

- The character name can be found in `config/character_dist.json`, the first item of each character is the character name, and the rest are role aliases, such as:

In `["albedo","Albedo","Albedo","アルベド"]`, the character name is `albedo`, and the others are aliases.

- When the character's health is too low or a character dies, the program may pause.
- The program may pause when not in the appropriate interface.

Since ~~ is a non-chief ~~ has limited ability and fewer roles, the above configuration is not the optimal solution, if you have a better solution, feel free to `issue`

If you encounter a problem that cannot be solved, you can also submit an `issue`.

If you have a good character output method, you can send an `issue` or share it in the q group~

## team.json file example

You can modify the `sample json` based on your own needs, or create a new `json` and add the
Modify `teamfile` to your own `json`.

File example:

[File Example 1 Xiaogong Zhongli Bennett Yunjin](./team_example1.json)

[File example 2 Ningguang Zhongli Bennett Yunjin](./team_example2.json)

There is also the sample file in the tactic folder.