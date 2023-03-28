import math
import random
import pygame.math

from level import Levels
from player import PlayerShip
from healthbar import HealthBar
from config import *
from config import screen_height
from animation import AnimatedSprite
from GameStates.game_state import GameState

game_level = 0


class Gameplay(GameState):
    def __init__(self):
        global game_level
        super().__init__()
        self.aim_enemies = []
        level = Levels(game_level)
        self.background = level.get_bg_color()
        self.level = level
        self.score = 0
        self.humans_rescued = 0
        self.sprites = level.get_group()
        self.ships = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()
        self.humans = pygame.sprite.Group()
        self.catchers = pygame.sprite.Group()
        self.temp_pickups = []
        ship = PlayerShip('Sprites/Player/Player_Walking_Down', (screen_width / 2 - 100, screen_height - 140))
        self.health_bars = pygame.sprite.Group()
        health1 = HealthBar(ship, 'ship_healthbar', 180, 111)
        health1.rect.center = (120, 40)
        self.health_bars.add(health1)
        self.players = [ship]
        self.ships.add(ship)
        self.enemies = pygame.sprite.Group()
        for ship in self.ships.sprites():
            self.sprites.add(ship)
        self.level_progress = 0
        self.wave_progress = 0
        self.level_timer = 0
        self.transition = 2
        self.done = False
        self.died_lol = False
        self.next_state = "GAMEPLAY"
        bossChannel.play(nextLevelSoundEffect)

    # Check if an event happens
    def check_event(self, event):
        global on_boss
        if self.transition > 0:
            self.players[0].stop(1, -1)
            self.players[0].stop(1, 1)
            self.players[0].stop(0, -1)
            self.players[0].stop(0, 1)
            return
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.players[0].stop(1, -1)
            if event.key == pygame.K_s:
                self.players[0].stop(1, 1)
            if event.key == pygame.K_a:
                self.players[0].stop(0, -1)
            if event.key == pygame.K_d:
                self.players[0].stop(0, 1)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.players[0].go(1, -1)
            if event.key == pygame.K_s:
                self.players[0].go(1, 1)
            if event.key == pygame.K_a:
                self.players[0].go(0, -1)
            if event.key == pygame.K_d:
                self.players[0].go(0, 1)
            # DEBUG
            if event.key == pygame.K_r:
                self.level_progress = 0
                self.done = True
                on_boss = False
                self.next_state = "GAMEPLAY"
            if event.key == pygame.K_QUOTE:
                self.level_progress = 99
                self.wave_progress = 99

    def update(self, dt):
        self.health_bars.update()
        self.sprites.update()
        self.pickups.update()
        if pygame.mouse.get_pressed()[0] and self.transition <= 0:
            self.players[0].shoot_()
        for ship in self.ships.sprites():
            ship.shot_sprites.update()
            for pickup in self.pickups.sprites():
                self.pickup_collision(ship, pickup)
            for human in self.humans:
                self.human_collision(ship, human)
            for pickup in self.temp_pickups:
                pickup.wear(ship)
                pickup.wear(ship)
        for catcher in self.catchers:
            for human in self.humans:
                self.human_collision(catcher, human)
        for enemy in self.enemies.sprites():
            enemy.shot_sprites.update()
            for ship in self.ships.sprites():
                self.enemy_collision(ship, enemy)
                self.shoot_collision(ship, enemy)
                self.shoot_collision(enemy, ship)
        for enemy in self.aim_enemies:
            closest = self.get_closest_to(enemy, self.ships)
            if closest is not None:
                enemy.set_target(pygame.math.Vector2(closest.rect.centerx, closest.rect.centery))

        self.progress_level()
        if len(self.ships) == 0:
            if self.players[0].hp <= 0:
                self.done = True
                pygame.mixer.fadeout(1500)
            else:
                self.died_lol = True
                self.ships.add(self.players[0])
                self.sprites.add(self.players[0])
                self.transition = 1

    def progress_level(self):
        global game_level
        if self.level_timer > 0:
            self.level_timer -= 1
            return
        if self.level_progress >= len(self.level.rounds):
            self.level_progress = 0
            self.wave_progress = 0
            self.temp_pickups.clear()
            self.level.get_level(game_level)
            self.level_timer = 200
            return
        if self.transition == 2:
            current_round = self.level.rounds[self.level_progress]
            self.add_waves(current_round)
            self.transition = 0
        elif self.transition == 1:
            for enemy in self.enemies.sprites():
                enemy.kill()
            for human in self.humans:
                self.human_collect(human)
            self.players[0].rect.x = random.randint(200, 1400)
            self.players[0].rect.y = random.randint(200, 700)
            self.transition = 2
            self.level_timer = 100
        elif len(self.enemies.sprites()) <= len(self.catchers.sprites()):
            self.transition = 1
            self.level_timer = 100
            self.level_progress += 1
            nextLevelSoundEffect.play()

    def add_waves(self, current_round):
        for wave in current_round:
            for i in range(wave.number):
                npc = self.level.make_enemy(wave.enemy)
                if not npc.friend:
                    self.enemies.add(npc)
                else:
                    self.humans.add(npc)
                if npc.aimed:
                    self.aim_enemies.append(npc)
                if npc.catcher:
                    self.catchers.add(npc)
                self.sprites.add(npc)
                self.level_timer = 60 / wave.number

    # Draws Elements
    def draw(self, screen):
        screen.fill(self.background)
        for enemy in self.enemies:
            enemy.shot_sprites.draw(screen)
            if enemy.dead and not enemy.shot_sprites:
                self.enemies.remove(enemy)
                del enemy
        self.sprites.draw(screen)
        self.pickups.draw(screen)
        self.health_bars.draw(screen)
        for ship in self.ships.sprites():
            ship.shot_sprites.draw(screen)

    def shoot_collision(self, ship_one, ship_two):
        global game_level
        if ship_two.dead:
            return
        if len(ship_one.shot_sprites) <= 0:
            return
        close = self.get_closest_to(ship_two, ship_one.shot_sprites)
        if pygame.sprite.collide_mask(close, ship_two):
            ship_two.lose_hp(ship_one.damage)
            explosion = AnimatedSprite(0.5, True, 'Sprites/Boom', 64, 64)
            self.sprites.add(explosion)
            explosion.rect.center = close.rect.midtop
            close.kill()
            del close

    @staticmethod
    def get_closest_to(sprite, group):
        if len(group) == 0:
            return
        close = group.sprites()[0]
        closest = pygame.math.Vector2(close.rect.centerx, close.rect.centery).distance_to(pygame.math.Vector2(
            sprite.rect.centerx, sprite.rect.centery))
        for other in group:
            distance = pygame.math.Vector2(other.rect.centerx, other.rect.centery).distance_to(pygame.math.Vector2(
                sprite.rect.centerx, sprite.rect.centery))
            if distance < closest:
                closest = distance
                close = other
        return close

    def pickup_collision(self, ship, pickup):
        if pygame.sprite.collide_mask(ship, pickup):
            pickup.effect(ship)
            pickup.kill()

    def human_collision(self, ship, human):
        if pygame.sprite.collide_mask(ship, human):
            if not ship.catcher:
                self.human_collect(human)
                humanCollectSoundEffect.play()
            else:
                human.kill()
                humanDeathSoundEffect.play()

    @staticmethod
    def enemy_collision(ship, enemy):
        if pygame.sprite.collide_mask(ship, enemy):
            ship.lose_hp(enemy.damage)
            bossChannel.play(playerDeathSoundEffect)

    def human_collect(self, human):
        if not self.died_lol:
            self.score += 1000 + self.humans_rescued * 1000
            self.humans_rescued += 1
            if self.humans_rescued % 10 == 0:
                self.players[0].hp += 1
        human.kill()
