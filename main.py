from cocos.director import director

from base import keyboard
from menu import MainMenuScene
from scenes import MajorScene
from settings import key_dict


def main():
    # 初始化
    director.init(audio_backend='sdl')
    # 处理键盘输入
    director.window.push_handlers(keyboard)
    # 建立开始菜单场景
    mainmenuscene = MainMenuScene()
    # 启动
    director.run(mainmenuscene)


if __name__ == '__main__':
    main()