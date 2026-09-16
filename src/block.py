import pygame
from random import randint
from typing import Any, TYPE_CHECKING
from src.constants import Blocks, Rubble
from src.screen_shake import shake
from src.rubble_manager import spawn_rubble
from src.button import settings


class Block(pygame.sprite.Sprite):
    def __init__(self, *groups: Any):
        super().__init__()

        self.type: Blocks = groups[0]
        self.image: pygame.Surface = self.type.value[0]
        self.hardness = self.type.value[1]

        # self.xy: list[float] = groups[1]

        self.rect: pygame.FRect = pygame.FRect(
            groups[1], (self.image.get_width(), self.image.get_height())
        )

        self.xv: float = 0
        self.yv: float = 0

    def destroy(
        self, explosion_strength: float, explosion: float, vector: pygame.Vector2
    ):
        if explosion_strength >= self.hardness:
            self.kill()
            if settings["rubble"]:
                vector = pygame.math.Vector2.normalize(vector)
                x_explosion = vector.x * explosion * 2
                y_explosion = vector.y * explosion * 1.5
                spawn_rubble(
                    Rubble[self.type.name], self.rect.topleft, x_explosion, y_explosion
                )

    def update(self):
        self.xv *= 0.95
        self.yv *= 0.95
        self.rect.left += self.xv
        self.rect.top += self.yv
        # self.rect.topleft = (int(self.xy[0]), int(self.xy[1]))

    def draw(self, screen: pygame.Surface):
        shake_values = shake.get_shake()
        screen.blit(
            self.image,
            (
                self.rect.left + shake_values[0],
                self.rect.top + shake_values[1],
                self.rect.width,
                self.rect.height,
            ),
        )

    def serialize(self) -> dict[str, str | tuple[float, float]]:
        return {"img": self.type.name, "xy": self.rect.topleft}


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Block]
else:
    Type = pygame.sprite.Group()

block_group: Type = pygame.sprite.Group()


def generate_column(starting_height: int, starting_x: int):
    column_height = randint(6, 8)

    dirt_height = 3
    stone_height = column_height - dirt_height

    block_group.add(Block(Blocks.GRASS, [starting_x, starting_height]))
    for i in range(dirt_height):
        block_group.add(
            Block(Blocks.DIRT, [starting_x, starting_height + 40 * (i + 1)])
        )
        column_height -= 1

    additional_height = 40 * dirt_height

    for i in range(stone_height):
        block_group.add(
            Block(
                Blocks.STONE,
                [starting_x, starting_height + additional_height + 40 * (i + 1)],
            )
        )


def generate_island():
    starting_height = 40 * randint(4, 7)
    starting_x = 40
    for i in range(30):  # type: ignore
        generate_column(starting_height, starting_x)

        weighted = min(round(abs(360 - starting_height) / 20), 10)
        if randint(1, 10) >= weighted:
            starting_height -= 40
        else:
            starting_height += 40
        starting_x += 40
