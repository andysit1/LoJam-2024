from pygame import Vector2
import pygame as pg


class Player(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((30, 30))
        self.image.fill(pg.Color('blue'))

        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.speed = 1

        self.flying : bool = False


    def input(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                self.vel.x = self.speed * 150
            elif event.key == pg.K_a:
                self.vel.x = -self.speed * 150
            elif event.key == pg.K_w:
                self.vel.y = -self.speed * 150
            elif event.key == pg.K_s:
                self.vel.y = self.speed * 150
        elif event.type == pg.KEYUP:
            if event.key == pg.K_d and self.vel.x > 0:
                self.vel.x = 0
            elif event.key == pg.K_a and self.vel.x < 0:
                self.vel.x = 0
            elif event.key == pg.K_w and self.vel.y < 0:
                self.vel.y = 0
            elif event.key == pg.K_s and self.vel.y > 0:
                self.vel.y = 0

    def update(self, delta):
        # Move the player.

        if not self.flying:
            self.pos += self.vel * delta
            self.rect.center = self.pos

