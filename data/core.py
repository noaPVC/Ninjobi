from data.constants import *
import pygame
import json
import os

# basically all needed funcs like assets loaders, animation helpers, etc.

# pass path of directory, and returns a dict of images
def asset_loader(path):
    dict_of_assets = {}
    for _,__,img_paths in os.walk(path):
        for img in img_paths:
            pygame_image = pygame.image.load(path + '/' + img).convert_alpha()
            dict_of_assets[img.split('.')[0]] = pygame.transform.scale(pygame_image, (tile_size, tile_size))
    return dict_of_assets

# main builder tile world
def build_world(map, screen, scroll):
    tile_dict = asset_loader('data/assets/tiles')
    tile_rects_list = []
    for y_index, row in enumerate(map):
        for x_index, tile in enumerate(row):
            x = x_index * tile_size - int(scroll[0])
            y = y_index * tile_size - int(scroll[1])
            if tile != '0' and tile != '20':
                if tile == '1': screen.blit(tile_dict['empty_tile'], (x, y))
                elif tile == '2': screen.blit(tile_dict['middle_tile'], (x, y))
                elif tile == '3': screen.blit(tile_dict['platform_tile'], (x, y))
                elif tile == '4': screen.blit(tile_dict['platform_left_corner'], (x, y))
                elif tile == '5': screen.blit(tile_dict['platform_right_corner'], (x, y))
                elif tile == '6': screen.blit(tile_dict['single_tile'], (x, y))
                tile_rects_list.append(pygame.Rect(x, y, tile_size, tile_size))
            elif tile == '20': screen.blit(tile_dict['grass'], (x, y))

    return tile_rects_list