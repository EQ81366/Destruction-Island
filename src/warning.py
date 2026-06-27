import pygame
from typing import Any
from src.constants import font_50
from src.destruction_management.destruction_constants import Destructions

class Warning():
    def __init__(self, *groups: Any):
        super().__init__()

        self.name = pygame.Surface((0, 0))
        self.alpha = 255

    def new_destruction(self, destruction: Destructions):
        self.alpha = 255
        name = [part.capitalize() for part in destruction.name.split("_")]
        full_name = ""
        for part in name:
            full_name += part+" "
        
        self.name = font_50.render(full_name.strip(), True, "black")

    def update(self, screen: pygame.Surface):
        surface = pygame.Surface(self.name.get_size(), pygame.SRCALPHA)
        surface.blit(self.name, (0, 0))
        surface.set_alpha(self.alpha)
        screen.blit(surface, (640-self.name.get_width()/2, 20))
        if self.alpha > 0:
            self.alpha -= 1
        else:
            surface.fill((0, 0, 0, 0))

warning = Warning()
