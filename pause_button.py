import pygame.font


class Pause:

    def __init__(self, ai_game, msg):
        # 初始化按钮属性
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # 按钮的尺寸和其他参数
        self.width = 200
        self.height = 50
        self.button_color = (255, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 45)

        # 按钮的rect对象，居中
        # 问题就在这！我只是隐藏了按钮，没有绘制了，但是当我点击相应位置，还是会触发效果
        # 解决方法
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 标签
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        # 将msg渲染为图像并在键盘上居中
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制按钮和文本
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
