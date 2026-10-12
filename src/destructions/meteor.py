import pygame
from typing import TYPE_CHECKING, Any
from random import randint
from math import atan2, cos, sin
from src.constants import DestructionImages
from src.block import block_group
from src.screen_shake import shake
from src.explosion_manager import explosion_group, Explosions


class Meteor(pygame.sprite.Sprite):
    destruction_value = 1000
    keybind = pygame.K_i
    def __init__(self, *groups: Any):
        super().__init__()

        if randint(0, 1) == 0:
            xy: list[float] = [randint(-100, 50), -200]
        else:
            xy: list[float] = [randint(1230, 1380), -200]

        self.xv = 0
        self.yv = 0

        self.image: pygame.Surface = pygame.transform.rotate(
            DestructionImages.METEOR.value, randint(1, 360)
        )
        self.rect: pygame.FRect = self.image.get_frect(center=xy)

        self.angle = atan2(
            -((360 + randint(-80, 80)) - xy[1]),
            ((640 + randint(-200, 200)) - xy[0]),
        )  # direction of movement
        self.increment = [cos(self.angle) / 2, -sin(self.angle) / 2]

        self.falling = 40

    def update(self, *args: Any):
        screen: pygame.Surface = args[0]

        if self.falling > 0:
            self.xv += self.increment[0]
            self.yv += self.increment[1]

            self.rect.centerx += self.xv
            self.rect.centery += self.yv
        else:
            if self.falling <= -60:
                self.kill()
            self.falling -= 1

        screen.blit(self.image, self.rect)

        mask = pygame.mask.from_surface(pygame.transform.scale(self.image, (250, 250)))

        for block in block_group:
            block_mask = pygame.mask.Mask(block.rect.size, fill=True)
            offset_x = block.rect.left - self.rect.left
            offset_y = block.rect.top - self.rect.top
            if mask.overlap(block_mask, (offset_x, offset_y)) != None:
                block.kill()
                self.falling -= 1
                explosion_group.add(Explosions(50, self.rect))
                shake.add_shake(25)

        if self.rect.top > 720:  # if it goes below the map
            self.kill()

    def serialize(self):
        return (self.rect.center, self.angle), DestructionImages.METEOR.name


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Meteor]
else:
    Type = pygame.sprite.Group

meteor_group: Type = pygame.sprite.Group()
