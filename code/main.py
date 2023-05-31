import pygame
import sys
from allsprites import AllSprites
from spriteobject import SpriteObject, Bullet
import game_settings as gs
from player import Player
from pytmx.util_pygame import load_pygame
from enemy import Coffin, Cactus

class Game:
    def __init__(self):
        pygame.init()
        self.game_display = pygame.display.set_mode((gs.WINDOW_WIDTH,
                                                        gs. WINDOW_HEIGHT))
        pygame.display.set_caption("Sheriff Jay")
        self.game_clock = pygame.time.Clock()
        self.bullet_surface = pygame.image.load("graphix/other/particle.png").convert_alpha()
        
        # Groups
        self.all_sprites = AllSprites()
        self.obstacles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        
        # Background Music
        self.bg_music = pygame.mixer.Sound("sound/Tal_Tal_Heights.mp3")
        self.bullet_sfx = pygame.mixer.Sound("sound/bullet.wav")
        
        self.init_level()
        self.bg_music.play(loops = -1)
        
    def init_level(self):
        # import tmx data from Tiled
        # Tiles
        tmx_map = load_pygame("data/game_map.tmx")
        for x, y, surface in tmx_map.get_layer_by_name("Zaun_Layer").tiles():
            SpriteObject((x * 64, y * 64), surface, [self.all_sprites, self.obstacles])
        
        # Level Objects
        for level_object in tmx_map.get_layer_by_name("level_objects_Layer"):
            SpriteObject((level_object.x, level_object.y),
                            level_object.image, [self.all_sprites, self.obstacles])
        
        # Entity for Player Spawning
        for entity in tmx_map.get_layer_by_name("Entities_Layer"):
            if entity.name == "Player":
                self.player = Player(
                    init_position = (entity.x, entity.y),
                    group = self.all_sprites,
                    path = gs.PATHS["player"],
                    collision_sprites = self.obstacles,
                    create_bullet = self.create_bullet
                )
            
            if entity.name == "Coffin":
                Coffin(
                    init_position = (entity.x, entity.y),
                    group = [self.all_sprites, self.monsters],
                    path = gs.PATHS["coffin"],
                    collision_sprites = self.obstacles,
                    player = self.player
                )
            
            if entity.name == "Cactus":
                Cactus(
                    init_position = (entity.x, entity.y),
                    group = [self.all_sprites, self.monsters],
                    path = gs.PATHS["cactus"],
                    collision_sprites = self.obstacles,
                    player = self.player,
                    create_bullet = self.create_bullet
                )
        
    def create_bullet(self, position, direction):
        Bullet(position, direction, self.bullet_surface, [self.all_sprites, self.bullets])
        self.bullet_sfx.play()
    
    def check_bullet_collision(self):
        # Bullet Obstacle Collision
        for obstacle in self.obstacles.sprites():
            pygame.sprite.spritecollide(obstacle, self.bullets, True, pygame.sprite.collide_mask)
        
        # Bullet Monster Collision
        for bullet in self.bullets.sprites():
            sprites =  pygame.sprite.spritecollide(bullet, self.monsters, False, pygame.sprite.collide_mask)
            if sprites:
                bullet.kill()
                for sprite in sprites:
                    sprite.take_damage()
                    
        # Bullet Player Collision
        if pygame.sprite.spritecollide(self.player, self.bullets, True, pygame.sprite.collide_mask):
            self.player.take_damage()
        
    def execute_gameloop(self):
        while True:
            # Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            delta_time = self.game_clock.tick() / 1000
            
            # update Groups
            self.all_sprites.update(delta_time)
            self.check_bullet_collision()
            
            # draw Groups
            self.game_display.fill("White")
            self.all_sprites.custom_draw(self.player)
            
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.execute_gameloop()