import pygame

class Particle:
    def __init__(self, game, p_type, pos, velocity=[0,0], frame=0):
        self.game = game
        self.type = p_type
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(velocity)
        self.animation = self.game.assets['particle/' + p_type].copy()
        self.animation.frame = frame

    def update(self):
        kill = False
        if self.animation.done:
            kill = True

        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y

        self.animation.update()

        return kill

    def render(self, surf, offset=(0.0)):
        img = self.animation.img()
        surf.blit(img, (self.pos.x - offset[0] - img.get_width() // 2, self.pos.y - offset[1] - img.get_height() // 2))
