import pygame
from typing import Any, TYPE_CHECKING
from random import randint
from copy import deepcopy
from math import sin, cos, radians
from src.constants import DestructionImages, Blocks
from src.block import block_group

class Thunderstorm(pygame.sprite.Sprite):
    destruction_value = 2000
    keybind = pygame.K_t
    def __init__(self, *groups: Any):
        super().__init__()

        # cloud[0], wind[1], wooteer[2]
        self.images: tuple[pygame.Surface, ...] = DestructionImages.THUNDERCLOUD.value, DestructionImages.WIND.value, DestructionImages.WATER.value
        self.rects: list[pygame.FRect] = [
            image.get_frect() for image in self.images
        ]

        self.modules: pygame.sprite.Group[Wind|Water|Lightning] = pygame.sprite.Group()

        self.count = 600

        image = self.images[0]
        self.xy = (640-image.get_width()/2, -170)

    def update(self, *args: Any):
        screen: pygame.Surface = args[0]


        if randint(1, 11) == 1:
            self.modules.add(Wind())
        if randint(1, 8) == 1:
            self.modules.add(Water())
        if randint(1, 100) == 1:
            self.modules.add(Lightning())
        self.modules.update(args)

        screen.blit(self.images[0], self.xy)

        self.count -= 1
        if self.count < 1:
            self.kill()

    def serialize(self):
        return (self.xy), DestructionImages.THUNDERCLOUD.name


class Wind(Thunderstorm):
    def __init__(self, *groups: Any):
        super().__init__(groups)

        self.rect: pygame.FRect = self.rects[1]

        self.rect.center = (-50 if randint(0, 1)==0 else 1330, randint(30, 690))

        self.xv = -10 if self.rect.centerx > 0 else 10
        self.image: pygame.Surface = self.images[1] if self.rect.centerx < 0 else pygame.transform.flip(self.images[1], True, False)

    def update(self, *args: Any):
        args = args[0]
        screen: pygame.Surface = args[0]
        block_rects: list[pygame.FRect] = args[1]
        player_rects: list[pygame.FRect] = args[2]

        self.rect.centerx += self.xv

        blocks_colliding = self.rect.collidelistall(block_rects)
        for block_index in blocks_colliding:
            block_rects[block_index].centerx += self.xv/2

        players_colliding = self.rect.collidelistall(player_rects)
        for player_index in players_colliding:
            player_rects[player_index].centerx += self.xv

        screen.blit(self.image, self.rect)

    def serialize(self): # type: ignore
        return (self.rect.center), DestructionImages.WIND.name


class Water(Thunderstorm):
    def __init__(self, *groups: Any):
        super().__init__(groups)

        self.rect: pygame.FRect = self.rects[2]

        self.rect.center = (randint(20, 1260), randint(-30, 50))

        self.yv = 10
        self.acceleration = 0.218
        self.image: pygame.Surface = self.images[2]

    def update(self, *args: Any):
        args = args[0]
        screen: pygame.Surface = args[0]
        block_rects: list[pygame.FRect] = args[1]

        self.yv += self.acceleration
        self.rect.centery += self.yv

        blocks_colliding = self.rect.collidelistall(block_rects)
        blocks = block_group.sprites()
        for block_index in blocks_colliding:
            if blocks[block_index].type is not Blocks.MUD:
                blocks[block_index].change_block_type(Blocks.MUD)
                blocks[block_index].image = pygame.transform.scale_by(blocks[block_index].image, 0.8)
                self.kill()
                break

        screen.blit(self.image, self.rect)

    def serialize(self): # type: ignore
        return (self.rect.center), DestructionImages.WATER.name


class Lightning(Thunderstorm):
    def __init__(self, *groups: Any):
        super().__init__(groups)

        self.color = "white"
        self.image: pygame.Surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        x = randint(50, 1230)
        y = 30
        rect = pygame.FRect(0, 0, 10, 120)
        rect.topleft = (x, y)
        branch: pygame.Surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        branch.fill(self.color)

        self.branches: dict[int, pygame.Surface] = {}
        self.branches[0] = branch
        self.branches_constant: dict[int, tuple[pygame.FRect, pygame.FRect, tuple[float, float], int]] = {}
        self.branches_constant[0] = (rect, rect, (0, rect.height/2), 0)

        self.tick = 0

        self.make_lightning()

        self.rect = pygame.Rect(0, 0, 1280, 720)

    def make_branch(self, prev_rect: pygame.FRect, prev_rrect: pygame.FRect, color: str|tuple[int, int, int], left: bool, offset: tuple[float, float], smaller: bool=False):
        prev_rect = deepcopy(prev_rect)
        prev_rect.width -= 2*smaller
        prev_rect.height -= 2*smaller
        center: list[float] = [prev_rrect.centerx, prev_rrect.centery]
        center[0] += offset[0]
        center[1] += offset[1]
        rect = pygame.FRect(0, 0, prev_rect.width, prev_rect.height)

        branch = pygame.Surface(rect.size, pygame.SRCALPHA)
        branch.fill(color)

        angle: int
        if left:
            angle = randint(-60, -10)
        else:
            angle = randint(10, 60)

        rotated_branch = pygame.transform.rotate(branch, angle)
        rotated_rect = rotated_branch.get_frect(centerx=center[0], centery=center[1])

        height = prev_rect.height
        offset_xy = (
            int(sin(radians(angle)) * (height/2)),
            int(cos(radians(angle)) * (height/2)),
        )

        rotated_rect.x += offset_xy[0]
        rotated_rect.y += offset_xy[1]

        rect.centerx = center[0]
        rect.top = center[1]

        return rotated_rect, rotated_branch, rect, offset_xy, angle

    def create_generation(self, gen: int):
        idxs: list[int] = [
            (2**(gen-1))+i-1 for i in range(2**(gen-1))
        ]
        total_i: int = idxs[-1]+1
        for idx in idxs: # to make pairs of forks for each thing of image
            for i in range(2): # makes 2 forks from 1 thing of image
                rrect, branch, rect, offset, angle = self.make_branch(self.branches_constant[idx][1], self.branches_constant[idx][0], self.color, bool(True*i), self.branches_constant[idx][2], smaller=True)
                self.branches[total_i] = branch
                self.branches_constant[total_i] = (rrect, rect, offset, angle)
                total_i += 1

    def make_lightning(self):
        for i in range(4):
            self.create_generation(i+1)

        for part in self.branches:
            surface = self.branches[part]
            rrect = self.branches_constant[part][0]
            self.image.blit(surface, rrect)

        self.tick = 3

    def update(self, *args: Any):
        args = args[0]
        screen: pygame.Surface = args[0]

        screen.blit(self.image)
        if self.tick > 2:
            screen.fill("white")
        elif self.tick == 2:
            pygame.sprite.spritecollide(self, block_group, True, pygame.sprite.collide_mask) # type: ignore
        elif self.tick == 0:
            self.kill()

        self.tick -= 1

    def serialize(self): # type: ignore
        return (0, 0), self.branches_constant

if TYPE_CHECKING:
    Type = pygame.sprite.Group[Thunderstorm]
else:
    Type = pygame.sprite.Group

thunderstorm_group: Type = pygame.sprite.Group()