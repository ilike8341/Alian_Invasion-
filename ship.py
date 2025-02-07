import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    # 管理飞船
    def __init__(self, ai_game):
        super().__init__()
        # 初始化飞船,初始位置
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.screen_rect = ai_game.screen.get_rect()

        self.ship_width = 130
        self.ship_height = 120

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # 加载图像获取外接矩形
        # load返回surface
        # (0,0)是左上角
        self.image = pygame.image.load('ship.png')
        # (自加)改飞船图片尺寸
        self.image = pygame.transform.scale(self.image, (self.ship_width, self.ship_height))
        self.rect = self.image.get_rect()

        # 新飞船放在屏幕底部中央
        # 为什么不再中间了？好像是x坐标限制住了
        # 放到self.x计算上面又好了
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        # 指定位置绘制飞船
        self.screen.blit(self.image, self.rect)

    # 注意y轴方向,rect属性
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_x_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_x_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_y_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_y_speed

        # 新建x以存储小数，在连续低速时很有用
        # self.rect.x还是只能读取整数输出,不是那么精确
        self.rect.x = self.x
        self.rect.y = self.y

    def center_ship(self):
        # 这个击杀环节有点问题
        # 哎呀！应该是忘了我比他多的y了,现在好了
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)



