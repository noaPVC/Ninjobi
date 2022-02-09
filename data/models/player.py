import pygame
from data.constants import *
from data.core import animation_asset_loader, asset_loader

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animation_sprites = animation_asset_loader('data/assets/characters/ninja')

        self.animation_frame_index = 0
        self.image = self.animation_sprites['idle'][self.animation_frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        self.gravity = 0
        self.movement_value = 5
        self.jump_value = 20
        
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
        if self.gravity > 23: self.gravity = 23
        self.movement[1] += self.gravity

    pygame.USEREVENT + 1

    def perform_animation(self, type):
        if self.animation_frame_index < len(self.animation_sprites[type]):
            self.image = self.animation_sprites[type][int(self.animation_frame_index)]
            self.animation_frame_index += 0.15
        else: self.animation_frame_index = 0        

    def key_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]: self.moving_left = True
        else: self.moving_left = False
        if keys[pygame.K_RIGHT]: self.moving_right = True
        else: self.moving_right = False
        if keys[pygame.K_UP] and self.collisions_on['bottom']: self.moving_up = True
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
        self.perform_animation('idle')
        self.update_gravity()