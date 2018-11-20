from cocos.sprite import Sprite

from base import Setting


class Wall(Setting):
    '''墙壁'''
    def __init__(self, x, y, hw=25, hh=25, c=25):
        super().__init__(x, y, hw, hh, c)
        self.anchor = (0, 0)
        s = Sprite('q.png')
        self.add(s)
        self.scale = 0.2
        self.durability = 2 # 耐久度
    
    def get_hit(self):
        self.durability -= 1