import pygame
from typing import Any, TYPE_CHECKING
from src.constants import DestructionImages
from src.block import block_group


class Laser(pygame.sprite.Sprite):
    destruction_value = 500
    keybind = pygame.K_SEMICOLON
    def __init__(self, *groups: Any):
        super().__init__()

        self.target: int = groups[0]

        self.image: pygame.Surface = pygame.Surface((65, 1000), pygame.SRCALPHA)
        self.warning_image = DestructionImages.LASER.value

        self.color = (255, 0, 0, 255)

        self.xy = [0, 20]

        self.timer = 300

    def update(self, *args: Any):
        screen: pygame.Surface = args[0]
        player_rects: list[pygame.Rect] = args[2]

        if self.timer >= 60:
            if self.timer >= 80:
                self.xy[0] = player_rects[self.target].centerx
            screen.blit(
                self.warning_image,
                (self.xy[0] - self.warning_image.get_width() / 2, self.xy[1]),
            )
        elif self.timer < 60 and self.timer >= 0:
            self.color = (255, 0, 0, 255 - int((59 - self.timer) * 4.3220339))
            self.image.fill(self.color)
            screen.blit(self.image, (self.xy[0] - int(self.image.get_width() / 2), 0))
        else:
            self.kill()

        if self.timer == 59:
            # block_rects: list[pygame.Rect] = args[1]
            rect = self.image.get_rect(
                topleft=(self.xy[0] - int(self.image.get_width() / 2), 0)
            )

            for block in block_group:
                if block.rect.colliderect(rect):
                    block.kill()

        self.timer -= 1

    def serialize(self):
        if self.timer >= 60:
            return (
                (self.xy[0], self.xy[1] + self.warning_image.get_height() / 2)
            ), DestructionImages.LASER.name
        else:
            return (
                (
                    (
                        self.xy[0] + self.image.get_width() / 2,
                        self.image.get_height() / 2,
                    ),
                    (-int(self.image.get_width() / 2), 0),
                ),
                self.color,
                self.image.get_size(),
            )


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Laser]  # type: ignore
else:
    Type = pygame.sprite.Group

laser_group: Type = pygame.sprite.Group()  # type: ignore
