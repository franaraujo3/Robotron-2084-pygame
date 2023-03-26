import pygame

pygame.font.init()
pygame.mixer.init()
screen_width = 1600
screen_height = 900
clk = pygame.time.Clock()
fps = 60
shot_time = 15

menuMusic = pygame.mixer.Sound("Sounds/MenuMusic.wav")
gameplayMusic = pygame.mixer.Sound("Sounds/gameplayMusic.wav")
gameplayMusic.set_volume(0.3)
gameoverMusic = pygame.mixer.Sound("Sounds/gameover.wav")
gameWinMusic = pygame.mixer.Sound("Sounds/Yippeee.wav")

shotSoundEffect = pygame.mixer.Sound("Sounds/shotBeam.wav")
shotSoundEffect.set_volume(0.15)
explosionSoundEffect = pygame.mixer.Sound("Sounds/explosionSoundEffect.wav")
explosionSoundEffect.set_volume(0.7)

bossWarningChannel = pygame.mixer.Channel(3)
bossChannel = pygame.mixer.Channel(2)