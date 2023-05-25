import pygame
from entity import Entity
from pygame.math import Vector2 as v2

class Monster():
    def get_player_distance_and_direction(self):
        enemy_position = v2(self.rect.center)
        player_position = v2(self.player.rect.center)
        distance = (player_position - enemy_position).magnitude()
        
        if distance != 0:
            direction = (player_position - enemy_position).normalize()
        else: 
            direction = v2()
        
        return (distance, direction)

    def face_player(self):
        distance, direction = self.get_player_distance_and_direction()
        if distance < self.notice_radius:
            if -0.5 < direction.y < 0.5:
                if direction.x < 0: # then player is on the left side
                    self.status = "left_idle"
                elif direction.x > 0: # player is in the right side
                    self.status = "right_idle"
            else:
                if direction.y < 0: # player is on the top
                    self.status = "up_idle"
                elif direction.y > 0: # player to bottom side
                    self.status = "down_idle"
    
    def walk_to_player(self):
        distance, direction = self.get_player_distance_and_direction()
        if self.attack_radius < distance < self.walk_radius:
            self.direction = direction
            self.status = self.status.split("_")[0]
        else:
            self.direction = v2() #Enemy stops if outside of walking_radius

class Coffin(Entity, Monster):
    def __init__(self, init_position, group, path, collision_sprites, player):
        super().__init__(init_position, group, path, collision_sprites)
        
        # Overwrites
        self.speed = 150
        
        # For player interaction
        self.player = player
        self.notice_radius = 550
        self.walk_radius = 400
        self.attack_radius = 60
    
    def attack(self):
        distance = self.get_player_distance_and_direction()[0]
        if distance < self.attack_radius and not self.is_attacking:
            self.is_attacking = True
            self.frame_index = 0 # Attacken Animation fängt hier von vorne an 
            # und soll nicht mitten drin abgespielt werden
        if self.is_attacking:
            self.status = self.status.split("_")[0] + "_attack"
    
    def animate(self, delta_time):
        current_animation = self.animations[self.status]
        self.frame_index += 7 * delta_time
        
        if int(self.frame_index) == 4 and self.is_attacking:
            if self.get_player_distance_and_direction()[0] <= self.attack_radius:
                self.player.take_damage()
        
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.is_attacking:
                self.is_attacking = False
        self.image = current_animation[int(self.frame_index)]

    def update(self, delta_time):
        self.face_player()
        self.walk_to_player()
        self.attack()
        self.move(delta_time)
        self.animate(delta_time)

class Cactus(Entity, Monster):
    def __init__(self, init_position, group, path, collision_sprites, player):
        super().__init__(init_position, group, path, collision_sprites)
        
        # Overwrites
        self.speed = 100
        
        # For player interaction
        self.player = player
        self.notice_radius = 600
        self.walk_radius = 500
        self.attack_radius = 300
        
    def animate(self, delta_time):
        current_animation = self.animations[self.status]
        self.frame_index += 7 * delta_time
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            # if self.is_attacking:
            #     self.is_attacking = False
        self.image = current_animation[int(self.frame_index)]

    def update(self, delta_time):
        self.face_player()
        self.walk_to_player()
        self.move(delta_time)
        self.animate(delta_time)