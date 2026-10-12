import pygame, numpy
from typing import Any, TYPE_CHECKING
from random import randint
from math import atan2, degrees, sin, cos
from src.explosion_manager import explosion_group, Explosions
from src.constants import DestructionImages


class Missile(pygame.sprite.Sprite):
    explosion_strength = 170
    destruction_value = 150
    keybind = pygame.K_o

    def __init__(self, *groups: Any):
        super().__init__()

        self.image: pygame.Surface = DestructionImages.MISSILE.value
        self.rect: pygame.FRect = self.image.get_frect(center=(randint(0, 1280), -150))

        self.speed = 3
        self.direction = 0

        # self.explosion_strength = 170

    def update(self, *args: Any):
        screen: pygame.Surface = args[0]
        block_rects: numpy.ndarray = args[1]
        player_rects: list[pygame.Rect] = args[2]
        player_one_rect: pygame.Rect = player_rects[0]
        if len(player_rects) > 1:
            player_two_rect: pygame.Rect = player_rects[1]

            rect_x = self.rect.centerx
            rect_y = self.rect.centery
            delta_x = [
                player_one_rect.centerx - rect_x,
                player_two_rect.centerx - rect_x,
            ]
            delta_y = [
                player_one_rect.centery - rect_y,
                player_two_rect.centery - rect_y,
            ]

            distances = [
                delta_x[0] ** 2 + delta_y[0] ** 2,
                delta_x[1] ** 2 + delta_y[1] ** 2,
            ]
            if distances[0] <= distances[1]:
                self.direction = atan2(-delta_y[0], delta_x[0])
            else:
                self.direction = atan2(-delta_y[1], delta_x[1])

        else:
            delta_x = player_one_rect.centerx - self.rect.centerx
            delta_y = player_one_rect.centery - self.rect.centery
            self.direction = atan2(-delta_y, delta_x)

        movement_x = cos(self.direction) * self.speed
        movement_y = -sin(self.direction) * self.speed

        self.rect.centerx += movement_x
        self.rect.centery += movement_y

        colliding = self.rect.collidelist(block_rects)  # type: ignore
        if colliding != -1 or self.rect.collideobjects(player_rects):
            explosion_group.add(Explosions(self.explosion_strength, self.rect))
            self.kill()

        image = pygame.transform.rotate(self.image, degrees(self.direction))

        screen.blit(image, self.rect)

        self.speed += 0.1

    def serialize(self):
        return (self.rect.center, self.direction), DestructionImages.MISSILE.name


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Missile]
else:
    Type = pygame.sprite.Group

missile_group: Type = pygame.sprite.Group()
