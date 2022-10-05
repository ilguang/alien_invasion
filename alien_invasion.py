import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

class AlenInvasion:
    """管理游戏资源和行为的类"""
    
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        #设置类
        self.settings = Settings()
        #设置game窗口大小
        self.screen = pygame.display.set_mode((self.settings.screen_widht, self.settings.screen_height),pygame.RESIZABLE)
        #设置game窗口标题
        pygame.display.set_caption("Alien Invasion")
        #创建一搜飞船
        self.ship = Ship(self)
        #创建一个存储子弹的编组
        self.bullets = pygame.sprite.Group()



    def run_game(self):
        """开始游戏的主循环"""
        while True :
            #监事键盘和鼠标事件
            self._check_events()

            #飞船移动后位置更新
            self.ship.update()

            #更新 bullets 编组中所有子弹的位置
            self.bullets.update()

            #每次循环时重绘屏幕
            self._undate_screen()

            


    """重构事件监视和屏幕更新的代码"""
    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:      #触发按键 按下 事件
                self._check_keydown_events(event)   #处理键盘按键按下事件

            elif event.type == pygame.KEYUP:        #触发按键 松开 事件
                self._check_keyup_events(event)     #处理键盘按键松开事件

    def _check_keydown_events(self,event):
        """响应键盘按键按下"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:     #触发飞船右移按键(K_RIGHT or K_d)事件
            self.ship.moving_right = True                              #将右移标志置为 True

        elif event.key == pygame.K_q:
            sys.exit()                              

        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:    #触发飞船左移按键(K_LEFT or K_a)事件
            self.ship.moving_left = True                               #将左移标志置为 True
        
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """响应键盘按键松开"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:     #触发飞船右移按键(K_RIGHT or K_d)松开事件  
            self.ship.moving_right = False                             #将右移标志置为 False

        if event.key == pygame.K_LEFT or event.key == pygame.K_a:      #触发飞船左移按键(K_LEFT or K_a)松开事件
            self.ship.moving_left = False                              #将左移标志置为 False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组 bullets 中"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _undate_screen(self):
        """更新屏幕上的图像，并切换到更新屏幕"""
        # 每次循环时重绘屏幕
        self.screen.fill(self.settings.bg_color)
        #在窗口显示飞船
        self.ship.blitme()
        #在窗口中显示所有子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
    
        #让最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == '__main__' :
    #创建游戏实例并运行游戏。
    ai = AlenInvasion()
    ai.run_game()



