from config import *
from enemy_types import *
from wave import Wave


class Levels:
    def __init__(self, level):
        self.group = pygame.sprite.Group()
        self.rounds = []
        self.progress = 0
        self.wave_progress = 0
        self.get_level(level)
        self.wall_color = "#d4a941"
        self.bg_color = "#150d28"

        # for layout in self.layouts[layout_type - 1]:
        #    self.group.add(wall.Wall(self.wall_color, layout[0], layout[1]))

    def get_group(self):
        return self.group

    def get_bg_color(self):
        return self.bg_color

    def get_level(self, level):
        self.progress = 0
        self.wave_progress = 0
        self.rounds = []
        if level == 0:
            waves = [Wave(0, 3), Wave(1, 10)]
            self.rounds.append(waves)
            waves = [Wave(0, 6), Wave(1, 2), Wave(1, 2)]
            self.rounds.append(waves)
            waves = [Wave(2, 10)]
            self.rounds.append(waves)
            waves = [Wave(1, 3), Wave(2, 6)]
            self.rounds.append(waves)
            waves = [Wave(0, 6), Wave(2, 6),
                     Wave(1, 2), Wave(1, 2)]
            self.rounds.append(waves)
        pass

    @staticmethod
    def make_enemy(number):
        enemy = None
        if number == 0:
            enemy = Human()
        elif number == 1:
            enemy = Grunt()
        elif number == 2:
            enemy = Hulk()
        return enemy
