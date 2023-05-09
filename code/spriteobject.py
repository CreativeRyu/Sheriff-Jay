import pygame

class SpriteObject(pygame.sprite.Sprite):
    def __init__(self, position, surface, group):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0, -self.rect.height / 3)
