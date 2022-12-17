# genshin_impact_assistant 原神助手

多功能原神自动辅助操作,包括自动战斗,自动刷秘境.不用每天原神半小时清体力了(*´▽｀)ノノ

To没用过github的小伙伴:描述文档中的蓝色文字是链接,可以打开的.

# 介绍

基于图像识别的原神自动操作辅助.使用图片识别与模拟键盘操作,不涉及违规操作.
> 用别怂,怂别用 --unknown

## 演示视频

<https://www.bilibili.com/video/BV1RV4y157m6>(挂了)

## 功能及其启动方式

### 1. [自动战斗辅助](./doc/combat_assi.md)

- 在GUI中将FlowMode切换到AutoCombat，等待模块导入

- 按下`[`键启动/停止功能。可在`keymap.json`中更改。

其他设置参见[自动战斗辅助介绍](./doc/combat_assi.md).

### 2. [自动秘境辅助](./doc/domain_assi.md)

1. 在config中设置挑战秘境的次数与其他设置,详见[config设置](./doc/config.md).
2. 手动选择队伍,配置队伍,进入秘境.
3. 进入秘境后,在GUI中将FlowMode切换到AutoDomain，等待模块导入
4. 按下`[`键启动/停止功能。可在`keymap.json`中更改。

- 注意阅读[domain_assi.md](./doc/domain_assi.md)中的注意事项.

其他设置参见[自动秘境辅助介绍](./doc/domain_assi.md).

### 3. [自动采集辅助](./doc/collector_assi.md)

<strong>注:测试中功能</strong>

- 在GUI中将FlowMode切换到AutoCollector，等待模块导入

- 按下`[`键启动/停止功能。可在`keymap.json`中更改。

- 注意阅读[collector_assi.md](./doc/collector_assi.md)中的注意事项.

其他设置参见[自动采集辅助介绍](./doc/collector_assi.md).

## 更新路线图

[路线图](update_note.md)

## 使用方法

### 快速安装

请参见[GIA Launcher自动安装器使用方法](doc/install.md).

### 从源代码构建

#### 安装

<strong>注意: 这里是从源代码运行,需要一定编程基础.快速使用请参见:</strong>

<strong>[GIA Launcher自动安装器使用方法](doc/install.md)</strong>
要求:

- <strong>！！！ 重要修改 ！！！ python版本 3.7.6 (因为py3.9bug实在是太多了).</strong>
- python版本[3.7.6](https://www.python.org/downloads/release/python-376/).
- [git](https://git-scm.com/download/win).
- <strong>使用管理员权限打开命令提示符和你的代码编写器(IDE)!!!</strong>

1. 输入以下命令以完成源码和依赖的下载:

   ```shell
   git clone https://github.com/infstellar/genshin_impact_assistant.git&cd genshin_impact_assistant&python setup.py install
   ```

2. 输入以下命令运行程序:

   ```shell
   python genshin_assistant.py
   ```

#### 更新

提供两种方法更新:

- 使用setup.py更新:
   ```shell
   python setup.py update
   ```
- 使用git pull更新:
   ```shell
   git pull
   ```

<strong>注意: 这里是从源代码运行,需要一定编程基础.快速使用请参见:</strong>

<strong>[GIA Launcher自动安装器使用方法](doc/install.md)</strong>

### 原神窗口设置

- 需要在原神启动后再运行程序.

- 原神需要以1080p窗口化运行(全屏也可以),设置抗锯齿为SMAA,中或以上特效.

- 窗口焦点应全程在原神窗口上.

### GUI使用方法

#### main窗口

- 点击main按钮进入

- FlowMode：选择当前启用的功能

- Log：输出日志

#### setting窗口

- 点击setting按钮进入

- 在下拉列表中选择对应的config，进行配置。

### config设置

参考[config设置](./doc/config.md).

### 为什么文件这么多

神奇的python需要打包所有运行环境到一起才能启动 实际上是个python虚拟机 T_T

## 性能需求

- 此程序至少需要`2.5G内存`与`6G存储空间`.

## 鸣谢

### 开源库

#### 特别感谢

- [原神-基于图像算法的坐标定位 GenshinImpact AutoTrack DLL](https://github.com/GengGode/GenshinImpact_AutoTrack_DLL)

- [空荧酒馆原神地图 kongying-tavern/yuan-shen-map](https://github.com/kongying-tavern/yuan-shen-map)

#### 开源库调用

- [opencv](https://github.com/opencv/opencv)
- [paddleocr](https://github.com/PaddlePaddle/PaddleOCR)
- [yolox](https://github.com/Megvii-BaseDetection/YOLOX)
- [pyinstaller](https://github.com/pyinstaller/pyinstaller)

#### 其他

- [Alas 参考了自动安装与一些实现](https://github.com/LmeSzinc/AzurLaneAutoScript)
- [GIS 参考了自动战斗脚本的格式](https://github.com/phonowell/genshin-impact-script)

### 贡献/参与者

- 数据集标注,测试: [nɡ.](https://space.bilibili.com/396023811)

## 声明

- 本软件开源免费,仅供学习交流使用,请勿用于非法用途.使用本软件进行代练的商家所收取的费用均为商家的人工/设备费用,产生的<strong>
任何问题</strong>与本软件无关.

## 广告

qq群:[901372518](https://jq.qq.com/?_wv=1027&k=YLTrqlzX)

开发者交流群:[680029885](https://jq.qq.com/?_wv=1027&k=CGuTvCXU)
(请确保你已经会使用git以及github)
