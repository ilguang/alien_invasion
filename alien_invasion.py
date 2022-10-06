import sys
from time import sleep
from turtle import Screen
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlenInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        #设置类
        self.settings = Settings()
        #设置game窗口大小
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, 
            self.settings.screen_height),
            pygame.RESIZABLE
        )
        #设置game窗口标题
        pygame.display.set_caption("Alien Invasion")
        #创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)
        #创建一搜飞船
        self.ship = Ship(self)
        #创建一个存储子弹的编组
        self.bullets = pygame.sprite.Group()
        #创建一个存储外星人的编组
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    
    
    def _create_fleet(self):
        """创建外星人群"""
        #创建一个外星人,并计算一行可容纳多少个外星人
        #外星人的间距为外星人宽度
        alien = Alien(self)
        #拿到外星人所在矩形的宽、高
        alien_width, alien_height = alien.rect.size
        #拿到除了屏幕两边各需要留出来一个外星人宽度身位的空间外其余的屏幕宽度
        available_space_x = self.settings.screen_width - (2 * alien_width) 
        #拿到屏幕 空闲宽度 可容纳 外星人以及外星人之间的一个外星人宽度的 个数
        number_aliens_x = available_space_x // (2 * alien_width)

        #计算屏幕可容纳多少外星人
        #拿到飞船高度
        ship_height = self.ship.rect.height
        #拿到屏幕空闲高度
        available_space_y = (
            self.settings.screen_height - (3 * alien_height) - ship_height
        )
        #计算屏幕空闲高度中可容纳外星人的个数
        number_rows = available_space_y // (2 * alien_height)

        #创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                #创建一个外星人并将其加入当前行
                self._create_alien(alien_number,row_number)

    def _create_alien(self, alien_number,row_number):
        """创建一个外星人，并将其放在当前行"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """将整群外星人下移，并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def run_game(self):
        """开始游戏的主循环"""
        while True :
            #监事键盘和鼠标事件
            self._check_events()

            if self.stats.game_active:
                #飞船移动后位置更新
                self.ship.update()
                #更新子弹的位置并删除消失的子弹
                self._update_bullets()
                #更新外星人的位置
                self._update_aliens()

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
        if len(self.bullets) < self.settings.bullet_allowed:#限制子弹数量
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):  
        """更新子弹的位置并删除消失的子弹"""
        #更新 bullets 编组中所有子弹的位置
        self.bullets.update()
        #删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        #检查子弹是否击中外星人
        #如果是，就删除相应的子弹和外星人
        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞"""
        #删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets,self.aliens,True,True
        )
        #判断外星人是否全部消灭
        if not self.aliens:
            #删除现有的子弹并新建一群外星人
            self.bullets.empty()
            self._create_fleet()
        

    def _update_aliens(self):
        """
        检查是否有外星人位于屏幕边缘
        并更新整群外星人的位置
        """
        self._check_fleet_edges()
        self.aliens.update()

        #检查外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        #检查是否有外星人到达了屏幕低端
        self._check_aliens_bottom()

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left > 0:    
            #将 ship_left 减 1
            self.stats.ships_left -= 1

            #清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人，并将飞船放到屏幕低端的中央
            self._create_fleet()
            self.ship.center_ship()

            #暂停
            sleep(0.5)
        else:
            #飞船个数用完后标志置为 False
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        """检测是否有外星人到达了屏幕低端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #象飞船被撞到一样处理
                self._ship_hit()
                break

    def _undate_screen(self):
        """更新屏幕上的图像，并切换到更新屏幕"""
        # 每次循环时重绘屏幕
        self.screen.fill(self.settings.bg_color)
        #在窗口显示飞船
        self.ship.blitme()
        #在窗口中显示所有子弹
        for bullet in self.bullets.sprites(): 
            bullet.draw_bullet()
        #在窗口显示外星人
        self.aliens.draw(self.screen)

        #让最近绘制的屏幕可见
        pygame.display.flip()

if __name__ == '__main__' :
    #创建游戏实例并运行游戏。
    ai = AlenInvasion()
    ai.run_game()



