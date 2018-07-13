
import pygame
from pygame.sprite import Sprite

#表示单个外星人的类
class Alien(Sprite):

    #初始化外星人并设置其起始位置
    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载外星人图像并设置其rect属性
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        #外星人初始在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #储存外星人准确位置
        self.x = float(self.rect.x)

    #在指定位置绘制
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    """检查是否撞到屏幕边缘"""

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    #向左/右移动外星人
    def update(self):
        self.x += (self.ai_settings.alien_speed * self.ai_settings.fleet_direction)
        self.rect.x=self.x

