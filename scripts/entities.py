import pygame
import scripts.tilemap

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = pygame.math.Vector2(pos)
        self.size = pygame.math.Vector2(size)
        self.velocity = pygame.math.Vector2(0,0)
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')

    def rect(self):
        return pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def set_action(self, action: str):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + f"/{self.action}"].copy()




    def update(self, tilemap, movement=(0,0)):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        frame_movement = pygame.math.Vector2(movement[0] + self.velocity.x, movement[1] + self.velocity.y)

        self.pos.x += frame_movement.x
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement.x > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement.x < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos.x = entity_rect.x

        self.pos.y += frame_movement.y
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement.y > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement.y < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos.y = entity_rect.y

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.velocity.y = min(5, self.velocity.y + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity.y = 0

        self.animation.update()

    def render(self, surf, offset=(0,0)):
        #surf.blit(self.game.assets['player'], (self.pos.x - offset[0], self.pos.y - offset[1]))
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
            (self.pos.x - offset[0] + self.anim_offset[0], self.pos.y - offset[1] + self.anim_offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0

    def update(self, tilemap, movement=(0,0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0

        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
