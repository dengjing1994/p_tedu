from cocos.sprite import Sprite
from cocos.collision_model import AARectShape
from cocos.euclid import Vector2

from base import Actor


class Bullet(Actor):
    '''炮弹'''
    def __init__(self, x, y, direction, m, c=0, hw=20, hh=20, *args):
        if direction == 0:
            y += m
        elif direction == 1:
            y -= m
        elif direction == 2:
            x -= m
        elif direction == 3:
            x += m
        super().__init__(x, y, hw, hh, 2*c)
        if len(args) != 4:
            args = ('pic/zidan0.png', 'pic/zidan1.png', 'pic/zidan2.png', 'pic/zidan3.png')
        self.s = Sprite(args[direction])
        self.add(self.s)
        self.anchor = (0, 0)
        self.scale = 0.1
        self.direction = direction
        self.schedule(self.move)

    def move(self, dt):
        '''炮弹移动'''
        # 判断方向并进行移动
        if self.direction == 0:
            self.cshape_y += 300 * dt
        elif self.direction == 1:
            self.cshape_y -= 300 * dt
        elif self.direction == 2:
            self.cshape_x -= 300 * dt
        elif self.direction == 3:
            self.cshape_x += 300 * dt


class Bullet_t1(Bullet):
    def __init__(self, *args):
        super().__init__(*args)
        self.s.color = (255, 0, 0)