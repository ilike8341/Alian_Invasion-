# 在python里self到底是什么呢，为什么函数（方法）都要传递self
# 窗口及响应输入文件
#好好再看看ufo创建的代码
#暫停处理的鼠标很完美
#问题：1、boss阶段前子弹不能消失ok2、应用图标，打包的时候一起解决3、boss的追踪弹4、boss的血条
import sys
import pygame
import cv2
from time import sleep

from pygame.examples.aliens import Score

from bullet import Bullet
from settings import Settings
from ship import Ship
from bullet import Bullet
from beam import Beam, WhiteBeam
from alien import UfoNormal
from game_stats import GameStats
from buttom import Bottom
from pause_button import Pause
# 按钮拼写错了，后面改一下
from scoreboard import Scoreboard


# opencv可能会有用的


class AlienInvasion:
    # 管理游戏资源及行为
    def __init__(self):
        # 初始化并创建游戏资源
        pygame.init()
        # 创建Setting实例访问
        self.settings = Settings()

        # 与键盘输入有关，加了这句输入正常，也不用一定要改英文输入法！
        pygame.key.stop_text_input()

        # 窗口与标题
        # 全屏，以后加个功能
        # self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.settings.screen_width=self.screen.get_rect().width
        # self.settings.screen_height=self.screen.get_rect().height
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        self.stats = GameStats(self)
        self.ship = Ship(self)

        # 子弹编组
        self.bullets = pygame.sprite.Group()

        # 激光编组
        self.beams = pygame.sprite.Group()
        self.white_beams = pygame.sprite.Group()

        # 外星人编组
        # 普通
        self.ufo_normal_group = pygame.sprite.Group()

        self._create_normal_fleet()

        # boss检查,对已经出现的外星人normal计数
        self.total_alien_normal = 0

        # 创建play按钮和暂停按钮
        self.play_button = Bottom(self, 'PLAY')
        self.pause_button = Pause(self, 'CONTINUE')

        # 背景音乐
        pygame.mixer.init()
        # music跟sound有何不同呢
        pygame.mixer.music.set_volume(self.settings.music_volume)
        pygame.mixer.music.load('KALAX - Vice.ogg')
        pygame.mixer.music.play()

        # 计分
        self.scoreboard = Scoreboard(self)

    def run_game(self):
        # 游戏主循环
        while True:
            # 监控键盘和鼠标事件
            self._check_events()

            if self.stats.game_active and not self.stats.game_pause:
                self.ship.update()
                self._update_bullets()
                self._update_beams()
                self._update_white_beams()
                self._update_ufo_normal()
                self._update_ufo_boss()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            # 退出
            if event.type == pygame.QUIT:
                sys.exit()
            # 真能动了，这里pygame必帮忙简化了代码
            # 按下持续动
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                #天才的检查条件
                if not self.stats.game_active and not self.stats.game_pause:
                    self._check_play_buttom(mouse_pos)
                else:
                    self._check_pause_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_(event)

    def _check_play_buttom(self, mouse_pos):
        # 单击play时开始游戏
        # 游戏中不会被点击和重复开始
        play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        #这个and not 有什么用吗
        if play_button_clicked and not self.stats.game_active:
            # 重置设置
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True

            self.ufo_normal_group.empty()
            self.bullets.empty()

            self._create_normal_fleet()
            self.ship.center_ship()

            self.scoreboard.prep_score()
            self.scoreboard.prep_ships()

            # 游戏中隐藏光标
            pygame.mouse.set_visible(False)

    def _check_pause_button(self, mouse_pos):
       #暂停后继续
        pause_button_clicked = self.pause_button.rect.collidepoint(mouse_pos)
        if pause_button_clicked and self.stats.game_pause:
            self.stats.game_active = True
            self.stats.game_pause = False
        pygame.mouse.set_visible(False)

    def _update_screen(self):
        # 让最新绘制屏幕可见
        # 背景这里目前还很抽象
        # 下面两句作用目前好像没有
        # self.settings.image_rect = self.settings.img.get_rect(center=self.screen.get_rect().center)
        # self.screen.fill(self.settings.bg_color) #fill只接受颜色
        self.screen.blit(self.settings.img, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
            # beam不能快，总是'Beam' object has no attribute 'draw_bullet'
            # 而且我还没加碰撞消消乐，肯定是哪个编组写错了
        for beam in self.beams.sprites():
            beam.draw_beam()
        # 我说怎么没显示，原来没画出来
        for white_beam in self.white_beams.sprites():
            white_beam.draw_beam()
        # 编组方法draw,blit感觉是一个显示图像的办法
        self.ufo_normal_group.draw(self.screen)

        # 显示计分
        self.scoreboard.show_score()

        # 按钮
        #按钮消失在这里，没开始状态就是绘制
        if not self.stats.game_active and not self.stats.game_pause:
            self.play_button.draw_buttom()
        if not self.stats.game_active and self.stats.game_pause:
            self.pause_button.draw_button()
            pygame.mouse.set_visible(True)

        pygame.display.flip()

    def _check_keydown_(self, event):
        # q只会停止飞船运动，却不退出
        # 改成SPACE可以，字母却不行
        # 输入法要是英文！
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_p:
            #只添加这个会回到play初始，也许需要增加变量
            self.stats.game_pause = True
            self.stats.game_active = False
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
        if event.key == pygame.K_a:
            self._fire_beam()
            self._fire_white_beam()
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
            # 向右
            # 移动速度怎么改？两1改着改着动不了了,可能跟1像素已经够小了有关
            # 说是与只能存储整数有关
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = True

    def _check_keyup_(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        # 创建子弹加入编组
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            bullet_sound = pygame.mixer.Sound('bullet_sound.wav')
            bullet_sound.set_volume(0.2)
            pygame.mixer.Sound.play(bullet_sound)

    def _fire_beam(self):
        # 激光加入编组
        new_beam = Beam(self)
        # 这地方写成self.bullets.add(new_beam)了，难怪
        self.beams.add(new_beam)
        beam_sound = pygame.mixer.Sound('beam_sound.wav')
        beam_sound.set_volume(0.2)
        pygame.mixer.Sound.play(beam_sound)

    def _fire_white_beam(self):
        # 激光加入编组
        new_beam = WhiteBeam(self)
        # 这地方写成self.bullets.add(new_beam)了，难怪
        self.white_beams.add(new_beam)

    def _update_bullets(self):
        self.bullets.update()
        # 删除子弹
        for bullet in self.bullets.sprites():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # 有机会改成子弹数变了再显示
        # print(len(self.bullets))
        # 子弹击中
        self._normal_bullet_collision()

    def _update_beams(self):
        self.beams.update()
        self._normal_beam_collision()
        for beam in self.beams.sprites():
            if beam.rect.width <= 0:
                self.beams.remove(beam)

    def _update_white_beams(self):
        self.white_beams.update()
        self._normal_beam_collision()
        for white_beam in self.white_beams.sprites():
            if white_beam.rect.width <= 0:
                self.beams.remove(white_beam)

    def _create_normal_fleet(self):
        # 普通ufo创建
        ufo_normal = UfoNormal(self)
        # 所以自己这里修改只有理解才能改好！光复制抄没意义的
        # 意外实参,给的时候不用给self
        for ufo_normal_row_number in range(self.settings.ufo_normal_row_number):
            for ufo_normal_line_number in range(self.settings.ufo_normal_line_number):
                self._create_normal_ufo(ufo_normal_line_number, ufo_normal_row_number)

    def _create_normal_ufo(self, ufo_normal_line_number, ufo_normal_row_number):
        ufo_normal = UfoNormal(self)
        ufo_normal.x = self.settings.ufo_normal_first_show_x + \
                       2 * self.settings.ufo_normal_width * \
                       ufo_normal_line_number
        ufo_normal.y = self.settings.ufo_normal_first_show_y + \
                       2 * self.settings.ufo_normal_height * \
                       ufo_normal_row_number
        ufo_normal.rect.x = ufo_normal.x
        ufo_normal.rect.y = ufo_normal.y
        # 这地方的类型报错是啥
        self.ufo_normal_group.add(ufo_normal)

    def _check_normal_fleet_edges(self):
        # 到达边缘
        for ufo_normal in self.ufo_normal_group.sprites():
            if ufo_normal.check_edges():
                self._change_normal_fleet_directions()
                break

    def _change_normal_fleet_directions(self):
        # 我下移思路有点不一样
        # 这里方向控制还要考虑
        self.settings.ufo_normal_x_direction *= -1
        self.settings.ufo_normal_y_direction = 1

    def _normal_bullet_collision(self):
        # 后面可能得合并一下collisions
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.ufo_normal_group, True, True)
        explode_sound = pygame.mixer.Sound('explode.wav')
        explode_sound.set_volume(0.2)
        if collisions:
            # 真能放声音，我想到的是每次collisions都被定义，所以每创一次都从False到True，妙
            pygame.mixer.Sound.play(explode_sound)
            self.stats.score += self.settings.ufo_normal_points
            # 计分修改
            # 如果只用if字典存在,无法处理一个子弹同时打中多敌人情况
            for ufo_normals in collisions.values():
                self.stats.score += self.settings.ufo_normal_points * (len(ufo_normals) - 1)
                # 子弹为啥上来一个加100?先手动减个1
                self.scoreboard.prep_score()
                self.scoreboard._check_high_score()
        if not self.ufo_normal_group:
            # 为啥要删除子弹
            # 打完了就加,beam那好像不用写这个？
            if self._boss_check():
                self._create_normal_fleet()
                #千万不能放后面，不然速度起飞了
                self.settings.increase_speed()
                self.total_alien_normal += 8
                self.bullets.empty()
                self.beams.empty()
                self.white_beams.empty()
            #都放在Boss_check里，子弹问题解决了，满足boss出来不删子弹，后面得触发一个标志
            #打boss的时候需要删子弹，激光最好是延迟删？可能有点难搞



    def _normal_beam_collision(self):
        # 这里两个叠加碰撞还有一些问题
        collisions = pygame.sprite.groupcollide(
            self.beams, self.ufo_normal_group, False, True)
        for collision in collisions.values():
            self.stats.score += self.settings.ufo_normal_points * len(collision)
            self.scoreboard.prep_score()
            self.scoreboard._check_high_score()
        pygame.sprite.groupcollide(
            self.white_beams, self.ufo_normal_group, False, True)

    def _ship_hit(self):
        # 掉一条命
        if self.stats.ships_left > 0:
            self.ship.center_ship()
            self.ufo_normal_group.empty()
            self.bullets.empty()

            self._create_normal_fleet()
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()
            sleep(0.5)
            # 下一条命

        else:
            # print("You are done!")
            # sys.exit()
            # 精灵到底是什么
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_ufo_normal(self):
        self._check_normal_fleet_edges()
        self.ufo_normal_group.update()

        if pygame.sprite.spritecollideany(self.ship, self.ufo_normal_group):
            self._ship_hit()

        self._check_aliens_bottom()

    '''def _update_ufo_boss(self):
        self._check_boss_edges()
        self.ufo_boss_one.update()
        
        if pygame.sprite.spritecollideany(self.ship, self.ufo_boss_one):
            self._ship_hit()

        # 当然boss不一样，到底线了就弹回去
        self._check_boss_bottom()
     '''


    def _check_aliens_bottom(self):
        # 当错过外星人时给予惩罚
        screen_rect = self.screen.get_rect()
        for ufo_normal in self.ufo_normal_group.sprites():
            if ufo_normal.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _boss_check(self):
        if self.total_alien_normal >= self.settings.until_boss-8:
            #问题在于检查数量在collision里，最开始创建的额一组数量被忽略了
            return False
        else:
            return True


if __name__ == '__main__':
    # 创建游戏实例并运行
    ai = AlienInvasion()
    ai.run_game()
