from cocos.sprite import Sprite

from base import Setting


class Wall(Setting):
    '''墙壁'''
    def __init__(self, x, y, hw=50, hh=50, c=50):
        super().__init__(x, y, hw, hh, c)
        self.anchor = (0, 0)
        s = Sprite('q.png')
        self.add(s)
        self.scale = 0.4