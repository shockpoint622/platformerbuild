import pygame
import sys
from logger import log_state, log_event
from scripts.entities import *
from scripts.utils import *
from scripts.tilemap import *

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.dt: float = 0.0
        self.screen = pygame.display.set_mode((640,480))
        pygame.display.set_caption("platformer")

        self.display = pygame.Surface((320, 240))

        self.movement = [False, False, False, False]

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png')
        }

        self.player = PhysicsEntity(self, 'player', (50,50), (8,15))

        self.tilemap = Tilemap(self, tile_size = 16)

    def run(self):
        def main():
            while True:
                log_state()
                self.display.fill((14,219,248))

                self.tilemap.render(self.display)

                self.player.update(((self.movement[3] - self.movement[2]),0))
                self.player.render(self.display)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.movement[0] = True
                        if event.key == pygame.K_DOWN:
                            self.movement[1] = True
                        if event.key == pygame.K_LEFT:
                            self.movement[2] = True
                        if event.key == pygame.K_RIGHT:
                            self.movement[3] = True
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                            self.movement[0] = False
                        if event.key == pygame.K_DOWN:
                            self.movement[1] = False
                        if event.key == pygame.K_LEFT:
                            self.movement[2] = False
                        if event.key == pygame.K_RIGHT:
                            self.movement[3] = False



                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
                pygame.display.update()
                self.clock.tick(60)

        if __name__ == "__main__":
            main()


        pygame.quit()


Game().run()
