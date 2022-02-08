import pygame
from data.constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface((20, 30))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)
        
        self.gravity = 0
        self.movement_value = 4
        self.jump_value = 16
        
        self.movement = [0,0]
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.block_movement = False

        self.collisions_on = {'top': False, 'bottom': False, 'right': False, 'left': False}

    def update_gravity(self):
        self.movement = [0, 0]

        if not self.block_movement:
            if self.moving_right:
                self.movement[0] += self.movement_value
            if self.moving_left:
                self.movement[0] -= self.movement_value
        else:
            if self.moving_right:
                self.movement[0] += 0.1
            if self.moving_left:
                self.movement[0] -= 0.1

        if self.moving_up: self.gravity -= self.jump_value

        self.gravity += 1
        if self.gravity > 15: self.gravity = 15
        self.movement[1] += self.gravity

    def key_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.moving_left = True
        else: self.moving_left = False
        if keys[pygame.K_RIGHT]:
            self.moving_right = True
        else: self.moving_right = False
        if keys[pygame.K_UP] and self.collisions_on['bottom']:
            self.moving_up = True
        else: self.moving_up = False

    # check for any collisions
    def get_collisions(self, tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions

    def move(self, tiles):
        self.collisions_on = {'top': False, 'bottom': False, 'right': False, 'left': False}
        # x axis
        if round(self.movement[0]) != 0: self.rect.x += self.movement[0]
        collisions = self.get_collisions(tiles)
        for tile in collisions:
            if self.movement[0] > 0:
                self.rect.right = tile.left
                self.collisions_on['right'] = True
            elif self.movement[0] < 0:
                self.rect.left = tile.right
                self.collisions_on['left'] = True
        # y axis
        self.rect.y += self.movement[1]
        collisions = self.get_collisions(tiles)
        for tile in collisions:
            if self.movement[1] > 0:
                self.rect.bottom = tile.top
                self.collisions_on['bottom'] = True
            elif self.movement[1] < 0:
                self.rect.top = tile.bottom
                self.collisions_on['top'] = True

        return self.collisions_on

    def update(self, tiles):
        self.key_input()
        if self.collisions_on['bottom'] or self.collisions_on['top']: self.gravity = 0
        self.collisions_on = self.move(tiles)
        self.update_gravity()