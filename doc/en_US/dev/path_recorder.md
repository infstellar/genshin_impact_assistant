# 路径记录器

位置：flow/path_recorder_flow.py

## Usage

### 加载

1. 运行path_recorder_flow.py。

2. 等待加载，会出现`input your path name`提示，输入你的path名。

3. 等待提示`Load over.` `ready to start.` 即准备完成。

### 运行

1. 按下`\`键，提示`ready to start recording`。如果没有，就再按一次。
2. 一通操作后，提示`start recording`,就可以开始移动了。
3. 移动时，所有的坐标会被记录。同时，角色的动作状态（行走，爬山等）也会被记录。
3. 按下某些按键时，程序会记录下来。包括以下按键：`space` `f` `lshift` 等。但并非所有记录的按键都会被执行。
3. 角色移动方向改变超过3°时，会记录一次break position。break position之间的距离最小为5。
4. 走完之后，再次按下`\`键。提示`ready to stop recording`。
5. 在1秒内应该会提示`recording save as {jsonname}`。如果没有，就再按一次`\`。
6. json文件将在`assets/TeyvatMovePath`保存为`name+timestamp.json`。如果想继续记录，就重复这些步骤。

