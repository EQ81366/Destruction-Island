import pygame
from typing import Any, TYPE_CHECKING
from random import randint
from math import pi, dist
from src.block import block_group
from src.player import player_group, client_group


class BlackHole(pygame.sprite.Sprite):
    destruction_value = 1500
    keybind = pygame.K_b
    def __init__(self, *groups: Any):
        super().__init__()

        self.radius = 50

        self.xy = [randint(200, 1080), randint(200, 500)]

        self.timer = 600

    def update(self, *args: Any):
        screen: pygame.Surface = args[0]
        image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        rect = pygame.draw.circle(
            image, (0, 0, 0), (self.radius, self.radius), self.radius
        )
        rect.center = self.xy
        screen.blit(image, rect)  # blits the visible black hole

        center = pygame.Surface(
            (self.radius * 2, self.radius * 2), pygame.SRCALPHA
        )  # center-most part of circle, represents area where blocks get destroyed
        pygame.draw.circle(
            center, (0, 0, 0), (self.radius, self.radius), self.radius / 2
        )
        mask = pygame.mask.from_surface(center)

        bh_mass = pi * (self.radius**2)
        for block in block_group:
            distance = dist(block.rect.center, rect.center)

            dx = block.rect.centerx - rect.centerx
            dy = block.rect.centery - rect.centery

            if distance == 0:
                distance = 0.1

            block.xv += -dx / distance * (bh_mass * 0.000001)
            block.yv += -dy / distance * (bh_mass * 0.000001)

            block_rect = block.rect
            block_mask = pygame.mask.Mask(block_rect.size, fill=True)
            offset_x = block_rect.left - rect.left
            offset_y = block_rect.top - rect.top

            if mask.overlap(block_mask, (offset_x, offset_y)) != None:
                block.kill()
                bh_mass += (block.rect.width * block.rect.height) / 4
                self.radius = (bh_mass / pi) ** (0.5)  # 16000/(pi*(self.radius**2))

        for player in player_group:
            distance = dist(player.rect.center, rect.center)

            dx = player.rect.centerx - rect.centerx
            dy = player.rect.centery - rect.centery

            if distance == 0:
                distance = 0.0001

            player.xv += -dx / distance * (bh_mass * 0.000013)
            player.yv += -dy / distance * (bh_mass * 0.000013)

        for client in client_group:
            distance = dist(client.rect.center, rect.center)

            dx = client.rect.centerx - rect.centerx
            dy = client.rect.centery - rect.centery

            if distance == 0:
                distance = 0.0001

            client.xv += -dx / distance * (bh_mass * 0.000013)
            client.yv += -dy / distance * (bh_mass * 0.000013)

        # self.radius += 10000/(pi*(self.radius**2))
        self.timer -= 1
        if self.timer == 0:
            self.kill()

    def serialize(self):
        return self.radius, (self.xy), (0, 0, 0), (self.radius * 2, self.radius * 2)


if TYPE_CHECKING:
    Type = pygame.sprite.Group[BlackHole]  # type: ignore
else:
    Type = pygame.sprite.Group

black_hole_group: Type = pygame.sprite.Group()  # type: ignore
