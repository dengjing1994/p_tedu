import pyglet
from pyglet.window import key
from cocos.director import director
from cocos.menu import Menu, MenuItem, shake, shake_back
from cocos.scenes.transitions import FlipAngular3DTransition
from cocos.actions import Place
from cocos.scene import Scene
from cocos.layer import ColorLayer

from scenes import MajorScene
from settings import SettingScene


class MainMenu(Menu):
    '''主菜单'''
    def __init__(self):
        super().__init__('Fighter')
        l = []
        l.append(MenuItem('Start', self.on_start))
        l.append(MenuItem('Setting', self.on_setting))
        l.append(MenuItem('Connect', self.on_connect))
        l.append(MenuItem('Quit', self.on_quit))
        self.create_menu(l, shake(), shake_back())

    def on_start(self):
        '''切换到游戏场景'''
        next_scene = MajorScene(PlayMenuScene)
        director.push(FlipAngular3DTransition(next_scene))

    def on_setting(self):
        next_scene = SettingScene()
        director.push(FlipAngular3DTransition(next_scene))

    def on_connect(self):
        pass

    def on_quit(self):
        '''退出'''
        pyglet.app.exit()


class PlayMenu(Menu):
    def __init__(self):
        super().__init__('Pause')
        l = []
        l.append(MenuItem('Resume', self.on_resume))
        l.append(MenuItem('Setting', self.on_setting))
        l.append(MenuItem('Back to MainMenu', self.on_back_to_mainmenu))
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
        self.add(ColorLayer(0, 0, 255, 255))
        self.add(MainMenu())


class PlayMenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.add(PlayMenu())