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

        self.test_img = pygame.image.load('./data/images/clouds/cloud_1.png')
        self.test_img.set_colorkey((0,0,0))
        self.img_pos = [160, 260]
        self.movement = [False, False, False, False]

    def run(self):
        def main():
            while True:
                log_state()
                self.screen.fill("blue")
                self.img_pos[1] += (self.movement[1] - self.movement[0]) *5
                self.img_pos[0] += (self.movement[3] - self.movement[2]) *5

                self.screen.blit(self.test_img, self.img_pos)

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




                pygame.display.update()
                self.clock.tick(60)

        if __name__ == "__main__":
            main()


        pygame.quit()


Game().run()
