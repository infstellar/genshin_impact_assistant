# 流程控制单元

## FlowTemplate

基本流程单元。

### 基本概念：
Flow id: 存储于模块ST。

Flow Code: 存储于模块FC。

```python
class FlowTemplate():
    def __init__(self, upper:FlowConnector, flow_id:int, next_flow_id:int, flow_timeout_time:float = -1):
```

介绍：
upper：流程连接器（FlowConnector）单元。

flow_id: 流程代码：

## 流程代码

以自动秘境为例，它有以下流程码：

MOVETO_CHALLENGE

CHALLENGE

GETTING_REAWARD

FINGING_TREE

MOVETO_TREE

ATTAIN_REAWARD

END_DOMAIN

其中，终止流程码必须包含$END$字符。

所有流程码管理在flow/flow_state.py中。

next_flow_id: 该流程结束后运行的下一个流程的Flow id

flow_timeout_time: 流程超时时间。负数则为无限。


变量：

rfc：return flow code。有以下6个值：0,1,2,3,4,5

0~4: 对应state_init, state_before, state_in, state_after, state_end。即FC.INIT, FC.BEFORE, FC.IN, FC.AFTER, FC.END.

5: 流程结束标志码。即FC.OVER

### 状态执行函数：
state_init, state_before, state_in, state_after, state_end。

其中，state_init与state_end为单次执行函数，即在一个Flow单元中的一次执行中只执行一次。

state_before和state_after可以来回切换，例如：

```python
def state_after(self):
    ...
    self._set_rfc(FC.BEFORE)
```
从而切换回before状态。

state_in是循环状态，即如果该流程的一些代码需要循环执行，写在这里。

最后，上面的规则仅为建议和标准，不遵守也不会出错，只是方便维护。

如果你不需要某个状态，不在继承的类里实现它就好了。但是，state_in必须实现。

每个状态实现后，如果要切换到下一个state，必须使用```self._next_rfc()```。手动```self._set_rfc(x)```也是可以的。

函数清单：

|name|func|
|----|----|
|_next_rfc()|切换到下一个FlowCode|
|_before_timeout()|在函数超时之前做点什么|
|_set_nfid()|设置下一个流程id|

## FlowConnector

流程连接器。

所有的流程变量都应该存放在这里，方便重置与设置。

一个FlowController必须有且仅有一个FlowConnector。

## FlowController

流程控制器。

流程的主程序，控制流程流动。

```python
class FlowController(base_threading.BaseThreading):
    def __init__(self, flow_connector:FlowConnector, current_flow_id):
```
flow_connector: FlowConnector对象。

current_flow_id: 初始流程id。

函数清单：

|name|func|
|----|----|
|append_flow()|添加一个FlowTemplate到流程执行列表中|
|_err_code_exec()|错误码分析|
|set_current_flow_id()|设置流程id|

## EndFlowTemplate

同FlowTemplate。区别是

1. 需要填写err_code。ERR_PASS即为无错误。
2. 流程ID必须包含$END$。



