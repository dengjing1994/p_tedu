from random import randint

from pyglet.window import key
from cocos.actions import Hide, Show
from cocos.sprite import Sprite
from cocos.euclid import Vector2

from base import Actor, keyboard
from bullet import Bullet


class Tank(Actor):
    '''玩家坦克'''
    def __init__(self, x=0, y=0, hw=20, hh=40, c=15, *args):
        super().__init__(x, y, hw, hh, c)
        self.sprite_list = []
        if len(args) != 4:
            args = ('t0.png', 't1.png', 't2.png', 't3.png')
        self.set_sprite(args)
        self.anchor = (0, 0)
        self.scale = 0.2
        self.cdtime = 0 # 开火剩余cd时间
        self.schedule(self.update_attr) # 每帧调用以更新相关属性

    def set_sprite(self, args):
        for i in args:
            sd = Sprite(i)
            sd.do(Hide())
            self.add(sd)
            self.sprite_list.append(sd)
        self.sprite_list[0].do(Show())

    def fire(self, dt):
        '''开火'''
        if self.cdtime == 0:
            # 剩余cd时间为0时开火，在自身位置产生一个子弹对象，并返回给调用者
            bullet = Bullet(self.cshape_x, self.cshape_y, self.direction, self.hh, self.c)
            self.cdtime = 1 # 进入cd时间
            return bullet

    def move_up(self, dt):
        '''向上移动'''
        for i in self.sprite_list:
            i.do(Hide())
        self.sprite_list[0].do(Show())
        self.direction = 0
        if self.can_move[0]:
            self.cshape_y += 100 * dt

    def move_down(self, dt):
        '''向下移动'''
        for i in self.sprite_list:
            i.do(Hide())
        self.sprite_list[1].do(Show())
        self.direction = 1
        if self.can_move[1]:
            self.cshape_y -= 100 * dt

    def move_left(self, dt):
        '''向左移动'''
        for i in self.sprite_list:
            i.do(Hide())
        self.sprite_list[2].do(Show())
        self.direction = 2
        if self.can_move[2]:
            self.cshape_x -= 100 * dt

    def move_right(self, dt):
        '''向右移动'''
        for i in self.sprite_list:
            i.do(Hide())
        self.sprite_list[3].do(Show())
        self.direction = 3
        if self.can_move[3]:
            self.cshape_x += 100 * dt
    
    def update_attr(self, dt):
        # 计算剩余cd时间
        if self.cdtime > 0:
            self.cdtime -= dt
        else:
            self.cdtime = 0


class Panzer(Tank):
    '''敌方坦克'''
    def __init__(self, x=0, y=400, hw=20, hh=30, c=20, *args):
        super().__init__(x, y, hw, hh, c, *args)
        for i in self.sprite_list:
            i.color = (255, 0, 255)
        self.ai_direction = [1, 0, 0, 0]
        self.schedule(self.ai_move)
    
    def ai_move(self, dt):
        '''简易ai移动判断'''
        if self.ai_direction[0]:
            if self.can_move[0] and not self.cshape_y >= 1300:
                self.move_up(dt)
            else:
                if randint(0, 1) == 0:
                    self.ai_direction = [0, 0, 1, 0]
                else:
                    self.ai_direction = [0, 0, 0, 1]
        elif self.ai_direction[1]:
            if self.can_move[1] and not self.cshape_y <= 0:
                self.move_down(dt)
            else:
                if randint(0, 1) == 0:
                    self.ai_direction = [0, 0, 1, 0]
                else:
                    self.ai_direction = [0, 0, 0, 1]
        elif self.ai_direction[2]:
            if self.can_move[2] and not self.cshape_x <= 0:
                self.move_left(dt)
            else:
                if randint(0, 1) == 0:
                    self.ai_direction = [1, 0, 0, 0]
                else:
                    self.ai_direction = [0, 1, 0, 0]
        elif self.ai_direction[3]:
            if self.can_move[3] and not self.cshape_x >= 1300:
                self.move_right(dt)
            else:
                if randint(0, 1) == 0:
                    self.ai_direction = [1, 0, 0, 0]
                else:
                    self.ai_direction = [0, 1, 0, 0]