import pygame, sys
from data.constants import *
from data.models.level import Level

pygame.init()

pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode(WINDOW)
pygame.key.set_repeat()
clock = pygame.time.Clock()
level = Level(screen, game_map)

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill(BASE_SKY_COLOR_NIGHT)
    level.run()

    pygame.display.update()
    clock.tick(FPS)