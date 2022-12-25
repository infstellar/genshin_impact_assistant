# 从源代码安装

<strong>注意: 这里是从源代码运行,需要一定编程基础.快速使用请参见:
[GIA Launcher自动安装器使用方法](doc/install.md)</strong>

要求:

- python版本[3.7.6](https://www.python.org/downloads/release/python-376/).
- [git](https://git-scm.com/download/win).
- <strong>使用管理员权限打开命令提示符和你的代码编写器(IDE)!!!</strong>

## 安装

1. 输入以下命令以完成源码和依赖的下载:

   ```shell
   git clone https://github.com/infstellar/genshin_impact_assistant.git&cd genshin_impact_assistant&python setup.py install
   ```

2. 输入以下命令运行程序:

   ```shell
   python genshin_assistant.py
   ```

## 更新

提供两种方法更新:

- 使用setup.py更新:
   ```shell
   python setup.py update
   ```
- 使用git pull更新:
   ```shell
   git pull
   ```