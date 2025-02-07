import pygame
from pygame.sprite import Sprite
#精灵库，说是可以使用编组啥的

class Bullet(Sprite):
    #子弹类

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #我是图片作为子弹，所以这里会有点不同
        #做beam的时候借用这个
        self.image = pygame.image.load('bullet.png')
        self.rect = self.image.get_rect()
        self.rect.midtop=ai_game.ship.rect.midtop

        #子弹位置
        #不像书上用y,与飞船坐标做一个区分
        self.bullet_y = ai_game.ship.rect.y

    def update(self):
        #自动向上移动
        self.bullet_y -= self.settings.bullet_speed
        self.rect.y = self.bullet_y

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)

