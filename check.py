import cocos
from cocos.director import director
from cocos.sprite import Sprite
from cocos.menu import Menu, MenuItem
from cocos.scenes.transitions import FlipAngular3DTransition


class ScoreBoard(cocos.layer.Layer):
    def __init__(self):
        super(ScoreBoard,self).__init__()
        self.text1 = cocos.text.Label("姓名",position=(250,400),\
                                font_name = '黑体',\
                                font_size = 20)
        self.text2 = cocos.text.Label("得分",position=(400,400),\
                                font_name = '黑体',\
                                font_size = 20)
        self.text3 = cocos.text.Label("排名",position=(550,400),\
                                font_name = '黑体',\
                                font_size = 20)
        self.add(self.text1)
        self.add(self.text2)
        self.add(self.text3)
        self.score_list = self.get_limit_scores()
        self.create_board()
        
    def create_board(self):
        count = 0
        for i in self.score_list:
            name_text = cocos.text.Label("%s"%i[0],
                                                position=(250,370-30*count),
                                                font_name = '黑体',
                                                font_size = 20)
            self.add(name_text)
            score_text = cocos.text.Label("%s"%i[1],
                                                position=(400,370-30*count),
                                                font_name = '黑体',
                                                font_size = 20)
            self.add(score_text)
            sort = cocos.text.Label(str(count + 1),position=(570,370-30*count),
                                            font_name = '黑体',
                                            font_size = 20)
            self.add(sort)
            count += 1


    def get_infos(self):
        f = open('score_all.txt')
        datas = f.readlines()
        data_list = []
        for data in datas:
            data = data.replace('\n','')
            nn = data.split(':')
            data_list.append(nn)
        return data_list
    
    def get_limit_scores(self):
        data_list = self.get_infos()
        data_list.sort(key=lambda x:int(x[1]), reverse=True)
        if len(data_list) >= 10:
            return data_list[:10]
        else:
            return data_list


class CheckScene(cocos.scene.Scene):
    def __init__(self):
        super(CheckScene,self).__init__()
        self.scoreboard = cocos.scene.Scene(ScoreBoard())
        self.add(self.scoreboard,z=2)
        self.add_menu()
        #此处图片有待修改
        self.bg1 = Sprite('pic/setbg.png')
        self.bg1.position = 428, 280
        self.bg1.scale_x = 3
        self.bg1.scale_y = 1.5
        self.add(self.bg1,z=1)
        self.bg2 = Sprite('pic/startbg.jpg')
        self.bg2.position = 428, 280
        self.add(self.bg2,z=0)
    
    def add_menu(self):
        self.menu = Menu()
        self.menu.font_item_selected['font_name'] = '黑体'
        self.menuitem = MenuItem('返回', self.back)
        self.menu.create_menu([self.menuitem])
        self.menu.y -= 250
        self.add(self.menu, z=3)
    
    def back(self):
        director.pop()
        director.next_scene = FlipAngular3DTransition(director.next_scene)