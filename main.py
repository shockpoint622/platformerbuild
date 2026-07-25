import pygame
import sys
from logger import log_state, log_event

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.dt: float = 0.0
        self.screen = pygame.display.set_mode((640,480))
        pygame.display.set_caption("platformer")

    def run(self):
        def main():
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()



            pygame.display.update()
            self.clock.tick(60)
