# 安装方法

GIA provides an automatic installer/updater.

# GIA Auto Install Launcher

## Download

[GIA Launcher v0.6](https://github.com/infstellar/genshin_impact_assistant/releases/download/v0.6.0-beta.542/GIA_Launcher_v0.6.0.7z)
Note: If you have previously downloaded the v0.3 launcher, you will need to delete all files (but not the toolkit folder, to skip duplicate installation dependencies) before launching the new launcher.

## How to use

Double click on `GIA Launcher.exe` to run it.

## Configuration file

对中国用户来说，可以使用`installer_config_cn.json`配置文件，已经根据中国特色网络环境进行了单独配置。

使用方法：删除`installer_config.json`，保留`installer_config_cn.json`即自动启用`installer_config_cn.json`。

Specific configuration.

| name | content |
|---------------------|-----------------------------|
| RequirementsFile | requirements.txt file location |
| InstallDependencies | Whether to install dependencies, default is true |
| PypiMirror | Pypi mirror site. |
| Repository          | 仓库地址。默认为 `https://github.com/GenshinImpactAssistant/GIA_Launcher_Download_Lib` ，国内用户可设置为 `https://gitee.com/GenshinImpactAssistant/GIA_Launcher_Download_Lib` 加速访问速度。 |
| GitProxy | Switch Git SSL authentication. Defaults to false. |
| KeepLocalChanges | Keeps local changes to files. Defaults to false |
| AutoUpdate | Update automatically. Defaults to true |
| Branch | The branch where the code will be downloaded. The following branches are available: |

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

