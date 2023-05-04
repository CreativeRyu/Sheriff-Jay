import pygame
from pygame.math import Vector2 as v2
import game_settings as gs

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = v2()
        self.display_surface = pygame.display.get_surface()
        self.background = pygame.image.load("graphix/other/bg.png").convert()
    
    def custom_draw(self, player):
        # change offset vector
        self.offset.x = player.rect.centerx - gs.WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - gs.WINDOW_HEIGHT / 2
        
        # blit surfaces
        self.display_surface.blit(self.background, - self.offset)

        # sprites inside of the group
        for sprite in self.sprites():
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)