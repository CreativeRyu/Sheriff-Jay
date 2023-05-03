import pygame
from pygame.math import Vector2 as v2

class Player(pygame.sprite.Sprite):
    def __init__(self, init_position, group, path, collision_sprites):
        super().__init__(group)
        self.image = pygame.Surface((100, 100))
        self.image.fill("red")
        self.rect = self.image.get_rect(center = init_position)

        # float based movement
        self.position = v2(self.rect.center)
        self.direction = v2()
        self.speed = 200
        
        # collisions
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
        self.collision_sprites = collision_sprites
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else: 
            self.direction.y = 0
        
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else: 
            self.direction.x = 0
    
    def move(self, delta_time):
        # checks if the vector is longer than 0
        # if match, it gets normalized
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.position.x += self.direction.x * self.speed * delta_time
        self.hitbox.centerx = round(self.position.x)
        self.rect.centerx = self.hitbox.centerx
        
        self.position.y += self.direction.y * self.speed * delta_time
        self.hitbox.centery = round(self.position.y)
        self.rect.centery = self.hitbox.centery
    
    def update(self, delta_time):
        self.handle_input()
        self.move(delta_time)