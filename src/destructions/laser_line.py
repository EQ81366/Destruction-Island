import pygame
from typing import Any, TYPE_CHECKING
from math import sin, cos, radians
from random import randint
from src.block import block_group


class LaserLine(pygame.sprite.Sprite):
    destruction_value = 600
    keybind = pygame.K_l
    def __init__(self, *groups: Any):
        super().__init__()

        self.image: pygame.Surface = pygame.Surface((10, 1000), pygame.SRCALPHA)
        self.angle = 0
        self.mod = 5
        self.times = randint(30, 60)
        self.cd = 0
        self.xy = (640, 0)
        self.offset_xy = (640, 0)
        self.color = (200, 0, 0, 200)

    def update(self, *args: Any):
        screen: pygame.Surface = args[0]
        number = randint(1, 20)
        if number == 1 or self.cd > 0:
            self.color = (255, 0, 0, 255)
            pygame.draw.rect(self.image, self.color, self.image.get_rect())
            if number == 1:
                self.times -= 1

            if self.cd == 0:
                self.cd = 60
            else:
                self.cd -= 1

            number = 1
        else:
            self.color = (200, 0, 0, 200)
            pygame.draw.rect(self.image, (200, 0, 0, 200), self.image.get_rect())
            self.angle += self.mod
            if self.angle == 90 or self.angle == 270 or self.angle == -90:
                self.mod *= -1

        rotated = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated.get_rect(center=self.xy)
        self.offset_xy = (
            int(sin(radians(self.angle)) * 500),
            int(cos(radians(self.angle)) * 500),
        )
        rotated_rect.x += self.offset_xy[0]
        rotated_rect.y += self.offset_xy[1]
        screen.blit(rotated, rotated_rect)
        if number == 1 and self.times > 0:
            mask = pygame.mask.from_surface(rotated)
            for block in block_group:
                block_mask = pygame.mask.Mask(block.rect.size, fill=True)
                top_left = rotated_rect.topleft
                top_left_block = block.rect.topleft
                offset_x = top_left_block[0] - top_left[0]
                offset_y = top_left_block[1] - top_left[1]
                if mask.overlap(block_mask, (offset_x, offset_y)) != None:
                    block.kill()

        if self.times == 0:
            self.kill()

    def serialize(self):
        return (self.xy, self.offset_xy, self.angle), self.color, self.image.get_size()


if TYPE_CHECKING:
    Type = pygame.sprite.Group[LaserLine]  # type: ignore
else:
    Type = pygame.sprite.Group

laser_line_group: Type = pygame.sprite.Group()  # type: ignore
