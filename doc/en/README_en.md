```
Note: Parts of this document may be machine translated.

Note: English is not fully adapted yet. If necessary, you can change the game language to Simplified Chinese.
```

# genshin_impact_assistant

The multi-functional genshin automatic auxiliary operation, including automatic combat, automatic brush domain. Don't need to genshin  every day half an hour to clear physical strength (*´▽｀)ノノ

# Introduction

Image recognition based on Hara-Kami's automatic operation assistance. Uses image recognition and simulates keyboard operations, no irregularities involved.

## Functions and their activation

### 1. [Automatic combat assistance](combat_assi_en)

- Switch the FlowMode to AutoCombat in the GUI and wait for the module to be imported

- Press the `[` key to start/stop the function. Can be changed in `keymap.json`.

For other settings see [Introduction to automatic combat aids].(combat_assi_en).

### 2. [Auto Domain Assist](domain_assi_en)

1. Set the number of challenges and other settings in the config, see [config settings](config_en).
2. Manually select a team, configure the team and enter the secret world. 3.
3. Once in the secret world, switch the FlowMode to AutoDomain in the GUI and wait for the module to be imported.
4. Press the `[` key to start/stop the function. This can be changed in `keymap.json`.

- Read the notes in [domain_assi.md](domain_assi_en).

For other settings, see [Introduction to automatic secret assistance](domain_assi_en).

### 3. [Auto Collector Assist](collector_assi_en)

<strong>Note: Function under test</strong>

- Switch the FlowMode to AutoCollector in the GUI and wait for the module to be imported

- Press the `[ ` key to start/stop the function. Can be changed in `keymap.json`.

- Be careful to read the notes in [collector_assi.md](collector_assi_en).

For other settings see [Introduction to automatic collection assistance](collector_assi_en).

## Updating the Roadmap

[Roadmap](update_note.md)

## How to use

### Quick installation

See [How to use the GIA Launcher automatic installer](doc/install.md).

### Building from source

#### Installation

<strong>Note: This is run from source code and requires some programming skills. For a quick overview, see:</strong>

<strong>[How to use the GIA Launcher Auto Installer](doc/install.md)</strong>
Request:

- python version[3.7.6](https://www.python.org/downloads/release/python-376/).
- [git](https://git-scm.com/download/win).
- <strong>Open the command prompt and your code writer (IDE) with administrator privileges!!!</strong>

1. Enter the following command to complete the download of the source code and dependencies:

   ```shell
   git clone https://github.com/infstellar/genshin_impact_assistant.git&cd genshin_impact_assistant&python setup.py install
   ```

2. Type the following command to run the program:

   ```shell
   python genshin_assistant.py
   ```

#### Update

Two methods of updating are provided:

- Update with setup.py:
   ```shell
   python setup.py update
   ```
- Update with git pull:
   ```shell
   git pull
   ```

### Genshin Window Settings

- You need to run the program after the original god has started.

- Protokami needs to be run in a 1080p window (full screen is fine) with anti-aliasing set to SMAA, medium or above.

- The focus of the window should be on the original God window at all times.

### How to use the GUI

#### main window

- Click the main button to enter

- FlowMode：Select the currently enabled function

- Log：Output logs

#### setting window

- Click on the setting button to enter

- Select the corresponding config in the drop-down list and configure it.

### config settings

Refer to [config settings](. /doc/config.md).

## Performance requirements

- This application requires at least `2.5G RAM` and `6G storage`.

## Acknowledgements

### Open Source Library

#### Special thanks

- [原神-基于图像算法的坐标定位 GenshinImpact AutoTrack DLL](https://github.com/GengGode/GenshinImpact_AutoTrack_DLL)

- [空荧酒馆原神地图 kongying-tavern/yuan-shen-map](https://github.com/kongying-tavern/yuan-shen-map)

#### Open source library

- [opencv](https://github.com/opencv/opencv)
- [paddleocr](https://github.com/PaddlePaddle/PaddleOCR)
- [yolox](https://github.com/Megvii-BaseDetection/YOLOX)
- [pyinstaller](https://github.com/pyinstaller/pyinstaller)

#### Others

- [Alas Reference is made to the automatic installation with some implementations](https://github.com/LmeSzinc/AzurLaneAutoScript)
- [GIS Reference to the format of the automatic battle script](https://github.com/phonowell/genshin-impact-script)

### Contributions/participants

- Data set annotation, testing: [nɡ.](https://space.bilibili.com/396023811)

## Advertisement

QQ team:[901372518](https://jq.qq.com/?_wv=1027&k=YLTrqlzX)

developer QQ team:[680029885](https://jq.qq.com/?_wv=1027&k=CGuTvCXU)
