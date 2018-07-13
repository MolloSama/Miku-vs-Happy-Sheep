
#存储游戏设置的类
class Settings():
    def __init__(self):

        #屏幕设置
        self.screen_width=1280
        self.screen_height=720
        self.bg_color= (255, 192, 203)

        #飞船设置
        self.ship_speed = 3
        self.ship_limit = 2

        #子弹设置
        self.bullet_speed = 3
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = (128, 138, 135)
        self.bullets_allowed = 20   #允许发射的子弹数量

        #外星人设置
        self.alien_speed = 2
        self.fleet_drop_speed = 20
        #此处direction为1表示右移，为-1表示左移
        self.fleet_direction = 1