import pygame
from pygame.math import Vector2 as v2
from entity import Entity

class Player(Entity):
    def __init__(self, init_position, group, path, collision_sprites, create_bullet):
        super().__init__(init_position, group, path, collision_sprites)
        
        self.create_bullet = create_bullet
        self.is_bullet_shot = False

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
                self.is_bullet_shot = False
                
                match self.status.split("_")[0]:
                    case "left": 
                        self.bullet_direction = v2(-1,0)
                    case "right": 
                        self.bullet_direction = v2(1,0)
                    case "up": 
                        self.bullet_direction = v2(0,-1)
                    case "down": 
                        self.bullet_direction = v2(0,1)
    
    def animate(self, delta_time):
        current_animation = self.animations[self.status]
        self.frame_index += 7 * delta_time

        # Bullet wird erst ausgelöst, wenn der dritte Frame der Animation gezeigt wird
        if int(self.frame_index) == 2 and self.is_attacking and not self.is_bullet_shot:
            bullet_start_position = self.rect.center + self.bullet_direction * 75
            self.create_bullet(bullet_start_position, self.bullet_direction)
            self.is_bullet_shot = True
        
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False
        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, delta_time):
        self.handle_input()
        self.set_status()
        self.move(delta_time)
        self.animate(delta_time)
        
        self.blink()
        
        self.invincibility_timer()
        print(self.health)