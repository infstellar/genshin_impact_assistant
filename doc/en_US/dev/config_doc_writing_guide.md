# 配置文档书写指南

## 命名格式

名称一般为目标文档的名字加上`{语言}.jsondoc`的后缀.

例如`auto_domain.json`对应的文档名应为`auto_domain.json.zh_CN.jsondoc`.

## 存储位置

应按命名规范存储在对应配置同目录下.

## 翻译

把键对应的翻译写入doc内.例如:

```yaml
{
  domain_times: 
    doc: 1


  fast_mode:
    doc: true


  isLiYueDomain: 
    doc: false,
  resin: 
    doc: 20
}
```

## 选择框

以前想过这个问题,不过觉得应该可以不用就没写,这次看来是必须写了..

和上边一样,选择框只需要在yaml里加入一个名为`select_items`的项就行了.

例如:

```yaml

  itemname: 
    select_items: [
      甜甜花 - 蒙德,
      霓裳花 - 璃月,
      鸣草 - 稻妻
    ],
    doc: 物品名

```

## Special Key

用于执行特殊方法的标记，包括


## 其他

- 如果你觉得有一些不必要翻译那可以删掉键值对,程序会自动使用配置的值作为标题.
- <strong>请不要写入无法解析的yaml文档!!!</strong>

