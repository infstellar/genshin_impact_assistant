# genshin_impact_assistant 原神助手  

多功能原神自动辅助操作，包括自动战斗，自动刷秘境。不用每天原神半小时清体力了(*´▽｀)ノノ

# 介绍

基于图像识别的原神自动操作辅助。使用图片识别与模拟键盘操作，不涉及违规操作。

## 目前功能

### 1. [自动战斗辅助](./doc/combat_assi.md)

### 2. [自动秘境战斗](./doc/domain_assi.md)

## 使用方法

### 下载与安装

1. 下载`tag`里最新版本的`genshin_assistant.zip`并解压，之后每次更新只需要重新下载`genshin_assistant.zip`即可。
2. 下载`tag`里的`environment_all.7z`,并全部复制到解压后的`genshin_assistant`目录中,选择全部替换。

    如果environment_all.7z下载过慢，也可以下载environment_no_torch.7z,并自行下载torch复制到目录中(或者加入q群下载
3. 启动原神后，以管理员权限运行`genshin_assistant.exe`

### 原神窗口设置

- 需要在原神启动后再运行程序
- 原神需要以1080p窗口化运行，设置抗锯齿为SMAA，低特效。

### config设置

参考[config设置](./doc/config.md)

### 为什么文件这么多

神奇的python需要打包所有运行环境到一起才能启动 T_T 实际上是个python虚拟机

## 性能需求

- 程序需要至少1.5G内存与至少6G存储空间。

## 致谢

### 开源库

- [opencv](https://github.com/opencv/opencv)
- [paddleocr](https://github.com/PaddlePaddle/PaddleOCR)
- [yolox](https://github.com/Megvii-BaseDetection/YOLOX)
- [GenshinImpact_AutoTrack](https://github.com/GengGode/GenshinImpact_AutoTrack_DLL)
- [pyinstaller](https://github.com/pyinstaller/pyinstaller)

### 贡献/参与者

- 数据集标注，测试： [nɡ.](https://space.bilibili.com/396023811)

## 声明

- 本软件开源、免费，仅供学习交流使用。若您遇到商家使用本软件进行代练并收费，可能是设备与时间等费用，产生的问题及后果与本软件无关。
