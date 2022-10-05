import pygame

class Settings:
    def __init__(self):
        """窗口设置"""
        #设置游戏窗口大小
        self.screen_widht = 1200
        self.screen_height = 800
        #设置背景颜色
        self.bg_color = (230, 230, 230)

        """飞船设置"""
        self.ship_speed = 1.5   #飞船速度

        """子弹设置"""
        self.bullet_speed = 1.0         #子弹速度
        self.bullet_width = 3           #子弹宽度
        self.bullet_height = 15         #子弹长度
        self.bullet_color = (60,60,60)  #子弹颜色


