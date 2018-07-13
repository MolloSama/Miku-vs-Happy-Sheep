
import sys
import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from alien import Alien
from pygame.sprite import Group
import game_functions as gf

def run_game():

    #游戏窗口初始化
    pygame.init()
    #从settings.py中获取
    ai_settings=Settings()

    screen=pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("MIKU大战喜羊羊")

    #创建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    #用于储存游戏信息的实例
    stats = GameStats(ai_settings)

    #创建飞船
    ship=Ship(ai_settings, screen)

    #创建储存子弹的编组
    bullets = Group()

    #创建外星人
    aliens = Group()
    #创建外星人编组
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #游戏主循环
    while True:

        # 鼠标和键盘事件
        gf.check_events(ai_settings, screen, stats, play_button, ship, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        #用背景色重绘屏幕
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button)

run_game()
