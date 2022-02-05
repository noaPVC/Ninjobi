from distutils.command.build import build
import pygame
from data.constants import *
from data.core import build_world
from data.models.player import Player

class Level:
    def __init__(self, screen, map):
        self.screen = screen
        self.map = map
        self.world_rects = build_world(self.map, self.screen, (0, 0)) # build once
        self.init_player()

        self.scroll_value = [0, 0]

    def init_player(self):
        self.player = pygame.sprite.GroupSingle()
        self.player_obj = Player((WINDOW[0]/2, 420))
        self.player.add(self.player_obj)

    def update_world(self):
        
        if self.player_obj.moving_left and self.player_obj.rect.x <= 150:
            self.player_obj.block_movement = True
            self.scroll_value[0] -= self.player_obj.movement_value
        elif self.player_obj.moving_right and self.player_obj.rect.x >= (WINDOW[0]-150):
            self.player_obj.block_movement = True
            self.scroll_value[0] += self.player_obj.movement_value
        else: 
            self.player_obj.block_movement = False

        if self.player_obj.rect.y <= 150:
            self.scroll_value[1] -= 2
        elif self.player_obj.rect.y >= (WINDOW[1]-150):
            self.scroll_value[1] += 10
        

    def run(self):
        self.player.draw(self.screen)
        self.player.update(self.world_rects)

        self.update_world()
        self.world_rects = build_world(self.map, self.screen, self.scroll_value)