# 简体中文 | Simplified Chinese

# 安装方法

GIA提供了自动安装/更新器。

# GIA 自动安装启动器

## 下载

[GIA Launcher v0.6](https://github.com/infstellar/genshin_impact_assistant/releases/download/v0.6.0-beta.542/GIA_Launcher_v0.6.0.7z)
注意：如果你之前下载了v0.3版本的启动器，需要全部删除(toolkit文件夹可不删除，跳过重复安装依赖)所有文件后再启动新的启动器。

## 使用方式

双击`GIA Launcher.exe`运行。

## 配置文件

对中国用户来说，可以使用`installer_config_cn.json`配置文件，已经根据中国特色网络环境进行了单独配置。

使用方法：删除`installer_config.json`，保留`installer_config_cn.json`即自动启用`installer_config_cn.json`。

具体配置：

| 项目                  | 内容                                    |
|---------------------|-----------------------------|
| RequirementsFile    | requirements.txt文件位置                  |
| InstallDependencies | 是否安装依赖文件，默认为true                      |
| PypiMirror          | Pypi镜像网站，国内用户需要设置为 `https://pypi.tuna.tsinghua.edu.cn/simple` 或其他国内镜像源。                  |
| Repository          | 仓库地址。默认为 `https://github.com/infstellar/genshin_impact_assistant` ，国内用户可设置为 `https://gitee.com/infstellar/genshin_impact_assistant` 加速访问速度。 |
| GitProxy            | 开关Git SSL验证。默认为false                  |
| KeepLocalChanges    | 保持本地文件更改。默认为false                     |
| AutoUpdate          | 自动更新。默认为true                          |
| Branch              | 代码下载的分支。有以下分支可供选择：                    |

| Branch       | 内容         |
|--------------|------------|
| main         | 默认主分支，稳定版本 |
| beta_version | 测试版本       |
| dev          | 开发中版本      |

# English | 英文

# Installation method

GIA provides an automatic installer/updater.

# GIA Auto Install Launcher

## Download

[GIA Launcher v0.6](https://github.com/infstellar/genshin_impact_assistant/releases/download/v0.6.0-beta.542/GIA_Launcher_v0.6.0.7z)
Note: If you have previously downloaded the v0.3 launcher, you will need to delete all files (but not the toolkit folder, to skip duplicate installation dependencies) before launching the new launcher.

## How to use

Double click on `GIA Launcher.exe` to run it.

## Configuration file

Specific configuration.

| project | content |
|---------------------|---------------------|
| RequirementsFile | requirements.txt file location |
| InstallDependencies | Whether to install dependencies, default is true |
| PypiMirror | Pypi mirror site, for domestic users set to `https://pypi.tuna.tsinghua.edu.cn/simple` or other domestic mirror source.    |
| Repository | The address of the repository. Default is `https://github.com/infstellar/genshin_impact_assistant`, domestic users can set it to `https://gitee.com/infstellar/genshin_impact_assistant` to speed up access. |
| GitProxy | Switch Git SSL authentication. Defaults to false |
| KeepLocalChanges | Keeps local changes to files. Defaults to false |
| AutoUpdate | Update automatically. Defaults to true |
| Branch | The branch where the code will be downloaded. The following branches are available: |

| Branch | Contents |
|--------------|------------|
| main | Default main branch, stable version |
| beta_version | test_version |
| dev | Under development |