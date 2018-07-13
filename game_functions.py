
import sys
import pygame

from bullet import Bullet
from alien import Alien
from time import sleep

#响应按键
def chect_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
        
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

    #退出
    elif event.key == pygame.K_ESCAPE:
        sys.exit()

#开火
def fire_bullet(ai_settings, screen, ship, bullets):
    # 创建一颗子弹加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

#响应释放按键
def chect_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, play_button, ship, bullets):

    # 鼠标和键盘事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type==pygame.KEYDOWN:
            chect_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type==pygame.KEYUP:
            chect_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y)

def check_play_button(stats, play_button, mouse_x, mouse_y):
    """玩家单击Play开始新游戏"""
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True

def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button):
    #更新屏幕图像并切换到新屏幕

    #在循环时重绘屏幕
    screen.fill(ai_settings.bg_color)
    
    #在飞船和外星人之后重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    #若是非活动状态就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 屏幕可见
    pygame.display.flip()

#更新子弹的位置并删除已经消失的子弹
def update_bullets(ai_settings, screen, ship, aliens, bullets):

    #更新子弹位置
    bullets.update()
    #删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    #检查是否有子弹击中目标
    collisions =pygame.sprite.groupcollide(bullets, aliens, True, True)

    #删除现有的子弹并新建一群外星人
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


"""计算每行可容纳的外星人"""
def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x/(2 * alien_width))
    return number_aliens_x

"""计算屏幕可容纳多少外星人"""
def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height -
                            (3 * alien_height) - ship_height)
    number_rows = int(available_space_y/(2 * alien_height))
    return number_rows

"""创建一个外星人放在当前行"""
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

"""创建外星人群"""
def create_fleet(ai_settings, screen, ship, aliens):
    #创建一个外星人并计算一行可容纳多少个外星人
    #（间距为外星人宽度）
    alien= Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                    alien.rect.height)

    #创建外星人群
    for row_number in range(number_rows):
        #创建第一行外星人
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                            row_number)


"""在外星人到达边缘时采取措施"""
def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

"""下移整群外星人并改变他们的方向"""
def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

"""响应被外星人撞到的飞船"""
def ship_hit(ai_settings, stats,screen, ship,aliens, bullets):
    """响应飞船遭遇碰撞"""
    if stats.ships_left > 0:
        #将ships_left减一
        stats.ships_left -= 1

        #清空外星人及子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，将飞船放到屏幕底端
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #暂停
        sleep(0.5)
    else:
        stats.game_active = False

"""检查是否有外星人撞到屏幕底端"""
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            #处理为飞船被撞
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

"""检查边缘，更新外星人群的位置"""
def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings, stats, screen, ship,aliens, bullets)
        print("Ship hit!!!")
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)