from cocos.sprite import Sprite
from cocos.collision_model import AARectShape
from cocos.euclid import Vector2

from base import Actor


class Bullet(Actor):
    '''炮弹'''
    def __init__(self, x, y, direction, m, c=0, hw=20, hh=20):
        if direction == 0:
            y += m
        elif direction == 1:
            y -= m
        elif direction == 2:
            x -= m
        elif direction == 3:
            x += m
        super().__init__(x, y, hw, hh, 2*c)
        s = Sprite('zidan.png')
        self.add(s)
        self.anchor = (0, 0)
        self.scale = 0.1
        self.direction = direction
        self.schedule(self.move)

    def move(self, dt):
        '''炮弹移动'''
        # 判断方向并进行移动
        if self.direction == 0:
            self.cshape_y += 300 * dt
            # self.rotation = 0
        elif self.direction == 1:
            self.cshape_y -= 300 * dt
            self.rotation = 180
        elif self.direction == 2:
            self.cshape_x -= 300 * dt
            self.rotation = -90
        elif self.direction == 3:
            self.cshape_x += 300 * dt
            self.rotation = 90