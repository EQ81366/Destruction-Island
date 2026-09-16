import pygame, numpy
from random import randint
from typing import Any, TYPE_CHECKING
from src.explosion_manager import explosion_group, Explosions
from src.constants import DestructionImages


class Bomb(pygame.sprite.Sprite):
    explosion_strength = 200

    def __init__(self, *groups: Any):
        super().__init__()

        self.image: pygame.Surface = DestructionImages.BOMB.value

        self.rect: pygame.FRect = pygame.FRect(
            randint(0, 1280), -150, self.image.get_width(), self.image.get_height()
        )

        self.explode = False
        # self.explosion_strength = 200
        self.timer = 180  # frames

        self.xv: float = randint(-3, 3)
        self.yv: float = randint(-2, 2)
        self.yv = 0

    def update(self, *args: Any):
        if self.timer > 0:
            screen: pygame.Surface = args[0]
            block_rects: numpy.ndarray = args[1]
            self.yv += 0.109

            self.explode = False
            for rect in block_rects:
                if self.explode:
                    break
                elif self.rect.colliderect(rect):
                    self.explode = True
                    self.yv = 0
                    self.xv = 0

            self.rect.centerx += self.xv
            self.rect.centery += self.yv

            self.xv *= 0.99

            screen.blit(self.image, self.rect)

            if self.explode:
                self.timer -= 1

        else:
            explosion_group.add(Explosions(self.explosion_strength, self.rect))
            self.kill()

        if self.rect.top > 720:  # if it goes below the map
            self.kill()

    def serialize(self):
        return (self.rect.center), DestructionImages.BOMB.name


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Bomb]
else:
    Type = pygame.sprite.Group()

bomb_group: Type = pygame.sprite.Group()
