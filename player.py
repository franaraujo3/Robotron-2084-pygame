import math

from ship import Ship
from shot import Shot
from config import *


class PlayerShip(Ship):
    def __init__(self, sheet, pos):
        super().__init__()
        self.score = 0
        self.shot_time = 10
        self.shot_speed = 10
        self.move_speed = 6
        self.damage = 10
        self.max_hp = 5
        self.hp = 5
        self.make_ship(sheet, 'Sprites/fire')
        self.rect.center = (pos[0], pos[1])
        self.invincibility_time = 100
        self.invincible_timer = 0
        self.vel = pygame.math.Vector2(0, 0)
        self.store = pygame.math.Vector2(0, 0)

    def go(self, axis, speed):
        if self.vel[axis] == speed*-1:
            self.store[axis] = self.vel[axis]
        self.vel[axis] = speed

    def stop(self, axis, speed):
        if self.vel[axis] == speed:
            self.vel[axis] = self.store[axis]
            self.store[axis] = 0
        elif speed == self.store[axis]:
            self.store[axis] = 0

    def lose_hp(self, damage):
        if self.invincible_timer <= 0:
            super().lose_hp(damage)
            self.invincible_timer = self.invincibility_time

    def shoot_(self):
        self.shoot = True

    def create_shots(self):
        vector = pygame.math.Vector2(pygame.mouse.get_pos()[0]-self.rect.x,
                                     pygame.mouse.get_pos()[1]-self.rect.y)
        vector.normalize()
        angle = math.radians(pygame.math.Vector2(1, 0).angle_to(vector))
        angle = round(angle/(math.pi/4))*math.pi/4
        shots = [Shot(self, 40 * math.cos(angle)+8,
                      40 * math.sin(angle)+15,
                      math.cos(angle),
                      math.sin(angle))]
        shotSoundEffect.play()
        return shots

    def move(self):
        speed = self.vel.copy()
        if speed.length() > 0:
            speed.normalize()
        if 0 < self.rect.x + speed[0] * self.move_speed < screen_width-self.rect.width:
            self.rect.x += speed[0] * self.move_speed
        if 0 < self.rect.y + speed[1] * self.move_speed < screen_height-self.rect.height:
            self.rect.y += speed[1] * self.move_speed

    def update(self):
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        self.alpha = 255-255*self.invincible_timer/100
        super().update()
