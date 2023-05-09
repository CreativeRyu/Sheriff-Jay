import pygame
import sys
from allsprites import AllSprites
from spriteobject import SpriteObject
import game_settings as gs
from player import Player
from pytmx.util_pygame import load_pygame

class Game:
    def __init__(self):
        pygame.init()
        self.game_display = pygame.display.set_mode((gs.WINDOW_WIDTH, gs. WINDOW_HEIGHT))
        pygame.display.set_caption("Sheriff Jay")
        self.game_clock = pygame.time.Clock()
        
        # Groups
        self.all_sprites = AllSprites()
        
        self.init_level()
        
    def init_level(self):
        # import tmx data from Tiled
        # Tiles
        tmx_map = load_pygame("data/game_map.tmx")
        for x, y, surface in tmx_map.get_layer_by_name("Zaun_Layer").tiles():
            SpriteObject((x * 64, y * 64), surface, self.all_sprites)
        
        # level objects
        for level_object in tmx_map.get_layer_by_name("level_objects_Layer"):
            SpriteObject((level_object.x, level_object.y),
                            level_object.image, self.all_sprites)
        
        # Entity for Player Spawning
        for entity in tmx_map.get_layer_by_name("Entities_Layer"):
            if entity.name == "Player":
                self.player = Player((entity.x, entity.y), 
                                        self.all_sprites, gs.PATHS["player"], None)
        
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
