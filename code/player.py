import pygame
from pygame.math import Vector2 as v2
from os import walk

class Player(pygame.sprite.Sprite):
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
        self.speed = 200
        
        # collisions
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)
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

    def set_status(self):
        # Idling
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = self.status.split("_")[0] + "_idle"
        
        # Attacking
        if self.is_attacking:
            self.status = self.status.split("_")[0] + "_attack"

    def handle_input(self):
        
        if not self.is_attacking:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else: 
                self.direction.y = 0
            
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            else: 
                self.direction.x = 0
            
            if keys[pygame.K_SPACE]:
                self.is_attacking = True
                self.direction = v2()
                self.frame_index = 0
            
    def animate(self, delta_time):
        current_animation = self.animations[self.status]
        self.frame_index += 7 * delta_time
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False
        self.image = current_animation[int(self.frame_index)]
        
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
        self.set_status()
        self.move(delta_time)
        self.animate(delta_time)