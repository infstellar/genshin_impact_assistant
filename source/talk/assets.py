from source.manager import asset
from source.util import *

ButtonTalkSkip = asset.Button(threshold=0.99)
ButtonTalkSkip_Force = asset.Button(name="ButtonTalkSkip", threshold=0, click_offset=[-120,0])
AreaTalkSelects = asset.Area()
Expedition = asset.TextTemplate(text={'zh_CN': '探索派遣',"en_US": "Expedition"})