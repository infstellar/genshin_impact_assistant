# Install from source

```
Portions of this document may be machine translated.
```

<strong>Note: This is to run from the source code, which requires a certain programming foundation. For quick use, please refer to:
[How to use GIA Launcher automatic installer](install.md)</strong>

Require:

- python version [3.7.6](https://www.python.org/downloads/release/python-376/).
- [git](https://git-scm.com/download/win).
- <strong>Open a command prompt and your code writer (IDE) with admin privileges!!!</strong>

## Install

1. Enter the following command to complete the download of source code and dependencies:

    ```shell
    git clone https://github.com/infstellar/genshin_impact_assistant.git&cd genshin_impact_assistant&python setup.py install
    ```

2. Enter the following command to run the program:

    ```shell
    python genshin_assistant.py
    ```

## renew

There are two ways to update:

- Update with setup.py:
    ```shell
    python setup.py update
    ```
- update with git pull:
    ```shell
    git pull
    ```