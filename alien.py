import pygame
from pygame.sprite import Sprite


class UfoNormal(Sprite):
    # 普通外星敌人
    def __init__(self, ai_game):
        super().__init__()
        # 经典屏幕和设置实例
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 图像
        self.image = pygame.image.load('ufo_normal.png')
        self.rect = self.image.get_rect()

        # 出现位置
        # settings这里不导入库也有，因为从ai_game实例来的
        self.rect.x = self.settings.ufo_normal_first_show_x
        self.rect.y = self.settings.ufo_normal_first_show_y

        # 外星人精确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        # 向右移动
        # 先做向右碰到边缘后向下的
        self.x += (self.settings.ufo_normal_x_speed * self.settings.ufo_normal_x_direction)
        self.y += (self.settings.ufo_normal_y_speed * self.settings.ufo_normal_y_direction)
        self.rect.x = self.x
        self.rect.y = self.y

    # 检查是否碰到边缘
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
