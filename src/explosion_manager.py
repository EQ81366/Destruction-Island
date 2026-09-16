import pygame, numpy
from typing import Any, TYPE_CHECKING
from math import dist
from src.block import block_group
from src.player import player_group, client_group
from src.screen_shake import shake


class Explosions(pygame.sprite.Sprite):
    def __init__(self, *groups: Any):
        super().__init__()

        self.explosion_strength: float = groups[0]
        self.rect: pygame.Rect = groups[1]  # object rect

        self.image: pygame.Surface = pygame.Surface(
            (self.explosion_strength * 2, self.explosion_strength * 2), pygame.SRCALPHA
        ).convert_alpha()  # explosion surface
        self.color = (255, 0, 0, 255)

        self.timer = 0

    def update(self, screen: pygame.Surface):
        if self.timer >= 60:
            self.kill()
        else:
            if self.timer == 0:

                # distances = numpy.sqrt(numpy.subtract(centerx, self.rect.centerx)**2 + numpy.subtract(centery, self.rect.centery)**2)

                # explosion_values = ((-1*(numpy.abs(distances)**(numpy.abs(distances)/self.explosion_strength))) + self.explosion_strength) # use this for less realism, more explosion equality
                # explosion_values = ((-1*self.explosion_strength)*0.5**(-((distances/self.explosion_strength)**2)))+(2*self.explosion_strength) # use this for realism

                for block in block_group:
                    dx = block.rect.centerx - self.rect.centerx
                    dy = block.rect.centery - self.rect.centery
                    vector = pygame.Vector2(dx, dy)

                    distance = dist(block.rect.center, self.rect.center)

                    explosion_value = (
                        (-1 * self.explosion_strength)
                        * 0.5 ** (-((distance / self.explosion_strength) ** 2))
                    ) + (2 * self.explosion_strength)

                    block.destroy(
                        explosion_value,
                        (self.explosion_strength * (0.995**distance)) / 10,
                        vector,
                    )

                for player in player_group:
                    distance_list: list[float] = []
                    # distance_list += [dist(player.rect.center, self.rect.center)]
                    distance_list += [dist(player.rect.bottomleft, self.rect.center)]
                    distance_list += [dist(player.rect.bottomright, self.rect.center)]
                    distance_list += [dist(player.rect.topleft, self.rect.center)]
                    distance_list += [dist(player.rect.topright, self.rect.center)]

                    dx = player.rect.centerx - self.rect.centerx
                    dy = player.rect.centery - self.rect.centery

                    vector = pygame.math.Vector2.normalize(pygame.Vector2(dx, dy))

                    total = 0
                    for distance in distance_list:
                        total += (self.explosion_strength * (0.995**distance)) / 10

                    explosion = total / 5

                    x_explosion = vector.x * explosion * 2
                    y_explosion = vector.y * explosion * 1.5

                    player.xv += x_explosion
                    player.yv += y_explosion

                    shake.add_shake(explosion * 20)

                for client in client_group:
                    distance_list: list[float] = []
                    # distance_list += [dist(player.rect.center, self.rect.center)]
                    distance_list += [dist(client.rect.bottomleft, self.rect.center)]
                    distance_list += [dist(client.rect.bottomright, self.rect.center)]
                    distance_list += [dist(client.rect.topleft, self.rect.center)]
                    distance_list += [dist(client.rect.topright, self.rect.center)]

                    dx = client.rect.centerx - self.rect.centerx
                    dy = client.rect.centery - self.rect.centery

                    vector = pygame.math.Vector2.normalize(pygame.Vector2(dx, dy))

                    total: float = 0
                    for distance in distance_list:
                        total += (self.explosion_strength * (0.995**distance)) / 10

                    explosion = total / 5

                    x_explosion = vector.x * explosion * 2
                    y_explosion = vector.y * explosion * 1.5

                    client.xv += x_explosion
                    client.yv += y_explosion

                    client.shake = explosion * 5

                    # shake.add_shake(explosion*5)

            self.color = (255, 0, 0, 255 - int(abs(self.timer) * 4.3220339))
            pygame.draw.circle(
                self.image,
                self.color,
                (self.explosion_strength, self.explosion_strength),
                self.explosion_strength,
            )
            screen.blit(
                self.image,
                (
                    self.rect.centerx - self.explosion_strength,
                    self.rect.centery - self.explosion_strength,
                ),
            )
            self.timer += 1

    def serialize(self):
        if self.timer >= 60:
            time = 59
        else:
            time = self.timer
        return (self.explosion_strength, self.rect.center, time)


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Explosions]
else:
    Type = pygame.sprite.Group

explosion_group: Type = pygame.sprite.Group()
