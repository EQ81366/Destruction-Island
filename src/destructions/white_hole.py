import pygame
from typing import Any, TYPE_CHECKING
from random import randint
from math import pi, dist
from src.block import block_group
from src.player import player_group, client_group

class WhiteHole(pygame.sprite.Sprite):
    def __init__(self, *groups: Any):
        super().__init__()

        self.radius = 50

        self.xy = [randint(200, 1080), randint(200, 500)]
        self.color = (255, 255, 255)

        self.timer = 600

    def update(self, *args: Any):
        screen: pygame.Surface = args[0]
        image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        rect = pygame.draw.circle(image, self.color, (self.radius, self.radius), self.radius)
        rect.center = self.xy # type: ignore
        screen.blit(image, rect)

        center = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(center, self.color, (self.radius, self.radius), self.radius/2)
        mask = pygame.mask.from_surface(center)
        for block in block_group:
            distance = dist(block.rect.center, rect.center)

            dx = block.rect.centerx-rect.centerx
            dy = block.rect.centery-rect.centery

            if distance == 0:
                distance = 0.1

            bh_mass = (pi*(self.radius**2))

            block.xv -= -dx/distance*(bh_mass*0.000001)
            block.yv -= -dy/distance*(bh_mass*0.000001)

            block_mask = pygame.mask.Mask(block.rect.size, fill=True)
            block_rect = block.rect
            offset_x = block_rect.left-rect.left
            offset_y = block_rect.top-rect.top

            if mask.overlap(block_mask, (offset_x, offset_y)) != None:
                block.kill()
                self.radius += 16000/(pi*(self.radius**2))

        for player in player_group:
            distance = dist(player.rect.center, rect.center)

            dx = player.rect.centerx-rect.centerx
            dy = player.rect.centery-rect.centery

            if distance == 0:
                distance = 0.1
            
            player.xv -= -dx/distance*((pi*(self.radius**2))*0.00001)
            player.yv -= -dy/distance*((pi*(self.radius**2))*0.00001)

        for client in client_group:
            distance = dist(client.rect.center, rect.center)

            dx = client.rect.centerx-rect.centerx
            dy = client.rect.centery-rect.centery

            if distance == 0:
                distance = 0.1
            
            client.xv -= -dx/distance*((pi*(self.radius**2))*0.00001)
            client.yv -= -dy/distance*((pi*(self.radius**2))*0.00001)
        
        #self.radius += 10000/(pi*(self.radius**2))
        self.timer -= 1
        if self.timer == 0:
            self.kill()

    def serialize(self):
        return self.radius, (self.xy), self.color, (self.radius*2, self.radius*2)
    
if TYPE_CHECKING:
    Type = pygame.sprite.Group[WhiteHole] # type: ignore
else:
    Type = pygame.sprite.Group

white_hole_group: Type = pygame.sprite.Group() # type: ignore