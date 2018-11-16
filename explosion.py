from cocos.sprite import Sprite

from base import Setting


class Explosion(Setting):
    def __init__(self, *args):
        super().__init__(*args)
        s = Sprite('circle6.png')
        self.add(s)
        self.last_time = 1
        self.schedule(self.last)
    
    def last(self, dt):
        self.last_time -= dt
        if self.last_time < 0:
            self.kill()