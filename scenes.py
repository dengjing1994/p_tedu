from random import random, randrange, randint
from time import sleep
from pyglet.window import key
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.collision_model import CollisionManagerGrid
from cocos.sprite import Sprite
from cocos.audio.effect import Effect
from cocos.euclid import Vector2
from cocos.actions import Delay, CallFunc
from cocos.text import Label
from cocos.menu import Menu, EntryMenuItem, MenuItem

from tanks import *
from base import keyboard
from bullet import Bullet
from wall import Wall, Iron
from settings import wall_list, iron_list, key_dict, client_key_dict, gifts_list
from explosion import Explosion, ExplosionP
from gifts import Gifts


class MajorLayer(Layer):

    is_event_handler = False

    def __init__(self, mul=False, host=True):
        super().__init__()
        self.mul = mul
        self.host = host
        # 设置中心点为屏幕中心
        self.center = (director.get_window_size()[0] / 2, director.get_window_size()[1] / 2)
        # 添加背景层
        self.add(BgLayer(), z=0)
        # 设置存储对象的字典、集合和列表
        self.ally_dict = {}
        self.enermy_dict = {}
        self.bullet_dict = {}
        self.bullet_dicte = {}
        self.wall_dict = {}
        self.gifts_dict = {}
        self.toremove = set()
        self.blocking_pair = []
        # 设置敌方坦克数量
        self.totle_enermy_num = 1
        self.active_enermy_num = 0
        self.enermy_point_list = [(1250, 50), (1250, 650), (1250, 1250)]
        # 子弹计数
        self.b_count = 0
        self.be_count = 0
        # 设置道具数量和计数
        self.gifts_num = 0
        self.gift_count = 0
        # 设置碰撞管理对象
        self.collman = CollisionManagerGrid(0, 1300,
                                            0, 1300,
                                            10, 10)
        # 计分板
        self.score = 0
        if mul:
            self.is_game_over = [3, 3]
        else:
            self.is_game_over = [3, 0]
        # 音效
        self.fire_sound = Effect('music/fire.wav')
        self.explode_sound = Effect('music/bang.wav')
        self.bullet_hit_sound = Effect('music/blast.wav')
        self.get_hit_sound = Effect('music/hit.wav')
        # 增加墙壁
        self.add_wall()
        # 添加我方坦克
        self.add_player()
        if mul:
            self.add_ally()
        # 设置回调
        self.set_schedule()
    
    def set_schedule(self):
        self.schedule(self.key)
        # self.schedule(self.collisons_test)
        self.schedule(self.update)
        self.schedule(self.boundary)
        self.schedule(self.out_range_bullet)
        self.schedule(self.ai_stoped)
        # 每5秒试图添加敌人
        self.schedule_interval(self.add_enermy, 5)
        # 每隔一段时间给ai下达指令
        self.schedule_interval(self.ai_move, 3)
        self.schedule_interval(self.ai_fire, 1)
        # 在地图上添加道具
        self.schedule_interval(self.update_gift, 10)
    
    def add_wall(self):
        for i in wall_list:
            coo = list(i)
            self.create_wall(coo[0] - 25, coo[1] + 25)
            self.create_wall(coo[0] + 25, coo[1] + 25)
            self.create_wall(coo[0] + 25, coo[1] - 25)
            self.create_wall(coo[0] - 25, coo[1] - 25)
        for i in iron_list:
            w = Iron(*i)
            self.wall_dict[w] = str(w)
            self.add(w, z=w.z, name=self.wall_dict[w])
    
    def create_wall(self, x, y):
        w = Wall(x, y)
        self.wall_dict[w] = str(w)
        self.add(w, z=w.z, name=self.wall_dict[w])

    def add_player(self):
        if self.is_game_over[0] > 0:
            self.tank1 = Tank(50, 450)
            self.ally_dict[self.tank1] = 'p1' + str(self.is_game_over[0])
            self.add(self.tank1, z=self.tank1.z, name=self.ally_dict[self.tank1])
    
    def add_ally(self):
        if self.is_game_over[1] > 0:
            self.tank2 = Tank(50, 850)
            self.ally_dict[self.tank2] = 'p2' + str(self.is_game_over[1])
            self.add(self.tank2, z=self.tank2.z, name=self.ally_dict[self.tank2])

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
                    self.play_fire_sound(p)
                    self.bullet_dicte[b] = 'eb' + str(self.be_count)
                    self.add(b, z=b.z, name=self.bullet_dicte[b])
                    self.be_count += 1
        
    def ai_stoped(self, dt):
        for i in self.enermy_dict:
            ai_move(i, dt)
    
    def in_screen(self, p):
        '''判断是否在屏幕显示范围内'''
        v = p.point_to_world(Vector2(0, 0))
        if (0 < v.x < 2 * self.center[0]) and ( 0 < v.y < 2 * self.center[1]):
            return True
        else:
            return False

    def play_fire_sound(self, p):
        if self.in_screen(p):
            self.fire_sound.play()
    
    def play_explode_sound(self, p):
        if self.in_screen(p):
            self.explode_sound.play()
    
    def play_get_git_sound(self, p):
        if self.in_screen(p):
            self.get_hit_sound.play()
    
    def play_bullet_hit_sound(self, p):
        if self.in_screen(p):
            self.bullet_hit_sound.play()
    
    def add_explosion(self, i):
        '''坦克爆炸'''
        ep = ExplosionP(i.cshape_x, i.cshape_y, 20, 20, i.c)
        self.add(ep, z=ep.z)
        self.play_explode_sound(i)
    
    def add_bullet_hit(self, i):
        '''子弹命中'''
        ep = Explosion(i.cshape_x, i.cshape_y, 20, 20, i.c)
        self.add(ep, z=ep.z)
        self.play_bullet_hit_sound(i)

    def add_enermy(self, dt):
        '''添加敌人'''
        if self.totle_enermy_num and self.active_enermy_num < 7:
            i = self.totle_enermy_num % 3
            # 当仍有可用敌人数量时，添加敌人
            enermy = Panzer(*self.enermy_point_list[i])
            self.enermy_dict[enermy] = 'e' + str(self.totle_enermy_num)
            self.add(enermy, z=enermy.z, name=self.enermy_dict[enermy])
            self.totle_enermy_num += 1
            self.active_enermy_num += 1
    
    def add_gift(self):
        index = randint(0, 6)
        g = Gifts(*gifts_list[index])
        self.gifts_dict[g] = 'g' + str(self.gift_count)
        self.gift_count += 1
        self.add(g, z=g.z, name=self.gifts_dict[g])
    
    def update_gift(self, dt):
        if self.gifts_num < 2:
            self.add_gift()
            self.gifts_num += 1

    def update(self, dt):
        '''更新图像位置，保证玩家在屏幕中间'''
        if self.host:
            self.x = self.center[0] - self.tank1.x
            self.y = self.center[1] - self.tank1.y
        else:
            self.x = self.center[0] - self.tank2.x
            self.y = self.center[1] - self.tank2.y

    def key(self, dt):
        '''响应键盘按键'''
        # 主玩家
        if self.is_game_over[0]:
            if self.host:
                p1 = self.tank1
            else:
                p1 = self.tank2
            # 空格开火
            if keyboard[key_dict['fire:']]:
                bullet = p1.fire(dt)
                if bullet:
                    self.play_fire_sound(bullet) # 播放音效
                    # 开火成功则将炮弹加入self
                    self.bullet_dict[bullet] = 'b' + str(self.b_count)
                    self.add(bullet, z=bullet.z, name=self.bullet_dict[bullet])
                    self.b_count += 1
            # 移动操作
            if keyboard[key_dict['up:']]:
                p1.move_up(dt)
            elif keyboard[key_dict['down:']]:
                p1.move_down(dt)
            elif keyboard[key_dict['left:']]:
                p1.move_left(dt)
            elif keyboard[key_dict['right:']]:
                p1.move_right(dt)
        # 副玩家
        if self.is_game_over[1]:
            if self.host:
                p2 = self.tank2
            else:
                p2 = self.tank1
            # 空格开火
            if client_key_dict['fire:']:
                bullet = p2.fire(dt)
                if bullet:
                    self.play_fire_sound(bullet) # 播放音效
                    # 开火成功则将炮弹加入self
                    self.bullet_dict[bullet] = 'b' + str(self.b_count)
                    self.add(bullet, z=bullet.z, name=self.bullet_dict[bullet])
                    self.b_count += 1
            # 移动操作
            if client_key_dict['up:']:
                p2.move_up(dt)
            elif client_key_dict['down:']:
                p2.move_down(dt)
            elif client_key_dict['left:']:
                p2.move_left(dt)
            elif client_key_dict['right:']:
                p2.move_right(dt)
        # 测试用
        if keyboard[key.O]:
            self.is_game_over = [0, 0]
        if keyboard[key.P]:
            self.pause()
            self.pause_scheduler()
        # else:
        #     self.resume()
        
        self.collisons_test(dt)
    
    def collisons_test(self, dt):
        '''碰撞相关检测'''
        # 当一对移动受限物体不再碰撞时，解除移动限制
        for t1, t2, n in self.blocking_pair:
            if not self.collman.they_collide(t1, t2) or not (t1.is_running and t2.is_running):
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
        for p in self.ally_dict:
            self.collman.add(p)
        for p in self.enermy_dict:
            self.collman.add(p)
        for b in self.bullet_dict:
            self.collman.add(b)
        for b in self.bullet_dicte:
            self.collman.add(b)
        for w in self.wall_dict:
            self.collman.add(w)
        for g in self.gifts_dict:
            self.collman.add(g)
        # 判断发生哪些碰撞
        for o1, o2 in self.collman.iter_all_collisions():
            # 判断o1是否为炮弹
            if isinstance(o1, Bullet):
                if o1 in self.bullet_dict and o2 in self.ally_dict:
                    # 若为己方炮弹和己方坦克则无影响
                    pass
                elif o1 in self.bullet_dicte and o2 in self.enermy_dict:
                    # 地方炮弹和敌方坦克
                    pass
                elif o2 in self.gifts_dict:
                    # 对道具无影响
                    pass
                else:
                    # 否则将双方加入销毁列表
                    self.toremove.add(o1)
                    self.toremove.add(o2)
            # 判断o2是否为炮弹
            elif isinstance(o2, Bullet):
                if o2 in self.bullet_dict and o1 in self.ally_dict:
                    pass
                elif o2 in self.bullet_dicte and o1 in self.enermy_dict:
                    pass
                elif o1 in self.gifts_dict:
                    pass
                else:
                    self.toremove.add(o1)
                    self.toremove.add(o2)
            # 障碍物之间什么也不发生
            elif isinstance(o1, Wall) and isinstance(o2, Wall):
                pass
            # 坦克和道具
            elif isinstance(o1, Gifts):
                if o2 in self.ally_dict:
                    if o2.durability < 3:
                        o2.durability += 1
                        self.toremove.add(o1)
            elif isinstance(o2, Gifts):
                if o1 in self.ally_dict:
                    if o1.durability < 3:
                        o1.durability += 1
                        self.toremove.add(o2)
            # 坦克与障碍物和坦克与坦克的碰撞
            else:
                # 判断碰撞方向，并锁定相应的移动方式
                self.colliding(o1, o2)
        # 处理销毁列表中的对象
        for i in self.toremove:
            if isinstance(i, Bullet):
                # 添加爆炸效果
                self.add_bullet_hit(i)
                # 删除
                if i in self.bullet_dict:
                    self.remove(self.bullet_dict[i])
                    del self.bullet_dict[i]
                else:
                    self.remove(self.bullet_dicte[i])
                    del self.bullet_dicte[i]
            elif isinstance(i, Panzer):
                # 爆炸效果
                self.add_explosion(i)
                # 删除坦克
                self.remove(self.enermy_dict[i])
                del self.enermy_dict[i]
                # 销毁敌方坦克时，相关数据变动
                self.active_enermy_num -= 1
                self.score += 1
            elif isinstance(i, Tank):
                self.play_get_git_sound(i)
                if i is self.tank1:
                    if i.durability:
                        i.get_hit()
                    else:
                        self.remove(self.ally_dict[i])
                        del self.ally_dict[i]
                        # 爆炸效果
                        self.add_explosion(i)
                        # 玩家重生
                        self.is_game_over[0] -= 1
                        delay_act = Delay(1) + CallFunc(self.add_player)
                        self.do(delay_act)
                if self.mul:
                    if i is self.tank2:
                        if i.durability:
                            i.get_hit()
                        else:
                            self.remove(self.ally_dict[i])
                            del self.ally_dict[i]
                            # 爆炸效果
                            self.add_explosion(i)
                            # 玩家重生
                            self.is_game_over[1] -= 1
                            delay_act = Delay(1) + CallFunc(self.add_ally)
                            self.do(delay_act)
            elif isinstance(i, Wall):
                # 墙壁可以抵挡一定次数的攻击
                self.play_get_git_sound(i)
                if i.durability:
                    i.get_hit()
                else:
                    self.remove(self.wall_dict[i])
                    del self.wall_dict[i]
            elif isinstance(i, Gifts):
                self.remove(self.gifts_dict[i])
                del self.gifts_dict[i]
                self.gifts_num -= 1
        # 清空销毁列表
        self.toremove.clear()
    
    def boundary(self, dt):
        '''地图边界判断'''
        # 把已有坦克全部放进列表
        actor_list = []
        for p in self.ally_dict:
            actor_list.append(p)
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
                if not self.in_screen(b):
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

class BgLayer(Layer):
    '''背景层'''
    def __init__(self):
        super().__init__()
        self.bgsprite = Sprite('pic/dimian.png')
        self.bgsprite.position = 0, 650
        self.add(self.bgsprite)


class MajorScene(Scene):
    def __init__(self, scene):
        super().__init__()
        self.add_majorlayer()
        self.scene = scene
        self.game_over = GameOverLayer
        self.start_music = Effect('music/start.wav')
        self.start_music.play()
        self.schedule(self.p)
    
    def add_majorlayer(self):
        self.majorlayer = MajorLayer()
        self.add(self.majorlayer)
    
    def p(self, dt):
        if self.majorlayer.is_game_over == [0, 0]:
            self.unschedule(self.p)
            score = self.majorlayer.score
            self.add(self.game_over(score), z=10)
            self.remove(self.majorlayer)
        if keyboard[key_dict['pause:']]:
            director.push(self.scene())


class GameOverLayer(ColorLayer):
    def __init__(self, score):
        size = director.get_window_size()
        super().__init__(255, 215, 0, 200, size[0], size[1])
        self.get_score = str(score)
        s = '得分：' + self.get_score
        self.score = Label(s, font_name='WenQuanYi Micro Hei', font_size=36, color=(0, 0, 0, 255))
        self.score.position = 300, 400
        self.add(self.score)
        self.create_entry()
        self.name = ''
    
    def create_entry(self):
        self.entry = Menu('游戏结束')
        self.entry.font_title['font_name'] = 'WenQuanYi Micro Hei'
        self.entry.font_title['color'] = (0, 0, 0, 255)
        self.entry.font_item['font_name'] = 'WenQuanYi Micro Hei'
        self.entry.font_item['color'] = (255, 0, 0, 255)
        self.entry.font_item_selected['font_name'] = 'WenQuanYi Micro Hei'
        self.entry.font_item_selected['color'] = (255, 0, 0, 255)
        l = []
        l.append(EntryMenuItem('姓名:', self.update_text, '', max_length=7))
        l.append(MenuItem('确认', self.save))
        self.entry.create_menu(l)
        self.add(self.entry)

    def update_text(self, value):
        self.name = value
    
    def save(self):
        if self.name == '':
            self.name = 'NoName'
        with open('score_all.txt','a+') as f:
            f.write(self.name+":"+self.get_score+"\n")
        sleep(0.01)
        director.pop()