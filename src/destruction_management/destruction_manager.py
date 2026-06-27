import pygame
from random import randint
from typing import Any, TYPE_CHECKING
from src.warning import warning
from src.player import player_group, client_group
from src.destruction_management.destruction_constants import Destructions

if TYPE_CHECKING:
    Type = pygame.sprite.Group[Any]
else:
    Type = pygame.sprite.Group()

destruction_group: Type = pygame.sprite.Group()

class DestructionManager(pygame.sprite.Sprite):
    def __init__(self, *groups: Any):
        super().__init__()

        self.destruction = None

    def spawn_destruction(self):
        # 0-6
        destruction = randint(6, 6)

        destruction_list = list(Destructions)

        self.destruction = destruction_list[destruction].value
        warning.new_destruction(destruction_list[destruction])

        number = 1
        if destruction == 0:
            number = randint(3, 6)
        elif destruction == 5:
            number = len(player_group)+len(client_group)

        for i in range(number):
            self.destruction[1].add(self.destruction[0](i)) # type: ignore

        destruction_group.add(self.destruction[1])

    def destroy(self):
        for thing in destruction_group:
            thing.kill()

    def serialize(self) -> list[Any]:
        serialized: list[Any] = []
        for thing in destruction_group:
            serialized.append(thing.serialize())

        return serialized