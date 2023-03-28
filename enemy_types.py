import random

import pygame
import math

from npc import Npc
from shot import BounceShot


class Human(Npc):
    def __init__(self):
        super().__init__()
        self.hp = 20
        self.damage = 0
        self.friend = True
        self.sprite = random.randint(0, 2)
        self.vel = pygame.math.Vector2(0, 0)
        self.anim_path(0)
        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.move_timer = 0

    def move(self):
        if self.move_timer > 0:
            self.move_timer -= 1
        else:
            self.move_timer = 100
            num = random.randint(0, 7)
            angle = num / 8 * math.pi * 2
            self.vel = pygame.math.Vector2(math.cos(angle), math.sin(angle))
            self.anim_path(num)
        self.pos += self.vel * 1.5
        if self.pos.x < 200 or self.pos.x > 1400 or self.pos.y < 100 or self.pos.y > 800:
            self.move_timer = 0
        else:
            self.rect.center = [int(self.pos.x), int(self.pos.y)]

    def anim_path(self, num):
        path = ''
        if self.sprite == 0:
            path = 'Daddy'
        elif self.sprite == 1:
            path = 'Mommy'
        elif self.sprite == 2:
            path = 'Tommy'
        if 0 <= num < 2 or num == 7:
            self.load_path('Sprites/Family/'+path+'/'+path+'_Walk_Right')
        elif num == 2:
            self.load_path('Sprites/Family/'+path+'/'+path+'_Walk_Down')
        elif 2 < num <= 5:
            self.load_path('Sprites/Family/'+path+'/'+path+'_Walk_Left')
        else:
            self.load_path('Sprites/Family/'+path+'/'+path+'_Walk_Up')



class Grunt(Npc):
    def __init__(self):
        super().__init__()
        self.hp = 1
        self.damage = 1
        self.make_ship('Sprites/EnemyGrunt', 'Sprites/enemy_fire')
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
        self.hp = 999
        self.shot_speed = 5
        self.shot_time = 150
        self.damage = 1
        self.shot_tilt = 0
        self.make_ship('Sprites/EnemyHulk/Hulk_Walk_Down_Up', 'Sprites/enemy_fire2')
        self.move_timer = 0
        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.vel = pygame.math.Vector2(0, 0)
        self.catcher = True

    def move(self):
        if self.move_timer > 0:
            self.move_timer -= 1
        else:
            self.move_timer = 150
            num = random.randint(0, 3)
            angle = num / 4 * math.pi * 2
            self.anim_path(num)
            self.vel = pygame.math.Vector2(math.cos(angle), math.sin(angle))
        self.pos += self.vel
        if self.pos.x < 200 or self.pos.x > 1400 or self.pos.y < 100 or self.pos.y > 800:
            self.move_timer = 0
        else:
            self.rect.center = [int(self.pos.x), int(self.pos.y)]

    def anim_path(self, num):
        if num == 0:
            self.load_path('Sprites/EnemyHulk/Hulk_Walk_Right')
        elif num == 1:
            self.load_path('Sprites/EnemyHulk/Hulk_Walk_Down_Up')
        elif num == 2:
            self.load_path('Sprites/EnemyHulk/Hulk_Walk_Left')
        else:
            self.load_path('Sprites/EnemyHulk/Hulk_Walk_Down_Up')


class Electrode(Npc):
    def __init__(self):
        super().__init__()
        self.hp = 1
        self.damage = 1
        self.make_ship('Sprites/Electrodes', 'Sprites/enemy_fire')
        self.move_timer = 0
        self.target = pygame.math.Vector2(0, 0)


class Tank(Npc):
    def __init__(self, ):
        super().__init__()
        self.hp = 1
        self.shot_speed = 5
        self.shot_time = 150
        self.damage = 1
        self.shot_tilt = 0
        self.make_ship('Sprites/EnemyTank/Idle', 'Sprites/EnemyTank/Bullet')
        self.move_timer = 0
        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.vel = pygame.math.Vector2(0, 0)
        self.aimed = True
        self.target = pygame.math.Vector2(0, 0)

    def move(self):
        if self.move_timer > 0:
            self.move_timer -= 1
        else:
            self.move_timer = 150
            num = random.randint(0, 7)
            angle = num / 8 * math.pi * 2
            self.vel = pygame.math.Vector2(math.cos(angle), math.sin(angle))
            # self.anim_path(num)
        self.pos += self.vel * 1
        if self.pos.x < 200 or self.pos.x > 1400 or self.pos.y < 100 or self.pos.y > 800:
            self.move_timer = 0
        else:
            self.rect.center = [int(self.pos.x), int(self.pos.y)]

    def anim_path(self, num):
        pass

    def create_shots(self):
        shot_direction = pygame.math.Vector2(self.target.x - self.rect.centerx,
                                             self.target.y - self.rect.centery).normalize()
        shots = [BounceShot(self, shot_direction.x, shot_direction.y, shot_direction.x, shot_direction.y, 2)]
        return shots

    def set_target(self, target):
        self.target = target

