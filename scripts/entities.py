import pygame
import math
import random
import scripts.tilemap
from scripts.particle import *

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

        self.last_movement = [0,0]

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

        self.last_movement = movement

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
        self.jumps = 1
        self.wall_slide = False
        self.dashing = 0

    def update(self, tilemap, movement=(0,0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1

        self.wall_slide = False
        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:
            self.wall_slide = True
            self.velocity.y = min(self.velocity.y, 0.5)
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide')

        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')

        dash_abs = abs(self.dashing)
        if dash_abs in {60, 50}:
            for i in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                p_velo = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=p_velo, frame=random.randint(0,7)))
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if dash_abs > 50:
            self.velocity.x = dash_abs / self.dashing * 8
            if dash_abs == 51:
                self.velocity.x *= 0.1
            p_velo = [dash_abs / self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=p_velo, frame=random.randint(0,7)))


        if self.velocity.x > 0:
            self.velocity.x = max(self.velocity.x -0.1, 0)
        else:
            self.velocity.x = min(self.velocity.x + 0.1, 0)

    def render(self, surf, offset=(0,0)):
        if abs(self.dashing) <= 50:
            super().render(surf, offset=offset)


    def jump(self):
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity.x = 3.5
                self.velocity.y = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity.x = -3.5
                self.velocity.y = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
        elif self.jumps:
            self.velocity.y = -3
            self.jumps -= 1
            self.air_time = 5
            return True

    def dash(self):
        if not self.dashing:
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60
