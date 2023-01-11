# genshin_impact_assistant Genshin Assistant

```
Portions of this document may be machine translated.
```
```
Portions of this document were manually proofread.
```

<strong> The program's support for English is not yet complete. If you want to use it at this stage, please switch Genshin Impact to Simplified Chinese. Full support will be completed in January 2023 ~ February 2023.  </strong>

<div align="center">

Based on image recognition and simulated keyboard operations, the multi-functional Genshin automatically assists operations, including automatic combat, automatic domain, and automatic obtain materials in the teyvat big world.

The goal of GIA is: Let the program be responsible for playing Genshin, and you are responsible for get various characters and have fun with characters~~playn with ur wifes~~

[![GitHub Star](https://img.shields.io/github/stars/infstellar/genshin_impact_assistant?style=flat-square)](https://github.com/infstellar/genshin_impact_assistant/stargazers)
[![Release Download](https://img.shields.io/github/downloads/infstellar/genshin_impact_assistant/total?style=flat-square)](https://github.com/infstellar/genshin_impact_assistant/releases/download/v0.3.0/GIA.Launcher.v0.3.0.7z)
[![Release Version](https://img.shields.io/github/v/release/infstellar/genshin_impact_assistant?style=flat-square)](https://github.com/infstellar/genshin_impact_assistant/releases/latest)
[![Python Version](https://img.shields.io/badge/python-v3.7.6-blue?style=flat-square)](https://www.python.org/downloads/release/python-376/)
[![GitHub Repo Languages](https://img.shields.io/github/languages/top/infstellar/genshin_impact_assistant?style=flat-square)](https://github.com/infstellar/genshin_impact_assistant/search?l=Python)
![GitHub Repo size](https://img.shields.io/github/repo-size/infstellar/genshin_impact_assistant?style=flat-square&color=3cb371)
[![contributors](https://img.shields.io/github/contributors/infstellar/genshin_impact_assistant?style=flat-square)](https://github.com/infstellar/genshin_impact_assistant/graphs/contributors)
</br></br>
[![QQ group](https://img.shields.io/badge/QQ-901372518-blue.svg?style=flat-square&color=12b7f5&logo=qq)](https://jq.qq.com/?_wv=1027&k=YLTrqlzX)
[![Bilibili](https://img.shields.io/badge/bilibili-infstellar-blue.svg?style=flat-square&logo=bilibili)](https://space.bilibili.com/313212782)

</div>

# Introduce

Genshin's automatic operation assistance based on image recognition. Using image recognition and simulated keyboard operations does not involve illegal operations.

## Demo video

<https://www.bilibili.com/video/BV1RV4y157m6> (hang up)

<https://www.youtube.com/watch?v=ZieBDx6Go4A> (v0.2.0 demo video, some may be outdated)

## Functions and how they are started

### 1. [Auto Combat Assist](./combat_assi.md)

- Switch FlowMode to AutoCombat in GUI, wait for module to import

- Press the `[` key to start/stop the function. Can be changed in `keymap.json`.

For other settings, see [Introduction to Auto Combat Assist](./combat_assi.md).

### 2. [Auto Domain Assist](./domain_assi.md)

1. Set the number of times to challenge the domain and other settings in config, see [config settings](./config.md) for details.
2. Manually select the team, configure the team, and enter the domain
3. After entering the domain, switch the FlowMode to AutoDomain in the GUI and wait for the module to be imported
4. Press the `[` key to start/stop the function. Can be changed in `keymap.json`.

- Please read the notes in [domain_assi.md](./domain_assi.md).

For other settings, see [Introduction to Automatic Domain Assistant](./domain_assi.md).

### 3. [Automatic Collection Assist](./collector_assi.md)

Demonstration video: <https://www.bilibili.com/video/BV163411Q7fD>

<strong>Note: Function in test</strong>

- Switch FlowMode to AutoCollector in GUI, wait for module import

- Press the `[` key to start/stop the function. Can be changed in `keymap.json`.

- Please read the notes in [collector_assi.md](./collector_assi.md).

For other settings, see [Introduction to Automatic Collection Assist](./collector_assi.md).

## Instructions

### Quick Install

Please refer to [How to use GIA Launcher automatic installer](install.md).

### Build from source

See [Source code installation method](git_install.md)

## Setup before use

### Genshin window settings

- You need to run the program after the Genshin Impact is started.

- Genshin Impact needs to run in 1080p windowed mode (full screen is also possible), set anti-aliasing to SMAA, medium or above special effects.

- The window focus should be on the Genshin Impact window. If you switch the focus window to others, the program will suspend all keyboard and mouse operations and wait.

### config configuration

Before using, you need to pay attention to these configuration contents:

|Location|Configuration Item|Content|
|----|----|----|
|config/settings/config.json| `ChromelessWindow` | Set to true if it is a borderless window or full screen. |

Can be modified in the GUI or directly from the file.

For more other configuration items, see [config settings](./config.md).

### How to use the GUI

#### main window

- Click the main button to enter

- FlowMode: select the currently enabled function

- Log: output log

#### setting window

- Click the setting button to enter

- Select the corresponding config in the drop-down list to configure.

For more GUI usage methods such as remote operation, refer to [GUI usage](./gui.md)

### config settings

Refer to [config settings](./config.md).

## error report

If you encounter problems in use, you can submit an issue.

Before reporting an error, please make sure you have read the known issues and solutions in the documentation and [FAQ](FAQ.md).

When reporting errors, please also submit the log files in the `Logs` folder.

## Update roadmap

[Roadmap](update_note.md)

## Frequently Asked Questions FAQ

If you encounter problems during use, you can take a look at the FAQ first:

[FAQ](FAQ.md)

## Performance requirements

- This program requires at least `2.5G RAM` and `6G storage space`.

## Acknowledgments

### Open Source Libraries

#### Special thanks to

- [GenshinImpact AutoTrack DLL for coordinate positioning based on image algorithm](https://github.com/GengGode/GenshinImpact_AutoTrack_DLL)

- [Kongying Tavern Yuanshen Map kongying-tavern/yuan-shen-map](https://github.com/kongying-tavern/yuan-shen-map)

- [Alas referenced automatic installation and code implementation](https://github.com/LmeSzinc/AzurLaneAutoScript)

#### Open source library call

- [opencv](https://github.com/opencv/opencv)
- [paddleocr](https://github.com/PaddlePaddle/PaddleOCR)
- [yolox](https://github.com/Megvii-BaseDetection/YOLOX)
- [pyinstaller](https://github.com/pyinstaller/pyinstaller)

#### other

- [GIS refers to the format of the auto-combat script](https://github.com/phonowell/genshin-impact-script)

### Contributions/Contributors

- Dataset labeling, testing: [nɡ.](https://space.bilibili.com/396023811)

## statement

- This software is open source and free. It is only for learning and communication. Please do not use it for illegal purposes. The fees charged by merchants who use this software for leveling are the labor/equipment costs of the merchants. <strong>
Any problem</strong> has nothing to do with this software.
> Don't use it, don't use it --unknown
## advertise

Qq group: [901372518] (https://jq.qq.com/?_wv=1027&k=YLTrqlzX)

Developer exchange group: [680029885](https://jq.qq.com/?_wv=1027&k=CGuTvCXU)
(Make sure you already know how to use git and github)

Other software (such as discord) will also be used soon.
