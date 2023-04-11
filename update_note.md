## TODO：
- webui list的显示要改改
- 自动战斗预启动
- 自动战斗的e技能释放有延迟，可能是计时器问题
- 秘境开局会点两下 原神动画问题
- 自动战斗boss血条不动
- 检测。。。按钮识别是采集物还是人
- move straight在移动视角前按下了w
- aim operator move to enemy按空格
- 让sco get_characters_name()在continue时获得charalist
- tactic默认配置不要用json template
- ocr在角色名字时试试用in
- BigPudgyProblem需要对话

## Done：
- config的名字全部改成首字母大写，去掉下划线 pass
- jsontemplate与json分离 pass
- jsondoc的其他配置项与i18n分离,或者在加载时合并common与i18n两个jsondoc pass
- 合并aim与combat pass
- 合并pickup与collect pass
- collet增加一个在半径内逛街找敌人的功能 pass
- 游泳的usd有bug pass
- chara waiting增加更有效的usd。游泳、爬山、空格。 pass
- 秘境ocr结果输出 pass
- ui切换太慢 pass
- 太靠近地图边界会切换角色失败 pass
- QQ人哨塔可以识别委托标志去打 pass
- 每日委托图片不够靠近中心 pass
- auto combat的shield模式有bug pass
- QQ人哨塔可以识别委托标志下面的距离 pass
- 蒙德传送点太多扫不到锚点 pass

## Notice：
- 太靠近地图边界会切换角色失败 alpha问题
- 更新后设置部分丢失
- 更新后tactic的默认配置变为只读