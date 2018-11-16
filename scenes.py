from random import random, randrange
from pyglet.window import key
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.collision_model import CollisionManagerGrid
from cocos.sprite import Sprite

from tanks import *
from base import keyboard
from bullet import Bullet
from wall import Wall
from settings import wall_list
from explosion import Explosion


class MajorLayer(Layer):

    is_event_handler = False

    def __init__(self):
        super().__init__()
        # 设置中心点为屏幕中心
        self.center = (director.get_window_size()[0] / 2, director.get_window_size()[1] / 2)
        # 添加背景层
        self.add(BgLayer(), z=0)
        # 设置存储对象的字典、集合和列表
        self.enermy_dict = {}
        self.bullet_dict = {}
        self.bullet_dicte = {}
        self.wall_dict = {}
        self.toremove = set()
        self.blocking_pair = []
        # 设置敌方坦克数量
        self.totle_enermy_num = 25
        self.active_enermy_num = 0
        self.enermy_point_list = [(1250, 50), (1250, 650), (1250, 1250)]
        # 设置碰撞管理对象
        self.collman = CollisionManagerGrid(0, 1300,
                                            0, 1300,
                                            10, 10)
        # 计分板
        self.score = 0
        # 增加墙壁
        self.add_wall()
        # 添加我方坦克
        self.add_player()
        # 每帧调用方法
        self.schedule(self.key)
        self.schedule(self.collisons_test)
        self.schedule(self.update)
        self.schedule(self.boundary)
        self.schedule(self.out_range_bullet)
        # 每5秒试图添加敌人
        self.schedule_interval(self.add_enermy, 5)
        # 每隔一段时间给ai下达指令
        self.schedule_interval(self.ai_move, 3)
        self.schedule_interval(self.ai_fire, 1)
    
    def add_wall(self):
        for i in wall_list:
            w = Wall(*i)
            self.wall_dict[w] = str(w)
            self.add(w, z=w.z, name=self.wall_dict[w])

    def add_player(self):
        self.tank = Tank(50, 450)
        self.add(self.tank, z=self.tank.z, name='p1')

    def ai_move(self, dt):
        # 调整ai运动方向
        for p in self.enermy_dict:
            p.ai_direction = [0, 0, 0, 0]
            i = randrange(0, 4)
            p.ai_direction[i] = 1
    
    def ai_fire(self, dt):
        # ai开火
        for p in self.enermy_dict:
            if random() > 0.75:
                b = p.fire(dt)
                if b:
                    self.bullet_dicte[b] = str(b)
                    self.add(b, z=b.z, name=self.bullet_dicte[b])

    def add_enermy(self, dt):
        '''添加敌人'''
        if self.totle_enermy_num and self.active_enermy_num < 7:
            i = self.totle_enermy_num % 3
            # 当仍有可用敌人数量时，添加敌人
            enermy = Panzer(*self.enermy_point_list[i])
            self.enermy_dict[enermy] = str(enermy)
            self.add(enermy, z=enermy.z, name=self.enermy_dict[enermy])
            # 可用敌人数量减1
            self.totle_enermy_num -= 1
            self.active_enermy_num += 1

    def update(self, dt):
        '''更新图像位置，保证玩家在屏幕中间'''
        self.x = self.center[0] - self.tank.x
        self.y = self.center[1] - self.tank.y

    def key(self, dt):
        '''响应键盘按键'''
        # 空格开火
        if keyboard[key.SPACE]:
            bullet = self.tank.fire(dt)
            if bullet:
                # 开火成功则将炮弹加入self
                self.bullet_dict[bullet] = str(bullet)
                self.add(bullet, z=bullet.z, name=self.bullet_dict[bullet])
        # 移动操作
        if keyboard[key.UP]:
            self.tank.move_up(dt)
        elif keyboard[key.DOWN]:
            self.tank.move_down(dt)
        elif keyboard[key.LEFT]:
            self.tank.move_left(dt)
        elif keyboard[key.RIGHT]:
            self.tank.move_right(dt)
        # 测试用
        if keyboard[key.P]:
            print((self.tank.cshape_x, self.tank.cshape_y), (self.tank.x, self.tank.y))
        if keyboard[key.O]:
            print(self.get_children())
    
    def collisons_test(self, dt):
        '''碰撞相关检测'''
        # 当一对坦克不再碰撞时，解除移动限制
        for t1, t2, n in self.blocking_pair:
            if not self.collman.they_collide(t1, t2):
                if n == 0:
                    t1.can_move[2] = 1
                    t2.can_move[3] = 1
                elif n == 1:
                    t1.can_move[3] = 1
                    t2.can_move[2] = 1
                elif n == 2:
                    t1.can_move[1] = 1
                    t2.can_move[0] = 1
                elif n == 3:
                    t1.can_move[0] = 1
                    t2.can_move[1] = 1
        # 清空碰撞管理对象
        self.collman.clear()
        # 把各种对象加入碰撞管理对象中
        self.collman.add(self.tank)
        for p in self.enermy_dict:
            self.collman.add(p)
        for b in self.bullet_dict:
            self.collman.add(b)
        for b in self.bullet_dicte:
            self.collman.add(b)
        for w in self.wall_dict:
            self.collman.add(w)
        # 判断发生哪些碰撞
        for o1, o2 in self.collman.iter_all_collisions():
            # 判断o1是否为炮弹
            if isinstance(o1, Bullet):
                if o1 in self.bullet_dict and o2 is self.tank:
                    # 若为己方炮弹和己方坦克则无影响
                    pass
                elif o1 in self.bullet_dicte and o2 in self.enermy_dict:
                    pass
                else:
                    # 否则将双方加入销毁列表
                    self.toremove.add(o1)
                    self.toremove.add(o2)
            # 判断o2是否为炮弹
            elif isinstance(o2, Bullet):
                if o2 in self.bullet_dict and o1 is self.tank:
                    pass
                elif o2 in self.bullet_dicte and o1 in self.enermy_dict:
                    pass
                else:
                    self.toremove.add(o1)
                    self.toremove.add(o2)
            # 障碍物之间什么也不发生
            elif isinstance(o1, Wall) and isinstance(o2, Wall):
                pass
            # 坦克与障碍物和坦克与坦克的碰撞
            else:
                # 判断碰撞方向，并锁定相应的移动方式
                self.colliding(o1, o2)
                
        # 处理销毁列表中的对象
        for i in self.toremove:
            if isinstance(i, Bullet):
                # 添加爆炸效果
                ep = Explosion(i.cshape_x, i.cshape_y, 20, 20, i.c)
                self.add(ep, z=ep.z)
                if i in self.bullet_dict:
                    self.remove(self.bullet_dict[i])
                    del self.bullet_dict[i]
                else:
                    self.remove(self.bullet_dicte[i])
                    del self.bullet_dicte[i]
            elif isinstance(i, Panzer):
                self.remove(self.enermy_dict[i])
                del self.enermy_dict[i]
                # 爆炸效果
                ep = Explosion(i.cshape_x, i.cshape_y, 20, 20, i.c)
                self.add(ep, z=ep.z)
                # 销毁敌方坦克时，相关数据变动
                self.active_enermy_num -= 1
                self.totle_enermy_num += 1
                self.score += 1
            elif isinstance(i, Tank):
                self.remove('p1')
                # 爆炸效果
                ep = Explosion(i.cshape_x, i.cshape_y, 20, 20, i.c)
                self.add(ep, z=ep.z)
                # 玩家重生
                self.add_player()
        # 清空销毁列表
        self.toremove.clear()
    
    def boundary(self, dt):
        '''地图边界判断'''
        # 把已有坦克全部放进列表
        actor_list = []
        actor_list.append(self.tank)
        for p in self.enermy_dict:
            actor_list.append(p)
        # 依次判断坦克是否到达边界
        for p in actor_list:
            if p.cshape_x >= 1300:
                # 超过边界时，锁定相应坐标，使坦克不能继续移动
                p.cshape_x = 1300
            elif p.cshape_x <= 0:
                p.cshape_x = 0
            if p.cshape_y >= 1300:
                p.cshape_y = 1300
            elif p.cshape_y <= 0:
                p.cshape_y = 0
        
    def out_range_bullet(self, dt):
        '''清理飞出边界的炮弹'''
        # 把所有炮弹加入列表
        bullet_list = []
        for b in self.bullet_dict:
            bullet_list.append(b)
        for b in self.bullet_dicte:
            bullet_list.append(b)
        # 依次检查炮弹
        for b in bullet_list:
            if not (0 <= b.cshape_x <= 1300 and 0 <= b.cshape_y <= 1300):
                if abs(b.x - self.tank.x) > self.center[0] or abs(b.y - self.tank.y) > self.center[1]:
                    if b in self.bullet_dict:
                        self.remove(self.bullet_dict[b])
                        del self.bullet_dict[b]
                    else:
                        self.remove(self.bullet_dicte[b])
                        del self.bullet_dicte[b]

    def colliding(self, o1, o2):
        '''撞车加锁判断'''
        width = o1.hw + o2.hw
        height = o1.hh + o2.hh
        k = height / width
        w = o1.cshape_x - o2.cshape_x
        h = o1.cshape_y - o2.cshape_y
        try:
            k0 = h / w
        except ZeroDivisionError:
            if h >= 0:
                o1.can_move[1] = 0
                o2.can_move[0] = 0
                self.blocking_pair.append((o1, o2, 2))
            else:
                o1.can_move[0] = 0
                o2.can_move[1] = 0
                self.blocking_pair.append((o1, o2, 3))
        else:
            if abs(k0) <= k:
                if w >= 0:
                    o1.can_move[2] = 0
                    o2.can_move[3] = 0
                    self.blocking_pair.append((o1, o2, 0)) # 将发生碰撞的双方加入列表
                else:
                    o1.can_move[3] = 0
                    o2.can_move[2] = 0
                    self.blocking_pair.append((o1, o2, 1))
            else:
                if h >= 0:
                    o1.can_move[1] = 0
                    o2.can_move[0] = 0
                    self.blocking_pair.append((o1, o2, 2))
                else:
                    o1.can_move[0] = 0
                    o2.can_move[1] = 0
                    self.blocking_pair.append((o1, o2, 3))

class BgLayer(ColorLayer):
    '''背景层'''
    def __init__(self):
        super().__init__(100, 100, 100, 255, 2340, 1144)
        self.position = (-1170, 0)
        # self.bgsprite = Sprite('bg.jpg')
        # self.bgsprite.position = 0,503
        # self.add(self.bgsprite)


class MajorScene(Scene):
    def __init__(self, scene):
        super().__init__()
        self.majorlayer = MajorLayer()
        self.add(self.majorlayer)
        self.schedule(self.p)
        self.scene = scene()
    
    def p(self, dt):
        if keyboard[key.Q]:
            director.push(self.scene)