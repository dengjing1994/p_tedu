from random import randint

from pyglet.window import key
from cocos.actions import Hide, Show
from cocos.sprite import Sprite
from cocos.euclid import Vector2

from base import Actor, keyboard
from bullet import Bullet, Bullet_t1


class Tank(Actor):
    '''玩家坦克'''
    def __init__(self, x=0, y=0, hw=20, hh=40, c=15, *args):
        super().__init__(x, y, hw, hh, c)
        self.sprite_list = []
        if len(args) != 4:
            args = ('pic/t0.png', 'pic/t1.png', 'pic/t2.png', 'pic/t3.png')
        self.set_sprite(args)
        self.anchor = (0, 0)
        self.scale = 0.2
        self.cdtime = 0 # 开火剩余cd时间
        # 弹药选择
        self.b_list = [Bullet, Bullet_t1]
        self.b_level = 0
        # 血条
        self.durability = 3
        self.add_lifebar()
        self.schedule(self.update_attr) # 每帧调用以更新相关属性
        self.schedule(self.update_lifebar) # 更新血条

    def set_sprite(self, args):
        for i in args:
            sd = Sprite(i)
            sd.do(Hide())
            self.add(sd)
            self.sprite_list.append(sd)
        self.sprite_list[self.direction].do(Show())

    def fire(self, dt):
        '''开火'''
        if self.cdtime == 0:
            # 剩余cd时间为0时开火，在自身位置产生一个子弹对象，并返回给调用者
            bullet = self.b_list[self.b_level](self.cshape_x, self.cshape_y, self.direction, self.hh, self.c)
            self.cdtime = 1 # 进入cd时间
            # self.b_level = (self.b_level + 1) % 2 # 测试换炮弹
            return bullet
    
    def add_lifebar(self):
        p_list = ['pic/life01.png', 'pic/life02.png', 'pic/life03.png', 'pic/life04.png']
        self.lifebar_list = []
        for i in range(4):
            lifebar = Sprite(p_list[i])
            lifebar.anchor = (0, 0)
            lifebar.scale_x = 3
            lifebar.scale_y = 5
            lifebar.y += 300
            lifebar.do(Hide())
            self.lifebar_list.append(lifebar)
            self.add(lifebar)
        self.lifebar_list[3 - self.durability].do(Show())
    
    def get_hit(self):
        self.durability -= 1
    
    def update_lifebar(self, dt):
        for i in self.lifebar_list:
            i.do(Hide())
        self.lifebar_list[3 - self.durability].do(Show())

    def move_up(self, dt):
        '''向上移动'''
        if self.can_move[0] and self.direction == 0:
            self.cshape_y += 100 * dt
        for i in self.sprite_list:
            i.do(Hide())
        self.sprite_list[0].do(Show())
        self.direction = 0

    def move_down(self, dt):
        '''向下移动'''
        if self.can_move[1] and self.direction == 1:
            self.cshape_y -= 100 * dt
        for i in self.sprite_list:
            i.do(Hide())
        self.sprite_list[1].do(Show())
        self.direction = 1

    def move_left(self, dt):
        '''向左移动'''
        if self.can_move[2] and self.direction == 2:
            self.cshape_x -= 100 * dt
        for i in self.sprite_list:
            i.do(Hide())
        self.sprite_list[2].do(Show())
        self.direction = 2

    def move_right(self, dt):
        '''向右移动'''
        if self.can_move[3] and self.direction == 3:
            self.cshape_x += 100 * dt
        for i in self.sprite_list:
            i.do(Hide())
        self.sprite_list[3].do(Show())
        self.direction = 3
    
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
        self.durability = 1
    
    def add_lifebar(self):
        self.lifebar = Sprite('pic/life01.png')
        self.lifebar.anchor = (0, 0)
        self.lifebar.scale_x = 2
        self.lifebar.scale_y = 5
        self.lifebar.y += 300
        self.add(self.lifebar)
    
    def update_lifebar(self, dt):
        pass


def ai_move(panzer, dt):
    '''简易ai移动判断'''
    if panzer.ai_direction[0]:
        if panzer.can_move[0] and not panzer.cshape_y >= 1300:
            panzer.move_up(dt)
        else:
            if randint(0, 1) == 0:
                panzer.ai_direction = [0, 0, 1, 0]
            else:
                panzer.ai_direction = [0, 0, 0, 1]
    elif panzer.ai_direction[1]:
        if panzer.can_move[1] and not panzer.cshape_y <= 0:
            panzer.move_down(dt)
        else:
            if randint(0, 1) == 0:
                panzer.ai_direction = [0, 0, 1, 0]
            else:
                panzer.ai_direction = [0, 0, 0, 1]
    elif panzer.ai_direction[2]:
        if panzer.can_move[2] and not panzer.cshape_x <= 0:
            panzer.move_left(dt)
        else:
            if randint(0, 1) == 0:
                panzer.ai_direction = [1, 0, 0, 0]
            else:
                panzer.ai_direction = [0, 1, 0, 0]
    elif panzer.ai_direction[3]:
        if panzer.can_move[3] and not panzer.cshape_x >= 1300:
            panzer.move_right(dt)
        else:
            if randint(0, 1) == 0:
                panzer.ai_direction = [1, 0, 0, 0]
            else:
                panzer.ai_direction = [0, 1, 0, 0]
    
