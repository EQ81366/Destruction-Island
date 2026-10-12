import pygame, numpy
from typing import Any, TYPE_CHECKING
from src.nametag import Nametag, nametag_group
from src.screen_shake import shake

player_image = pygame.image.load("src/player_one.png").convert_alpha()


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups: Any):
        super().__init__()

        self.player = groups[0]
        if self.player == 0:
            self.controls = [pygame.K_w, pygame.K_a, pygame.K_d]
        elif self.player == 1:
            self.controls = [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]

        # self.xy: list[float] = [640, 0]

        self.image: pygame.Surface = player_image
        self.rect: pygame.FRect = pygame.FRect(
            640, 0, self.image.get_width(), self.image.get_height()
        )

        self.mass = self.rect.width * self.rect.height

        self.xv = 0
        self.yv = 0

        self.xv_modifier = 0.5

        self.left = False
        self.prev_direction = self.left
        self.flip = False
        self.jump = False
        self.shake: float = 0

    def update(self, block_rects: list[pygame.Rect]):
        self.yv += 0.218
        self.xv *= 0.95

        centerx: list[int] = []
        centery: list[int] = []
        for rect in block_rects:
            centerx += [rect.centerx]
            centery += [rect.centery]

        distance_top = (
            numpy.subtract(centerx, self.rect.centerx) ** 2
            + numpy.subtract(centery, self.rect.top) ** 2
        )
        distance_bottom = (
            numpy.subtract(centerx, self.rect.centerx) ** 2
            + numpy.subtract(centery, self.rect.bottom) ** 2
        )
        distance_left = (
            numpy.subtract(centerx, self.rect.left) ** 2
            + numpy.subtract(centery, self.rect.centery) ** 2
        )
        distance_right = (
            numpy.subtract(centerx, self.rect.right) ** 2
            + numpy.subtract(centery, self.rect.centery) ** 2
        )

        closest_top = numpy.argmin(distance_top)
        closest_bottom = numpy.argmin(distance_bottom)
        closest_left = numpy.argmin(distance_left)
        closest_right = numpy.argmin(distance_right)

        # pygame.draw.rect(screen, "red", block_rects[closest_top])
        # pygame.draw.rect(screen, "red", block_rects[closest_bottom])
        # pygame.draw.rect(screen, "red", block_rects[closest_left])
        # pygame.draw.rect(screen, "red", block_rects[closest_right])

        closest_rect_top: pygame.Rect = block_rects[closest_top]
        closest_rect_bottom: pygame.Rect = block_rects[closest_bottom]
        closest_rect_left: pygame.Rect = block_rects[closest_left]
        closest_rect_right: pygame.Rect = block_rects[closest_right]

        self.jump = False

        if self.rect.colliderect(closest_rect_bottom):
            if (
                self.yv > 0
                and self.rect.bottom < closest_rect_bottom.top + self.yv + 10
            ):
                self.rect.bottom = closest_rect_bottom.top + 1
                self.yv = 0
                self.jump = True

        self.rect.y -= 1
        if self.rect.colliderect(closest_rect_left):
            if self.xv < 0 and self.rect.left > closest_rect_left.right + self.xv - 10:
                self.rect.left = closest_rect_left.right
                self.xv = 0

        if self.rect.colliderect(closest_rect_right):
            if self.xv > 0 and self.rect.right < closest_rect_right.left + self.xv + 10:
                self.rect.right = closest_rect_right.left
                self.xv = 0

        self.rect.y += 1

        if self.rect.colliderect(closest_rect_top):
            if (
                self.yv < 0
                and self.rect.top > closest_rect_top.bottom + self.yv - 10
                # and abs(self.rect.centerx - closest_rect_top.centerx) < 33
            ):
                self.rect.top = closest_rect_top.bottom
                self.yv = 0

        self.rect.x += self.xv
        self.rect.y += self.yv

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

    def movement(self):
        keys_pressed = pygame.key.get_pressed()

        self.prev_direction = self.left

        if keys_pressed[self.controls[0]] and self.jump:
            self.yv -= 5.0
            self.jump = False

        if keys_pressed[self.controls[1]]:
            self.xv -= self.xv_modifier
            self.left = True
        if keys_pressed[self.controls[2]]:
            self.xv += self.xv_modifier
            self.left = False

        self.flip = self.prev_direction != self.left
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

    def movement_with_input(self, left: bool, right: bool, boing: bool):
        self.prev_direction = self.left

        if boing and self.jump:
            self.yv -= 5.0
            self.jump = False
        if left:
            self.xv -= self.xv_modifier
            self.left = True
        if right:
            self.xv += self.xv_modifier
            self.left = False

        self.flip = self.prev_direction != self.left
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

    def check_loss(self):
        if self.rect.y > 720:
            return True

        return False

    def serialize(self):
        shake = self.shake
        self.shake = 0
        return self.rect.topleft, self.flip, shake


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Player]
else:
    Type = pygame.sprite.Group()

player_group: Type = pygame.sprite.Group()
client_group: Type = pygame.sprite.Group()


def spawn_players(amount: int, nametags: bool):
    if nametags:
        for i in range(amount):
            player_group.add(Player(i))
            nametag_group.add(Nametag(i + len(nametag_group)))
    else:
        for i in range(amount):
            player_group.add(Player(i))


def spawn_clients(amount: int, nametags: bool):
    if nametags:
        for i in range(amount):
            client_group.add(Player(i))
            nametag_group.add(Nametag(i + len(nametag_group)))
    else:
        for i in range(amount):
            client_group.add(Player(i))
