import sys
import pygame
from settings import Settings
from ship import Ship

class AlenInvasion:
    """管理游戏资源和行为的类"""
    
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        #设置类
        self.settings = Settings()
        #设置game窗口大小
        self.screen = pygame.display.set_mode((self.settings.screen_widht, self.settings.screen_height))
        #设置game窗口标题
        pygame.display.set_caption("Alien Invasion")
        #创建一搜飞船
        self.ship = Ship(self)

    def run_game(self):
        """开始游戏的主循环"""
        while True :
            #监事键盘和鼠标事件
            for event in pygame.event.get():
                #触发QUIT事件退出游戏
                if event.type == pygame.QUIT :
                    sys.exit()

            # 每次循环时重绘屏幕
            self.screen.fill(self.settings.bg_color)
            
            #在窗口显示飞船
            self.ship

            #让最近绘制的屏幕可见
            pygame.display.flip()

if __name__ == '__main__' :
    #创建游戏实例并运行游戏。
    ai = AlenInvasion()
    ai.run_game()


