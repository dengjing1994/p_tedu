from cocos.sprite import Sprite
from pyglet import image

from base import Setting


class Explosion(Setting):
    def __init__(self, *args):
        super().__init__(*args)
        self.get_sprite()
        self.last_time = 0.3
        self.schedule(self.last)
    
    def get_sprite(self):
        l = []
        l.append(image.AnimationFrame(image.load('pic/1.png'), 0.1))
        l.append(image.AnimationFrame(image.load('pic/2.png'), 0.1))
        l.append(image.AnimationFrame(image.load('pic/3.png'), 0.1))
        images = image.Animation(l)
        self.sprite = Sprite(images)
        self.sprite.scale = 0.5
        self.add(self.sprite)
    
    def last(self, dt):
        self.last_time -= dt
        if self.last_time < 0:
            self.kill()


class ExplosionP(Explosion):
    def __init__(self, *args):
        super().__init__(*args)
    
    def get_sprite(self):
        l = []
        l.append(image.AnimationFrame(image.load('pic/b001.png'), 0.1))
        l.append(image.AnimationFrame(image.load('pic/b002.png'), 0.1))
        l.append(image.AnimationFrame(image.load('pic/b003.png'), 0.1))
        l.append(image.AnimationFrame(image.load('pic/b004.png'), 0.1))
        l.append(image.AnimationFrame(image.load('pic/b005.png'), 0.1))
        l.append(image.AnimationFrame(image.load('pic/b006.png'), 0.1))
        images = image.Animation(l)
        self.sprite = Sprite(images)
        self.add(self.sprite)