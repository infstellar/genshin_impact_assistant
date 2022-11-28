# 安装方法

GIA提供了自动安装更新器。

1. 在release中下载最新版GIAInstaller.7z并解压

2. 配置installer.json文件。配置方法：

| 项目                  | 内容                                                                                                                                          |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| RequirementsFile    | requirements.txt文件位置                                                                                                                        |
| InstallDependencies | 是否安装依赖文件，默认为True                                                                                                                            |
| PypiMirror          | Pypi镜像网站，国内用户需要设置为 `https://pypi.tuna.tsinghua.edu.cn/simple` 或其他国内镜像源。                                                                     |
| Repository          | 仓库地址。默认为 `https://github.com/infstellar/genshin_impact_assistant` ，国内用户可设置为 `https://gitee.com/infstellar/genshin_impact_assistant` 加速访问速度。 |
| GitProxy            | 开关Git SSL验证。默认为False                                                                                                                        |
| KeepLocalChanges    | 保持本地文件更改。默认为True                                                                                                                            |
| AutoUpdate          | 自动更新。默认为True                                                                                                                                |
| Branch              | 代码下载的分支。有以下分支可供选择：                                                                                                                          |

| Branch       | 内容                                  |
|--------------|-------------------------------------|
| main         | 默认主分支，稳定版本                          |
| beta_version | 测试版本                                |
| bug_fix      | 最新bug修复版本。如遇到bug并已经提交解决，可以切换到该分支测试。 |
 
3. 以管理员权限运行GIAStart.exe
