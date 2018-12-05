import math

from pyglet.window import key
from cocos.director import director
from cocos.menu import Menu, MenuItem, EntryMenuItem
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.scenes.transitions import FlipAngular3DTransition

screen_width = 720
screen_height = 600

wall_list = [
    (150, 150), (150, 350), (150, 950), (150, 1150),
    (250, 150), (250, 350), (250, 550), (250, 750), (250, 950), (250, 1150),
    (350, 150), (350, 350), (350, 550), (350, 750), (350, 950), (350, 1150),
    (450, 550), (450, 650), (450, 750),
    (550, 250), (550, 350), (550, 550), (550, 750), (550, 950), (550, 1050),
    (750, 150), (750, 350), (750, 550), (750, 750), (750, 950), (750, 1150),
    (850, 150), (850, 350), (850, 550), (850, 750), (850, 950), (850, 1150),
    (950, 150), (950, 350), (950, 550), (950, 750), (950, 950), (950, 1150),
    (1050, 150), (1050, 350), (1050, 550), (1050, 750), (1050, 950), (1050, 1150),
    (1150, 150), (1150, 350), (1150, 550), (1150, 750), (1150, 950), (1150, 1150)
]

iron_list = [
    (50, 650),
    (550, 50), (550, 1250),
    (950, 650)
]

gifts_list = [
    (50,750),
    (700,150),
    (300,1050),
    (550, 300),
    (1000,600),
    (100,450),
    (520,520)
]

client_key_dict = {
    'up:': 0,
    'down:': 0,
    'left:': 0,
    'right:': 0,
    'fire:': 0,
    'pause:': 0
}

key_dict = {
    'up:':key.UP,
    'down:':key.DOWN,
    'left:':key.LEFT,
    'right:':key.RIGHT,
    'fire:':key.SPACE,
    'pause:':key.Q,
}


class EntryMenuItemS(EntryMenuItem):
    # def __init__(self, *args):
    #     super().__init__(*args)
    #     self.bg = Sprite('pic/ditu.png')
    #     self.add(self.bg)
    
    def on_text(self, text):
        if isinstance(text, str):
            if text.upper() not in self._value:
                self._value.clear()
                self._calculate_value()
        else:
            self._value.append(key.symbol_string(text))
            key_dict[self._label] = text
            print(key_dict)
            self._calculate_value()
        return True
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER:
            self._value.clear()
            self._calculate_value()
            return True


class SettingMenu(Menu):
    def __init__(self):
        super().__init__(' ')
        # 字体
        self.font_title = {
            'text': 'title',
            'font_name': '黑体',
            'font_size': 56,
            'color': (255, 215, 0, 255),
            'bold': False,
            'italic': False,
            'anchor_y': 'center',
            'anchor_x': 'center',
            'dpi': 96,
            'x': 0, 'y': 0,
        }
        self.font_item = {
            'font_name': '黑体',
            'font_size': 32,
            'bold': False,
            'italic': False,
            'anchor_y': 'center',
            'anchor_x': 'center',
            'color': (255, 215, 0, 255),
            'dpi': 96,
        }
        self.font_item_selected = {
            'font_name': '黑体',
            'font_size': 42,
            'bold': False,
            'italic': False,
            'anchor_y': 'center',
            'anchor_x': 'center',
            'color': (255, 215, 0, 255),
            'dpi': 96,
        }
        # 列表项目
        l = []
        l.append(EntryMenuItemS('up:', self.set_key, key.symbol_string(key_dict['up:'])))
        l.append(EntryMenuItemS('down:', self.set_key, key.symbol_string(key_dict['down:'])))
        l.append(EntryMenuItemS('left:', self.set_key, key.symbol_string(key_dict['left:'])))
        l.append(EntryMenuItemS('right:', self.set_key, key.symbol_string(key_dict['right:'])))
        l.append(EntryMenuItemS('fire:', self.set_key, key.symbol_string(key_dict['fire:'])))
        l.append(EntryMenuItemS('pause:', self.set_key, key.symbol_string(key_dict['pause:'])))
        l.append(MenuItem('返回', self.back_to_mainmenu))
        self.create_menu(l)

    def back_to_mainmenu(self):
        director.pop()
        director.next_scene = FlipAngular3DTransition(director.next_scene)

    def set_key(self, value):
        if value == '':
            self.active = True
        else:
            self.active = False
    
    def on_text(self, text):
        pass
    
    def on_key_press(self, symbol, modifiers):
        if self.active:
            self.children[self.selected_index][1].on_text(symbol)
        else:
            super().on_key_press(symbol, modifiers)


class SettingScene(Scene):
    def __init__(self):
        super().__init__()
        self.menu = SettingMenu()
        self.add(self.menu)
        self.bg = Sprite('pic/startbg.jpg')
        self.bg.position = 428, 280
        self.add(self.bg, z=-10)
        self.border = Sprite('pic/setbg.png')
        self.border.position = 425, 250
        self.border.scale = 2
        self.border.scale_y = 0.9
        self.border.scale_x = 1.1
        self.add(self.border, z=-5)