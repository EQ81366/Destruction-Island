import pygame, numpy
from copy import deepcopy
from typing import Any, TYPE_CHECKING
from random import randint
from math import atan2, degrees, sin, cos
from src.explosion_manager import explosion_group, Explosions
from src.constants import DestructionImages, SCREEN_BOX
from src.player import player_group


class BunkerMissile(pygame.sprite.Sprite):
    explosion_strength = 220
    tall_box = deepcopy(SCREEN_BOX)
    tall_box.top -= 200
    destruction_value = 1400
    keybind = pygame.K_m

    def __init__(self, *groups: Any):
        super().__init__()

        self.image: pygame.Surface = DestructionImages.BUNKER_MISSILE.value
        self.rect: pygame.FRect = self.image.get_frect(center=(randint(0, 1280), -150))

        self.acceleration = 0.218
        self.speed = 0
        self.direction = 0
        players = list(player_group)
        if len(players) < 2:
            player_one_rect = players[0].rect
            player_two_rect = players[0].rect
        else:
            player_one_rect: pygame.FRect = players[randint(0, len(players)-1)].rect
            player_two_rect: pygame.FRect = players[randint(0, len(players)-1)].rect

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

    def update(self, *args: Any):
        screen: pygame.Surface = args[0]
        block_rects: list[pygame.FRect] = args[1]
        player_rects: list[pygame.FRect] = args[2]

        self.speed += self.acceleration
        movement_x = cos(self.direction) * self.speed
        movement_y = -sin(self.direction) * self.speed

        self.rect.centerx += movement_x
        self.rect.centery += movement_y

        colliding = self.rect.collidelist(block_rects)
        if colliding != -1 or self.rect.collideobjects(player_rects):
            explosion_group.add(Explosions(self.explosion_strength, deepcopy(self.rect)))
            if self.explosion_strength < 100:
                self.kill()
            else:
                self.explosion_strength -= 10

        if not self.tall_box.colliderect(self.rect):
            self.kill()

        image = pygame.transform.rotate(self.image, degrees(self.direction))

        screen.blit(image, self.rect)

        self.speed += 0.1

    def serialize(self):
        return (self.rect.center, self.direction), DestructionImages.BUNKER_MISSILE.name


if TYPE_CHECKING:
    Type = pygame.sprite.Group[BunkerMissile]
else:
    Type = pygame.sprite.Group

bunker_missile_group: Type = pygame.sprite.Group()
