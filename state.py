class GameState:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_screen = "main_menu"
        self.selected_menu_index = 0
        self.chosen_character = None
        self.player_rect = None
        self.enemy_rect = None
        self.enemy_active = True
        self.enemy_speed = 2
        self.projectiles = []
        self.score = 0

    def reset(self):
        self.current_screen = "main_menu"
        self.selected_menu_index = 0
        if self.player_rect:
            self.player_rect.center = (self.screen_width //  2, self.screen_height //2)
        self.enemy_rect = None
        self.enemy_active = True
        self.projectiles.clear()
        self.score = 0
       
