# GUI

GIA 的GUI由PyWebIO实现。包含以下功能：

- 选择自动辅助模式，状态显示

- 启动/停止

- 设置配置

- 远程操作

## 功能使用

### Task
Task是GIA执行的基本模块，所有的全自动功能从Task里启动。

启动时，在对应功能的复选框打钩，然后按下按钮。停止时按下同样按钮。

### Mission
Mission是GIA中在大世界执行功能的便携集成化单元，使用统一的接口，编写简单。

Mission可以实现的功能包括采集、战斗、NPC对话(正在制作)与行走。通过功能的组合可以实现固定路线采集、任务自动化等功能。

Mission的组织调用形式是MissionGroup。一个MissionGroup可以包括多个Mission和MissionGroup。在Main界面选择要进行的MissionGroup，然后在Task里启动Mission就可以运行MissionGroup。MissionGroup的下方有该Group功能的简单介绍。

## 辅助功能

辅助功能是一些半自动的功能模块，能够自动辅助部分操作。

在原神中按下快捷键(默认为`[`)即可启动/停止。

## 设置配置

在设置页面可以配置设置。

在下拉框中选择要配置的文件，按照提示配置。

## 远程操作

在`main`界面按下`获取ip`即可获取局域网连接ip，可以在电脑上输入该ip，连接到GIA控制面板，操作另一台电脑上的GIA。


