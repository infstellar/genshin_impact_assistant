# genshin_impact_assistant 原神助手

多功能原神自动辅助操作,包括自动战斗,自动刷秘境.不用每天原神半小时清体力了(*´▽｀)ノノ

To没用过github的小伙伴:描述文档中的蓝色文字是链接,可以打开的.

# 介绍

基于图像识别的原神自动操作辅助.使用图片识别与模拟键盘操作,不涉及违规操作.
> 用别怂,怂别用 --unknown

## 演示视频

<https://www.bilibili.com/video/BV1RV4y157m6>(挂了)

## 目前功能及如何启动

### 1. [自动战斗辅助](./doc/combat_assi.md)

- 按下`/`以启动或结束自动战斗辅助.

### 2. [自动秘境战斗](./doc/domain_assi.md)

1. 在config中设置挑战秘境的次数与其他设置,详见[config设置](./doc/config.md).
2. 手动选择队伍,配置队伍,进入秘境.
3. 进入秘境后,按下`]`键开始刷刷刷~
4. 如果要终止自动战斗,按下`]`键.

- 注意阅读[domain_assi.md](./doc/domain_assi.md)中的注意事项.

## 更新日志 (和饼

[更新记录](update_note.md).

## 使用方法

### 下载与安装

1. 下载`Releases`
   里最新版本的[`genshin_assistant.zip`](https://github.com/infstellar/genshin_impact_assistant/releases/latest)
   并解压,之后每次更新只需要重新下载`genshin_assistant.zip`即可.

2. 下载`Releases`里的[`environment_all.7z`](https://github.com/infstellar/genshin_impact_assistant/releases/tag/v0.2.0).

   如果`environment_all.7z`下载过慢,也可以下载`environment_no_torch.7z`,并自行下载`torch`复制到目录中(或者加入q群下载).

3. 将`genshin_assistant` 与 `environment` 文件夹置于同一目录下. 如果有能力,也可以在config中修改`env_floder_path`.

4. 根据实际情况配置config文件夹中的配置文件.

5. 启动原神后,以管理员权限运行`genshin_assistant.exe`.

6. 实在搞不定可以加[qq群](https://jq.qq.com/?_wv=1027&k=YLTrqlzX)
([图文教程](doc/install.md)).

### 从源代码构建

#### 安装

要求:

- python版本[3.9.6](https://www.python.org/downloads/release/python-396/).
- [git](https://git-scm.com/download/win).
- <strong>使用管理员权限打开命令提示符和你的代码编写器(IDE)!!!</strong>

1. 输入以下命令以完成源码和依赖的下载.

   ```shell
   git clone https://github.com/infstellar/genshin_impact_assistant.git&cd genshin_impact_assistant&python setup.py install
   ```

2. 输入以下命令运行程序.

   ```shell
   python genshin_assistant.py
   ```

#### 更新

提供两种方法更新:

- 使用setup.py更新.
   ```shell
   python setup.py update
   ```
- 使用git pull更新.
   ```shell
   git pull
   ```

注意：需要额外解压source/cvAutoTrack_7.2.3/CVAUTOTRACK.7z文件！

### 原神窗口设置

- 需要在原神启动后再运行程序.

- 原神需要以1080p窗口化运行(全屏也可以),设置抗锯齿为SMAA,中或以上特效.

- 窗口焦点应全程在原神窗口上.

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

#### 其他开源库

- [opencv](https://github.com/opencv/opencv)
- [paddleocr](https://github.com/PaddlePaddle/PaddleOCR)
- [yolox](https://github.com/Megvii-BaseDetection/YOLOX)
- [pyinstaller](https://github.com/pyinstaller/pyinstaller)

### 贡献/参与者

- 数据集标注,测试: [nɡ.](https://space.bilibili.com/396023811)

## 声明

- 本软件开源免费,仅供学习交流使用,请勿用于非法用途.使用本软件进行代练的商家所收取的费用均为商家的人工/设备费用,产生的<strong>任何问题</strong>与本软件无关.

## 广告

qq群:[901372518](https://jq.qq.com/?_wv=1027&k=YLTrqlzX)

开发者交流群:[680029885](https://jq.qq.com/?_wv=1027&k=CGuTvCXU)
(请确保你已经会使用git以及github)
