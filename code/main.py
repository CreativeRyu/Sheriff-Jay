import pygame
import sys
import game_settings as gs
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.game_display = pygame.display.set_mode((gs.WINDOW_WIDTH, gs. WINDOW_HEIGHT))
        pygame.display.set_caption("Sheriff Jay")
        self.game_clock = pygame.time.Clock()
        
        # Groups
        self.all_sprites = pygame.sprite.Group()
        
        self.setup()
        
    def setup(self):
        Player((200, 200), self.all_sprites, None, self.all_sprites)
        
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
            self.all_sprites.draw(self.game_display)
            
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.execute_gameloop()
