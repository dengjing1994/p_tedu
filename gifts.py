'''设置地图上出现的坦克生命，子弹升级等'''
from cocos.sprite import Sprite
from base import Setting

class Gifts(Setting):
    '''给玩家回血的物体'''
    def __init__(self, x, y, hw=25, hh=25, c=25):
        super().__init__(x, y, hw, hh, c)
        self.anchor = (0, 0)
        self.get_sprite()
        self.scale = 0.1
    
    def get_sprite(self):
        s = Sprite('pic/lipin.png')
        self.add(s)


