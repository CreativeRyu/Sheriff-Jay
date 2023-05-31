import pygame
from pygame.math import Vector2 as v2

class SpriteObject(pygame.sprite.Sprite):
    def __init__(self, position, surface, group):
        super().__init__(group)
        self.image = surface
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0, -self.rect.height / 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction, surface, group):
        super().__init__(group)
        self.image = surface
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = position)
        
        # float based movement
        self.position = v2(self.rect.center)
        self.direction = direction
        self.speed = 400
        
    def update(self, delta_time):
        self.position += self.direction * self.speed * delta_time
        self.rect.center = (round(self.position.x), round(self.position.y))
