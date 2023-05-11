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
        
        self.init_level()
        
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
                    group = self.all_sprites,
                    path = gs.PATHS["coffin"],
                    collision_sprites = self.obstacles
                )
            
            if entity.name == "Cactus":
                Cactus(
                    init_position = (entity.x, entity.y),
                    group = self.all_sprites,
                    path = gs.PATHS["cactus"],
                    collision_sprites = self.obstacles
                )
        
    def create_bullet(self, position, direction):
        Bullet(position, direction, self.bullet_surface, [self.all_sprites, self.bullets])
        
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
            
            # draw Groups
            self.game_display.fill("White")
            self.all_sprites.custom_draw(self.player)
            
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.execute_gameloop()