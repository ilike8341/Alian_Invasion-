import pygame
from pygame.sprite import Sprite


class Beam(Sprite):

    # 激光类
    def __init__(self, ai_game):
        # 激光对象
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.beam_color

        self.rect = pygame.Rect(0, 0, self.settings.beam_width, self.settings.screen_height)
        self.rect.midbottom = ai_game.ship.rect.midtop
        self.width = float(self.rect.width)
        self.x = float(self.rect.x)
        self.center = float(self.rect.centerx)
        # self.beam_left = ai_game.ship.rect.x

        # 不需要y的位置，因为激光贯穿

    def update(self):
        # 现在是这玩意不起作用，激光成屏障了
        if self.width >= 0:
            self.width -= 0.2

        self.x = self.center - self.width // 2
        self.rect.width = self.width
        self.rect.x = self.x

    def draw_beam(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


#感觉可以继承Beam会更方便
class WhiteBeam(Sprite):

    # 激光类
    def __init__(self, ai_game):
        # 激光对象
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.white_beam_color

        self.rect = pygame.Rect(0, 0, self.settings.white_beam_width, self.settings.screen_height)
        self.rect.midbottom = ai_game.ship.rect.midtop
        self.width = float(self.rect.width)
        self.x = float(self.rect.x)
        self.center = float(self.rect.centerx)
        # self.beam_left = ai_game.ship.rect.x

        # 不需要y的位置，因为激光贯穿

    def update(self):
        # 现在是这玩意不起作用，激光成屏障了
        if self.width >= 0:
            self.width -= 0.25

        self.x = self.center - self.width // 2
        self.rect.width = self.width
        self.rect.x = self.x

    def draw_beam(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
