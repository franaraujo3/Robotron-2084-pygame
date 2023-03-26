import random

import pygame
import math

from npc import Npc
from shot import Shot
from shot import SplitShot


class Human(Npc):
    def __init__(self):
        super().__init__()
        self.hp = 20
        self.damage = 0
        self.friend = True
        self.make_ship('Sprites/Player', 'Sprites/enemy_fire')
        self.move_timer = 0
        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.vel = pygame.math.Vector2(0, 0)

    def move(self):
        if self.move_timer > 0:
            self.move_timer -= 1
        else:
            self.move_timer = 100
            angle = random.randint(0, 7) / 8 * math.pi * 2
            self.vel = pygame.math.Vector2(math.cos(angle), math.sin(angle))
        self.pos += self.vel * 1.5
        self.rect.center = [int(self.pos.x), int(self.pos.y)]


class Grunt(Npc):
    def __init__(self):
        super().__init__()
        self.hp = 20
        self.damage = 1
        self.make_ship('Sprites/enemy_1', 'Sprites/enemy_fire')
        self.move_timer = 0
        self.aimed = True
        self.target = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)

    def move(self):
        if self.move_timer > 0:
            self.move_timer -= 1
        else:
            self.move_timer = random.randint(20, 200)
            vector = pygame.math.Vector2(self.target.x - self.pos.x,
                                         self.target.y - self.pos.y)
            angle = math.radians(pygame.math.Vector2(1, 0).angle_to(vector))
            angle = round(angle / (math.pi / 4)) * math.pi / 4
            vector = pygame.math.Vector2(math.cos(angle), math.sin(angle))
            self.pos += vector*75
            self.rect.center = [int(self.pos.x), int(self.pos.y)]

    def set_target(self, target):
        self.target = target


class Hulk(Npc):
    def __init__(self, ):
        super().__init__()
        self.hp = 40
        self.shot_speed = 5
        self.shot_time = 150
        self.damage = 1
        self.shot_tilt = 0
        self.make_ship('Sprites/enemy_2', 'Sprites/enemy_fire2')
        self.move_timer = 0
        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.vel = pygame.math.Vector2(0, 0)

    def move(self):
        if self.move_timer > 0:
            self.move_timer -= 1
        else:
            self.move_timer = 150
            angle = random.randint(0, 3) / 4 * math.pi * 2
            self.vel = pygame.math.Vector2(math.cos(angle), math.sin(angle))
        self.pos += self.vel
        self.rect.center = [int(self.pos.x), int(self.pos.y)]
