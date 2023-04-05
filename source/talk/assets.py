from source.manager import asset
from source.util import *

ButtonTalkSkip = asset.Button(path=fr"{ROOT_PATH}\assets\imgs\Windows\Talk\ButtonTalkSkip.jpg", threshold=0.99)
ButtonTalkSkip_Force = asset.Button(path=fr"{ROOT_PATH}\assets\imgs\Windows\Talk\ButtonTalkSkip.jpg", threshold=0, click_offset=[-120,0])
AreaTalkSelects = asset.PosiTemplate()
Expedition = asset.TextTemplate(text={'zh_CN': '探索派遣',"en_US": "Expedition"})