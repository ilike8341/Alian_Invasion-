import pygame


class Settings:
    # 所有设置

    # 静态设置
    def __init__(self):
        # 屏幕
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        self.ship_x_speed = 0.5
        self.ship_y_speed = 0.5
        self.ship_limit = 3

        self.bullet_speed = 1
        self.bullet_allowed = 5

        self.beam_width = 50
        self.beam_color = (60, 60, 60)

        self.white_beam_width = 25
        self.white_beam_color = (255, 255, 255)

        self.ufo_normal_first_show_x = 50
        self.ufo_normal_first_show_y = 50
        self.ufo_boss_first_show_x = 150
        self.ufo_boss_first_show_y = 100

        self.ufo_normal_width = 120
        self.ufo_normal_height = 62
        self.ufo_normal_line_number = 4
        self.ufo_normal_row_number = 2
        self.ufo_normal_x_speed = 0.3
        self.ufo_boss_x_speed = 0.3
        self.ufo_normal_y_speed = 0.03
        self.ufo_boss_y_speed = 0.03
        # 水平方向标志,1为向右,-1向左,0不动
        self.ufo_normal_x_direction = 1
        self.ufo_boss_x_direction = 1
        # 竖直方向标志,1为向下,-1为向上,0不动
        self.ufo_normal_y_direction = 0
        self.ufo_boss_y_direction = 0
        # self.ufo_normal_line_available_space = 100
        # self.bullet.width
        # self.bullet.height
        # self.bullet.color

        #直到boss出来之前需要击毁的ufo数量
        self.until_boss = 24


        # 背景
        self.img = pygame.image.load("background.png")
        self.img = pygame.transform.scale(self.img, (self.screen_width, self.screen_height))

        # 音乐
        self.music_volume = 0.5

        # 动态：提升等级
        # self.speedup_scale = 1.05
        self.ship_speedup_x_scale = 1.05
        self.ship_speedup_y_scale = 1.05
        self.ufo_normal_speedup_x_scale = 1.05
        self.ufo_normal_speedup_y_scale = 1.05

        self.ufo_points_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # 初始化动态设置
        self.ship_x_speed = 0.5
        self.ship_y_speed = 0.5
        self.ufo_normal_line_number = 4
        self.ufo_normal_x_speed = 0.3
        self.ufo_normal_y_speed = 0.03

        self.ufo_normal_x_direction = 1
        self.ufo_normal_points = 50

    def increase_speed(self):
        self.ship_x_speed = self.ship_x_speed * self.ship_speedup_x_scale
        self.ship_y_speed = self.ship_y_speed * self.ship_speedup_y_scale
        self.ufo_normal_x_speed = self.ufo_normal_x_speed * self.ufo_normal_speedup_x_scale
        self.ufo_normal_y_speed = self.ufo_normal_y_speed * self.ufo_normal_speedup_y_scale
        #注意！AI可能会生成一些出乎意料的自动代码
        self.ufo_normal_points = int(self.ufo_normal_points * self.ufo_points_scale)

