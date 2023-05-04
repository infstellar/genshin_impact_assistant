# Auto collector Assist

- Note: After v0.6.1, Auto Collector wan changed from Flow to Mission.

## Introduction

Auto Collector Assist can automatically acquire most of the materials in Teyvat World such as gatherables, loot, etc.

Example: Automatic collect sweet flowers, automatic kill Silme.

This function intergrates Auto Combat Assist, Auto Move Assist, Auto Pickup Assist. Make sure you have read the information about them before using.

## Function Introduction

- Specify the collection, GIA will select the cloest collection from the database and start-up.

- Can collect resource/enemy

- Automatic continuous collect

- Revive at the State when somebody died.

## Quick Start

Set the paramaters at the Collector.json.

Start the Auto Collector from the GUI.

## 参数设置

- 推荐在GUI中编辑

| key         | item             |
|-------------|------------------|
| collection_name        | 需要采集的物品名称             |
| collection_type    | 采集的物品类型，分为`COLLECTION`（一般采集物）和`ENEMY`（战斗掉落物）|
| minimum_times_mask_col_id | 自动生成黑名单时，采集失败次数超过该值即录入黑名单，不再采集|

## 采集日志

采集日志(collection_log.json)是自动采集辅助产生的日志文件，包括：

| key         | item             |
|-------------|------------------|
| time        | 采集时间             |
| id          | 该类型掉落物id         |
| error_code  | 退出原因             |
| picked item | 在该次采集过程中采集到的所有物品 |

## 采集物选择优先级

采集物有多个地点时，按照历史采集成功率和距离远近加权计算。

## 已采集地点

已采集地点(collected.json)保存了采集过的物品的id。自动生成。

## 黑名单设置

在对应项的列表中加入id即可屏蔽这些采集项。

如果有些id的采集常常失败，可以加入黑名单，在下次采集时将会自动跳过。

