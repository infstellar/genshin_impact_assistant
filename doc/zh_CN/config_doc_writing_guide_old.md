# 配置文档书写指南

## 命名格式

名称一般为目标文档的名字加上`{语言}.jsondoc`的后缀.

例如`auto_domain.json`对应的文档名应为`auto_domain.json.zh_CN.jsondoc`.

## 存储位置

应按命名规范存储在对应配置同目录下.

## 单层dict

如果文档是单层的dict的话,最简单的办法就是把json文件拷贝一份,并把值改为你想要的文字.
例如:

```json
{
  "domain_times": 1,
  "fast_mode": true,
  "isLiYueDomain": false,
  "resin": "20"
}
```

改为

```json
{
  "domain_times": "秘境探险次数",
  "fast_mode": "快速模式",
  "isLiYueDomain": "是否为璃月副本",
  "resin": "树脂"
}
```

## 嵌套dict

在json的书写中不可避免的会出现嵌套的dict,当然,在一开始考虑到了这一点.
在书写时只需在值内填写:

``` json
{"doc": "你的文本","data":<嵌套的dict>}
```

例子:

```json
{
  "bennett": {
    "E_long_cd_time": 10,
    "E_short_cd_time": 3,
    "Elast_time": 0
  }
}
```

应写成:

```json
{
  "bennett": {
    "doc": "班尼特",
    "data": {
      "E_long_cd_time": "元素战技长CD",
      "E_short_cd_time": "元素战技短CD",
      "Elast_time": "上次施展元素战技的时长"
    }
  }
}
```

## 选择框

以前想过这个问题,不过觉得应该可以不用就没写,这次看来是必须写了..

和上边一样,选择框只需要在dict里加入一个名为`select_items`的项就行了.

例如:

```json
{
  "itemname": {
    "select_items": [
      "甜甜花 - 蒙德",
      "霓裳花 - 璃月",
      "鸣草 - 稻妻"
    ],
    "doc": "物品名"
  }
}
```

## 其他

- 如果你觉得有一些不必要翻译那可以删掉键值对,程序会自动使用配置的值作为标题.
- <strong>请不要写入无法解析的json文档!!!</strong>

