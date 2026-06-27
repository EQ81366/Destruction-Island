import pygame
from typing import Any, TYPE_CHECKING
from src.constants import font_30

class Nametag(pygame.sprite.Sprite):
    id = 0
    def __init__(self, *groups: Any):
        super().__init__()

        self.nametag: int = Nametag.id
        Nametag.id += 1

        self.xy: list[float] = [0, 30]

        self.image = font_30.render(f"Player {self.nametag}", True, "black").convert_alpha()
        self.rect = self.image.get_rect()
        self.radius = self.image.get_width()/2

    def update(self, player_rect_list: list[pygame.Rect], screen: pygame.Surface):
        self.xy[0] = player_rect_list[self.nametag].centerx - self.radius

        screen.blit(self.image, self.xy)

if TYPE_CHECKING:
    Type = pygame.sprite.Group[Nametag]
else:
    Type = pygame.sprite.Group

nametag_group: Type = pygame.sprite.Group()

def spawn_nametags(amount: int):
    for i in range(amount):
        nametag_group.add(Nametag())