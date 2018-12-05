import json
import struct
from socket import *
from threading import Thread

from cocos.scene import Scene
from cocos.director import director
from cocos.sprite import Sprite

from scenes import MajorLayer, MajorScene
from settings import client_key_dict, key_dict
from base import keyboard
from bullet import Bullet
from gifts import Gifts

header_model = struct.Struct('!3i')
headerSize = 12


class ConnectScene(Scene):
    def __init__(self, layer):
        super().__init__()
        self.layer = layer()
        self.add(self.layer)
        self.bg = Sprite('pic/startbg.jpg')
        self.bg.position = 425, 280
        self.add(self.bg, z=-10)
        self.bg1 = Sprite('pic/setbg.png')
        self.bg1.position = 428, 300
        self.bg1.scale_x = 4
        self.bg1.scale_y = 1
        self.add(self.bg1, z=-5)


class MulGameSceneH(MajorScene):
    def __init__(self, scene, host):
        super().__init__(scene)
        self.host = host
        self.schedule(self.send_msg)
    
    def send_msg(self, dt):
        client_key_dict2 = dict()
        player_list = []
        enermy_list = []
        bullet_list = []
        gifts_list = []
        # key
        for i in key_dict:
            if keyboard[key_dict[i]]:
                client_key_dict2[i] = 1
            else:
                client_key_dict2[i] = 0
        # ally
        for i in self.majorlayer.ally_dict:
            player_list.append([self.majorlayer.ally_dict[i], i.cshape_x, i.cshape_y, i.direction])
        # enermy
        for i in self.majorlayer.enermy_dict:
            enermy_list.append([self.majorlayer.enermy_dict[i], i.cshape_x, i.cshape_y, i.direction, i.ai_direction])
        # bullet
        for i in self.majorlayer.bullet_dict:
            bullet_list.append([self.majorlayer.bullet_dict[i], i.cshape_x, i.cshape_y, i.direction])
        for i in self.majorlayer.bullet_dicte:
            bullet_list.append([self.majorlayer.bullet_dicte[i], i.cshape_x, i.cshape_y, i.direction, i.m, i.c])
        # gift
        for i in self.majorlayer.gifts_dict:
            gifts_list.append([self.majorlayer.gifts_dict[i], i.cshape_x, i.cshape_y, i.direction])
        # 打包信息
        b_list = [client_key_dict2, player_list, enermy_list, bullet_list, gifts_list]
        body = json.dumps(b_list)
        ver = 1
        cmd = 2
        header = [ver, body.__len__(), cmd]
        headpack = header_model.pack(*header)
        msg = headpack + body.encode()
        try:
            self.host.cfd.send(msg)
        except Exception:
            self.host.cfd.close()
            director.pop()

    def add_majorlayer(self):
        self.majorlayer = MajorLayer(True)
        self.add(self.majorlayer)

    def p(self, dt):
        super().p(dt)
        if client_key_dict['pause:']:
            director.push(self.scene())


class MulGameSceneC(MajorScene):
    def __init__(self, scene, client):
        super().__init__(scene)
        self.client = client
        self.schedule(self.send_msg)
        self.schedule_interval(self.synchronize, 0.005)
    
    def synchronize(self, dt):
        if self.client.b_list:
            # ally
            player_list = self.client.b_list[1]
            for i in player_list:
                for j in self.majorlayer.ally_dict:
                    if self.majorlayer.ally_dict[j] == i[0]:
                        j.cshape_x = i[1]
                        j.cshape_y = i[2]
                        j.direction = i[3]
            # enermy
            enermy_list = self.client.b_list[2]
            for i in enermy_list:
                for j in self.majorlayer.enermy_dict:
                    if self.majorlayer.enermy_dict[j] == i[0]:
                        j.cshape_x = i[1]
                        j.cshape_y = i[2]
                        j.direction = i[3]
                        j.ai_direction = i[4]
            # bullet
            bullet_list = self.client.b_list[3]
            b1 = [x for x in bullet_list if x[0] in self.majorlayer.bullet_dict.values()]
            for i in b1:
                for j in self.majorlayer.bullet_dict:
                    if i[0] == self.majorlayer.bullet_dict[j]:
                        j.cshape_x = i[1]
                        j.cshape_y = i[2]
                        j.direction = i[3]
            b2 = [x for x in bullet_list if x[0] in self.majorlayer.bullet_dicte.values()]
            for i in b2:
                for j in self.majorlayer.bullet_dicte:
                    if i[0] == self.majorlayer.bullet_dicte[j]:
                        j.cshape_x = i[1]
                        j.cshape_y = i[2]
                        j.direction = i[3]
            for i in [x for x in bullet_list if x not in (b1 + b2)]:
                if i[0][:2] == 'eb':
                    if int(i[0][2:]) >= self.majorlayer.be_count:
                        bullet = Bullet(i[1], i[2], i[3], i[4], i[5]/2)
                        self.majorlayer.play_fire_sound(bullet)
                        self.majorlayer.bullet_dicte[bullet] = i[0]
                        self.majorlayer.add(bullet, z=bullet.z, name=i[0])
                        self.majorlayer.be_count += 1
            # gift
            gifts_list = self.client.b_list[4]
            for i in gifts_list:
                if int(i[0][1:]) >= self.majorlayer.gift_count:
                    gift = Gifts(i[1], i[2], i[3])
                    self.majorlayer.gifts_dict[gift] = i[0]
                    self.majorlayer.add(gift, z=gift.z, name=i[0])
                    self.majorlayer.gift_count += 1
            self.client.b_list = []
    
    def send_msg(self, dt):
        client_key_dict2 = dict()
        for i in key_dict:
            if keyboard[key_dict[i]]:
                client_key_dict2[i] = 1
            else:
                client_key_dict2[i] = 0
        body = json.dumps(client_key_dict2)
        ver = 1
        cmd = 2
        header = [ver, body.__len__(), cmd]
        headpack = header_model.pack(*header)
        msg = headpack + body.encode()
        try:
            self.client.sfd.send(msg)
        except Exception:
            self.client.sfd.close()
            director.pop()
    
    def add_majorlayer(self):
        self.majorlayer = MajorLayer(True, False)
        self.add(self.majorlayer)
        self.majorlayer.unschedule(self.majorlayer.ai_move)
        self.majorlayer.unschedule(self.majorlayer.ai_fire)
    
    def p(self, dt):
        super().p(dt)
        if client_key_dict['pause:']:
            director.push(self.scene())


class Host():
    def __init__(self):
        self.sfd = socket()
        self.sfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sfd.bind(('0.0.0.0', 9527))
        self.data = bytes()
    
    def start_host(self):
        self.sfd.listen(5)
        while 1:
            self.cfd, addr = self.sfd.accept()
            msg = self.cfd.recv(4096).decode()
            if msg == 'tank_r':
                print(msg)
                self.t = Thread(target=self.handler, args=(self.cfd,))
                self.t.daemon = True
                self.t.start()
            elif msg == 'tank_s':
                print(msg)
                self.sfd.close()
                break
    
    def handler(self, cfd):
        while 1:
            try:
                msg = cfd.recv(4096)
            except Exception:
                cfd.close()
                break
            if msg:
                self.data += msg
                while 1:
                    if len(self.data) < headerSize:
                        break
                    headPack = header_model.unpack(self.data[:headerSize])
                    bodySize = headPack[1]
                    if len(self.data) < headerSize+bodySize:
                        break
                    body = self.data[headerSize:headerSize + bodySize]
                    self.dataHandle(body)
                    self.data = self.data[headerSize + bodySize:]
    
    def dataHandle(self, body):
        client_key_dict2 = json.loads(body.decode())
        for i in client_key_dict2:
            if client_key_dict2[i]:
                client_key_dict[i] = 1
            else:
                client_key_dict[i] = 0


class Client():
    def __init__(self, ip):
        self.b_list = []
        self.data = bytes()
        self.sfd = socket()
        self.rfd = socket()
        self.addr = (ip, 9527)
        self.connect_to_host()
    
    def connect_to_host(self):
        self.sfd.connect(self.addr)
        self.sfd.send(b'tank_r')
        self.rfd.connect(self.addr)
        self.rfd.send(b'tank_s')
        self.t = Thread(target=self.recv_msg)
        self.t.daemon = True
        self.t.start()
    
    def recv_msg(self):
        while 1:
            try:
                msg = self.rfd.recv(4096)
            except Exception:
                self.rfd.close()
                break
            if msg:
                self.data += msg
                while 1:
                    if len(self.data) < headerSize:
                        break
                    headPack = header_model.unpack(self.data[:headerSize])
                    bodySize = headPack[1]
                    if len(self.data) < headerSize+bodySize:
                        break
                    body = self.data[headerSize:headerSize + bodySize]
                    self.dataHandle(body)
                    self.data = self.data[headerSize + bodySize:]
    
    def dataHandle(self, body):
        self.b_list = json.loads(body.decode())
        client_key_dict2 = self.b_list[0]
        for i in client_key_dict2:
            if client_key_dict2[i]:
                client_key_dict[i] = 1
            else:
                client_key_dict[i] = 0