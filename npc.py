import math
import random

from ship import Ship
from shot import Shot
from config import *


class Npc(Ship):
    def __init__(self):
        super().__init__()
        self.rect.x = random.randint(200, 1400)
        self.rect.y = random.randint(200, 700)
        self.aimed = False
        self.friend = False

    def update(self):
        self.shoot = True
        super().update()
