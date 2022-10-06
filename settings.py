import pygame

class Settings:
    def __init__(self):
        """窗口设置"""
        #设置游戏窗口大小
        self.screen_width = 1200
        self.screen_height = 800
        #设置背景颜色
        self.bg_color = (230, 230, 230)

        """飞船设置"""
        self.ship_speed = 1.5   #飞船速度
        self.ship_limit = 3     #飞船数量

        """子弹设置"""
        self.bullet_speed = 1.5             #子弹速度
        self.bullet_width = 3               #子弹宽度
        self.bullet_height = 15             #子弹长度
        self.bullet_color = (192,192,192)   #子弹颜色
        self.bullet_allowed = 3             #最大子弹数

        """外星人设置"""
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction 为 1 表示向右移动，为 -1 表示向左移动
        self.fleet_direction = 1



