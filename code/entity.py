import pygame
from pygame.math import Vector2 as v2
from os import walk

class Entity(pygame.sprite.Sprite):
    def __init__(self, init_position, group, path, collision_sprites):
        super().__init__(group)
        self.import_assets(path)
        self.frame_index = 0
        self.status = "down_idle"
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = init_position)
        
        # float based movement
        self.position = v2(self.rect.center)
        self.direction = v2()
        self.speed = 220
        
        # Collisions
        self.hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height / 2)
        self.collision_sprites = collision_sprites
        
        # Attacking
        self.is_attacking = False
    
    def import_assets(self, path):
        self.animations = {}
        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2], 
                                        key = lambda string: string.split("."[0])):
                    file_path = folder[0].replace("\\", "/") + "/" + file_name
                    image = pygame.image.load(file_path).convert_alpha()
                    # image_size = v2(image.get_size()) * 3
                    # scaled_image = pygame.transform.scale(image, (image_size))
                    key = folder[0].split("\\")[1]
                    self.animations[key].append(image)
    
    def move(self, delta_time):
        # checks if the vector is longer than 0
        # if match, it gets normalized
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.position.x += self.direction.x * self.speed * delta_time
        self.hitbox.centerx = round(self.position.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")
        
        self.position.y += self.direction.y * self.speed * delta_time
        self.hitbox.centery = round(self.position.y)
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

    def collision(self, axis):
        for sprite in self.collision_sprites.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if axis == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.position.x = self.hitbox.centerx
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.position.y = self.hitbox.centery