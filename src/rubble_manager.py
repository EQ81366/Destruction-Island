import pygame
from typing import TYPE_CHECKING, Any
from random import randint
from src.constants import Rubble


class Rubbles(pygame.sprite.Sprite):
    def __init__(self, *groups: Any):
        super().__init__()

        self.type: Rubble = groups[0]

        self.image: pygame.Surface = self.type.value
        self.rect: pygame.FRect = self.image.get_frect(center=groups[1])

        self.xv = groups[2] / 1
        self.yv = groups[3] / 1

        self.lifespan = 300

    def update(self, screen: pygame.Surface):
        self.rect.centerx += self.xv
        self.rect.centery += self.yv

        self.xv *= 0.98
        self.yv += 0.218

        if self.lifespan <= 0:
            self.kill()

        screen.blit(self.image, self.rect)

        self.lifespan -= 1


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Rubbles]
else:
    Type = pygame.sprite.Group

rubble_group: Type = pygame.sprite.Group()


def spawn_rubble(
    type: Rubble, xy: tuple[float, float], explosion_x: float, explosion_y: float
):
    for i in range(randint(2, 5)):
        rubble_group.add(
            Rubbles(
                type,
                [xy[0] + randint(-20, 20), xy[1] + randint(-20, 20)],
                explosion_x,
                explosion_y,
            )
        )
