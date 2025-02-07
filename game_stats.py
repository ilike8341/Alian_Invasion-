from settings import Settings


class GameStats:
    def __init__(self, ai_game):
        self.game_active = False
        self.settings = Settings()
        self.screen = ai_game.screen
        self.reset_stats()

        self.game_pause = False

        #最高得分不应重置
        #后面搞个文件记录最高得分
        self.high_score = 0



    def reset_stats(self):
        #初始化
        #每次重来时，重置命数和分数
        self.ships_left =self.settings.ship_limit
        self.score = 0