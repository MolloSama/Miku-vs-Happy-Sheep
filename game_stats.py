class GameStats():
    """跟踪统计信息"""
    def __init__(self, ai_settings):
        """初始化"""
        self.ai_settings=ai_settings
        self.reset_stats()

        #让游戏在开始处于非活动状态
        self.game_active = False


    def reset_stats(self):
        self.ships_left=self.ai_settings.ship_limit
