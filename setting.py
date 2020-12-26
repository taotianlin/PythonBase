class Settings():
    def  __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (27,87,55)
        self.ship_speed = 2
        #子弹设置
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 3

        #外星人设置
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1#1 rightmove  -1 leftmove

        #ship设置
        self.ship_limit = 3