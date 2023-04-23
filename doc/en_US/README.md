# genshin_impact_assistant 原神助手
<strong>|[Chinese](./)|[English](en_US/readme.md)|</strong>
<div align="center">

A multi-functional auto-assist based on image recognition and keystroke simulation, including auto combat, auto domain and auto claim materials in Teyvat world

The aim of GIA is: let the program play Genshin, and you just need to selected characters and raise them.

[![GitHub Star](https://img.shields.io/github/stars/infstellar/genshin_impact_assistant?style=flat-square)](https://github.com/infstellar/genshin_impact_assistant/stargazers)
[![Release Download](https://img.shields.io/github/downloads/infstellar/genshin_impact_assistant/total?style=flat-square)](https://github.com/infstellar/genshin_impact_assistant/releases/download/v0.3.0/GIA.Launcher.v0.3.0.7z)
[![Release Version](https://img.shields.io/github/v/release/infstellar/genshin_impact_assistant?style=flat-square)](https://github.com/infstellar/genshin_impact_assistant/releases/latest)
[![Python Version](https://img.shields.io/badge/python-v3.7.6-blue?style=flat-square)](https://www.python.org/downloads/release/python-376/)
[![GitHub Repo Languages](https://img.shields.io/github/languages/top/infstellar/genshin_impact_assistant?style=flat-square)](https://github.com/infstellar/genshin_impact_assistant/search?l=Python)
![GitHub Repo size](https://img.shields.io/github/repo-size/infstellar/genshin_impact_assistant?style=flat-square&color=3cb371)
[![contributors](https://img.shields.io/github/contributors/infstellar/genshin_impact_assistant?style=flat-square)](https://github.com/infstellar/genshin_impact_assistant/graphs/contributors)
</br></br>
[![QQ群](https://img.shields.io/badge/QQ群-901372518-blue.svg?style=flat-square&color=12b7f5&logo=qq)](https://jq.qq.com/?_wv=1027&k=YLTrqlzX)
[![Bilibili](https://img.shields.io/badge/bilibili-infstellar-blue.svg?style=flat-square&logo=bilibili)](https://space.bilibili.com/313212782)<!-- ignore gettext -->

</div>

## Introduction

An Genshin automatic operation assistance based on image recognization and similated keyboard operation. Does not involve not-allowed operation.

To those who have not used github: the blue text in the docs is a hyperlink that can be clicked.

## Demo Video

<https://www.bilibili.com/video/BV1RV4y157m6>(hung up)

Addendum <https://www.youtube.com/watch?v=ZieBDx6Go4A> v0.2.0 demo video, may be partially out of date.

## Function Introduction

### 1. [Auto Combat Assist](./combat_assi.md)

- Switch Function to AutoCombat and wait for the module to be imported.

- Press `[` key to start/stop function. Can be edited in `keymap`.

For other settings, see [Auto Combat Assist introduction](./combat_assi.md).

### 2. [Auto Domain Assist](./domain_assi.md)

1. Set the number of challenges and other settings in the config, see [config settings](./config.md).
2. select the party manually, then enter the domain.
3. After enter domain(also in the Teyvat world ), select the DomainTask in GUI Tasklist, then click `start task` button.
4. Switch to Genshin window after imported.

Be careful to read the notes in [domain_assi.md](./domain_assi.md).

For other settings, sett [Auto Domain Assist introduction](./domain_assi.md).

### 3. [Auto Collect Assist](./collector_assi.md)

Demo video：<https://www.bilibili.com/video/BV163411Q7fD>

- Switch the Mission Group to AutoCollectorMission.json in GUI.

- Select Mission in Task List, then start Task.

- Be careful to read the notes in [collector_assi.md](./collector_assi.md).

For other settings, see[Auto Collector Assist introduction](./collector_assi.md).

### 4. [Auto Daily Commission Assist](./commission_assi.md)
**In Early Access, pls use it with caution and report any error occuring. **

For more detiles, see [Auto Daily Commission Assist introduction](./commission_assi.md).

### 5. [Claim Daily Reward](./claim_reward.md)
see [Claim Daily Reward introduction](./commission_assi.md).

### 6. [Auto Ley Line Outcrop Assist](./ley_line_ourcrop.md)
See [[Auto Ley Line Outcrop Assist introduction](./commission_assi.md).

## How to use

### Quick installation

See [GIA Launcher Auto Installer Tutorial](install.md).

### Run from source code

See [Source code running tutorial](git_install.md)

## Pre-use settings

### Genshin window settings

- Need to run GIA after the Genshin Impact starts.

- The Genshin needs to run in 1080p window (full screen is also possible), set anti-aliasing to SMAA, effects to meduim or above.

- The focus of windows shoule be on Genshin window. If the focus window is switched to another window, the program will pause all the operation of keyboard and mouse and wait.

### Config configuration

Before use, these configuration elements shoule be noted:

|Path|Configuration|Content|
|----|----|----|
|config/settings/config.json| `BorderlessWindow` | When using boradless window or full screen, set to true.|

Can be modified in the GUI or directly from the file.

For other configurations, see the notes of settings within the GUI.

### GUI Tutorials

#### Main window

- click `main` button to enter.
- Task List: select the task to be executed, can only be active in the GUI.
- FlowMode: Select the function to be enable, can only be activated by hotkey.
- Mission: select the mission group to be started, then select the `Mission` in `Task List` to start task list.
- Log: output logs.

#### Setting page

- click button to enter

- Select the corresponding item in the drop-down list to configure.

Other features such as remote control, see the [GUI guide](./gui.md)

### Auto combat, auto collect settings windows

- Click the corresponding button to enter and follow the instructions.

## Bug report

If you encounter ploblems in using, you can create an issue or give a feedback in qq group or discord.

Please make sure you have read the document and [FAQ](FAQ.md) before feedback bugs.

Please send the log file in the Logs folder when you feedback.

## Frequently ask question

If you enconter any problem when using, you can take a look at FAQ frist:

[FAQ](FAQ.md)

## Known issues

[Known issues](known_issues.md)

## Performance requirements

- This program requires at least `2.5G` RAM and `3G` storage space (full installation).

## 鸣谢

### 特别感谢

- [Alas](https://github.com/LmeSzinc/AzurLaneAutoScript)

### 开源库

#### 原神相关

- [GenshinImpact AutoTrack DLL](https://github.com/GengGode/cvAutoTrack)

- [kongying-tavern/yuan-shen-map](https://github.com/kongying-tavern/yuan-shen-map)

- [xicri/genshin-dictionary](https://github.com/xicri/genshin-dictionary)

#### Open source library

- [opencv](https://github.com/opencv/opencv)
- [paddleocr](https://github.com/PaddlePaddle/PaddleOCR)
- [yolox](https://github.com/Megvii-BaseDetection/YOLOX)
- [pyinstaller](https://github.com/pyinstaller/pyinstaller)

#### Others

- [GIS](https://github.com/phonowell/genshin-impact-script)

### Other Contributors

- Dataset labeling: [nɡ.](https://space.bilibili.com/396023811)

## Announcement

- 本软件开源免费,仅供学习交流使用,请勿用于非法用途.使用本软件进行代练的商家所收取的费用均为商家的人工/设备费用,产生的**任何问题**与本软件无关.

> 用别怂,怂别用 --unknown
## 广告

QQ group:[901372518](https://jq.qq.com/?_wv=1027&k=YLTrqlzX)

开发者交流群:[680029885](https://jq.qq.com/?_wv=1027&k=CGuTvCXU)
(请确保你已经会使用git以及github)


