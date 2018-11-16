import math
from pyglet.window import key
from cocos.layer import Layer
from cocos.collision_model import AARectShape
from cocos.euclid import Vector2

keyboard = key.KeyStateHandler() # 处理键盘输入


def coordinate_trans(x, y):
    '''坐标转换'''
    # 具体转多少度根据地图再调整
    # t_x = x * math.cos(math.pi * 45 / 180) - y * math.sin(math.pi * 45 / 180)
    # t_y = x * math.sin(math.pi * 45 / 180) + y * math.cos(math.pi * 45 / 180)
    t_x = x * 0.90 - y * 0.90
    t_y = x * 0.43 + y * 0.44
    return (t_x, t_y)


class Setting(Layer):
    '''游戏单位的基类'''
    def __init__(self, x, y, half_width, half_height, c=0):
        '''初始化需要位置(x,y),高度(hw),宽度(hh)，图像位置修正值(c)'''
        super().__init__()
        # 产生用于判断的矩形和位置
        self.cshape01 = AARectShape(Vector2(x, y), half_width, half_height)
        self.cshape23 = AARectShape(Vector2(x, y), half_height, half_width)
        self.direction = 0 # 默认朝向为上(0),其他方向为下(1)，左(2)，右(3)
        self.cshape = self.cshape01
        self.cshape_x = x
        self.cshape_y = y
        # 设置图片显示的位置
        self.c = c
        pos = coordinate_trans(x, y)
        self.x = pos[0]
        self.y = pos[1] + c
        self.z = 1 / (x + y + 1)
        # 其他属性
        self.can_move = [1, 1, 1, 1] # 在上下左右四个方向能否移动
        self.hw = half_width
        self.hh = half_height
        self.schedule(self.update_cshape)

    def update_cshape(self, dt):
        if self.direction in (0, 1):
            self.cshape = self.cshape01
        elif self.direction in (2, 3):
            self.cshape = self.cshape23


class Actor(Setting):
    '''游戏单位的基类'''
    def __init__(self, x, y, half_width, half_height, c=0):
        super().__init__(x, y, half_width, half_height, c)
        self.schedule(self.update_pos)
    
    def update_pos(self, dt):
        self.cshape.center = Vector2(self.cshape_x, self.cshape_y)
        pos = coordinate_trans(self.cshape_x, self.cshape_y)
        self.x = pos[0]
        self.y = pos[1] + self.c
        a = self.parent.children
        elem = self.z, self
        try:
            a.remove(elem)
        except:
            return
        self.z = 1 / (self.cshape_x + self.cshape_y + 1)
        elem = self.z, self
        lo = 0
        hi = len(a)
        while lo < hi:
            mid = (lo+hi) // 2
            if self.z < a[mid][0]:
                hi = mid
            else:
                lo = mid + 1
        a.insert(lo, elem)