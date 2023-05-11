import pygame
from entity import Entity

class Coffin(Entity):
    def __init__(self, init_position, group, path, collision_sprites):
        super().__init__(init_position, group, path, collision_sprites)

class Cactus(Entity):
    def __init__(self, init_position, group, path, collision_sprites):
        super().__init__(init_position, group, path, collision_sprites)