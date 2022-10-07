import pygame

class Settings:
    def __init__(self):
        """初始化游戏的静态设置"""
        # """窗口设置"""
        #设置游戏窗口大小
        self.screen_width = 1200
        self.screen_height = 800
        #设置背景颜色
        self.bg_color = (230, 230, 230)

        # """飞船设置"""
        self.ship_limit = 3     #飞船数量

        # """子弹设置"""
        self.bullet_width = 300               #子弹宽度
        self.bullet_height = 15             #子弹长度
        self.bullet_color = (192,192,192)   #子弹颜色
        self.bullet_allowed = 3             #最大子弹数

        # """外星人设置"""
        self.fleet_drop_speed = 10 

        # """加快游戏节奏的速度"""
        self.speedup_scale = 1.1
        #外星人分数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 1.5       #飞船初始速度
        self.bullet_speed = 3.0     #子弹初始速度
        self.alien_speed = 1.0      #外星人初始速度

        # fleet_direction 为 1 表示向右移动，为 -1 表示向左移动
        self.fleet_direction = 1

        #记分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置和外星人分数"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)





