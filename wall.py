from cocos.sprite import Sprite

from base import Setting


class Wall(Setting):
    '''墙壁'''
    def __init__(self, x, y, hw=25, hh=25, c=25):
        super().__init__(x, y, hw, hh, c)
        self.anchor = (0, 0)
        self.get_sprite()
        self.scale = 0.2
        self.durability = 2 # 耐久度
    
    def get_hit(self):
        self.durability -= 1
    
    def get_sprite(self):
        s = Sprite('pic/q.png')
        self.add(s)


class Iron(Wall):
    def __init__(self, x, y, hw=50, hh=50, c=50):
        super().__init__(x, y, hw, hh, c)
        self.scale = 0.4
    
    def get_hit(self):
        pass
    
    def get_sprite(self):
        s = Sprite('pic/q.png')
        s.color = (255, 0, 0)
        self.add(s)