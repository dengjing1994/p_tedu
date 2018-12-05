import pyglet
from pyglet.window import key
from cocos.director import director
from cocos.menu import Menu, MenuItem, EntryMenuItem, ImageMenuItem, shake, shake_back, LEFT
from cocos.scenes.transitions import FlipAngular3DTransition
from cocos.actions import Place
from cocos.scene import Scene
from cocos.layer import ColorLayer
from cocos.sprite import Sprite
from cocos.text import Label

from scenes import MajorScene
from settings import SettingScene
from check import CheckScene
from connect import Host, Client, ConnectScene, MulGameSceneH, MulGameSceneC


class MainMenu(Menu):
    '''主菜单'''
    def __init__(self):
        super().__init__(' ')
        l = []
        l.append(ImageMenuItem('pic/kaishi.png', self.on_start))
        l.append(ImageMenuItem('pic/keys.png', self.on_setting))
        l.append(ImageMenuItem('pic/jifen.png', self.on_score))
        l.append(ImageMenuItem('pic/lianji.png', self.on_connect))
        l.append(ImageMenuItem('pic/tuichu.png', self.on_quit))
        self.create_menu(l, shake(), shake_back())

    def on_start(self):
        '''切换到游戏场景'''
        next_scene = MajorScene(PlayMenuScene)
        director.push(FlipAngular3DTransition(next_scene))

    def on_setting(self):
        next_scene = SettingScene()
        director.push(FlipAngular3DTransition(next_scene))
    
    def on_score(self):
        next_scene = CheckScene()
        director.push(FlipAngular3DTransition(next_scene))

    def on_connect(self):
        next_scene = ConnectScene(ConnectMenu)
        director.push(FlipAngular3DTransition(next_scene))

    def on_quit(self):
        '''退出'''
        pyglet.app.exit()


class PlayMenu(Menu):
    def __init__(self):
        super().__init__()
        self.font_item['font_name'] = '黑体'
        self.font_item_selected['font_name'] = '黑体'
        l = []
        l.append(MenuItem('继续游戏', self.on_resume))
        l.append(MenuItem('键位设置', self.on_setting))
        l.append(MenuItem('返回主菜单', self.on_back_to_mainmenu))
        self.create_menu(l, shake(), shake_back())

    def on_resume(self):
        director.pop()
    
    def on_setting(self):
        next_scene = SettingScene()
        director.push(FlipAngular3DTransition(next_scene))

    def on_back_to_mainmenu(self):
        director.pop()
        director.pop()
        director.next_scene = FlipAngular3DTransition(director.next_scene)


class MainMenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.spr = Sprite('pic/startbg.jpg')
        self.spr.position = 425, 280
        self.add(self.spr, z=-1)
        self.mm = MainMenu()
        self.mm.scale = 2
        self.add(self.mm)


class PlayMenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.add(PlayMenu())
        self.bg = Sprite('pic/startbg.jpg')
        self.bg.position = 428, 280
        self.add(self.bg, z=-10)
        self.border = Sprite('pic/setbg.png')
        self.border.position = 425, 300
        self.border.scale_y = 1
        self.border.scale_x = 2
        self.add(self.border, z=-5)


class ConnectMenu(Menu):
    def __init__(self):
        super().__init__()
        self.font_item['font_name'] = '黑体'
        self.font_item_selected['font_name'] = '黑体'
        self.l = []
        self.l.append(MenuItem('建立主机', self.sethost))
        self.l.append(EntryMenuItem('目标IP:', self.connect, '127.0.0.1'))
        self.l.append(MenuItem('确认连接', self.try_connect))
        self.l.append(MenuItem('返回', self.on_back_to_mainmenu))
        self.create_menu(self.l, shake(), shake_back())
    
    def sethost(self):
        self.host = Host()
        self.host.start_host()
        self.gamescene = MulGameSceneH(PlayMenuScene, self.host)
        director.push(self.gamescene)
    
    def connect(self, value):
        pass
    
    def try_connect(self):
        print(self.l[1].value)
        self.client = Client(self.l[1].value)
        self.gamescene = MulGameSceneC(PlayMenuScene, self.client)
        director.push(self.gamescene)

    def on_back_to_mainmenu(self):
        director.pop()
        director.next_scene = FlipAngular3DTransition(director.next_scene)