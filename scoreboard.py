from pygame.sprite import Group
from ship import Ship
import pygame.font

class Scoreboard:

    #显示得分
    def __init__(self,ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #字体
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)

        #各种得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_ships()

    def prep_score(self):
        #得分转换为渲染图像

        #为啥要10的整数倍?
        #不这样报错了qwq
        rounded_score = round(self.stats.score,-1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str,
            True,self.text_color,None)#透明背景
        #右上角显示
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right=self.screen_rect.right-30
        self.score_rect.top=30

    def show_score(self):
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):

        high_score = round(self.stats.score,-1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str,
            True,self.text_color,None)#透明背景
        #中间显示
        self.high_score_rect = self.score_image.get_rect()
        self.high_score_rect.right=self.screen_rect.centerx
        self.high_score_rect.top=30

    #检查最高得分
    def _check_high_score(self):
        if self.stats.score>self.stats.high_score:
            self.stats.high_score=self.stats.score
            self.prep_high_score()

    #显示等级先不做了，这些计分思路都一样的

    def prep_ships(self):
        #显示剩余命数
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)