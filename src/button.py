import pygame
from typing import Any, TYPE_CHECKING
from src.constants import ButtonTypes, GameState, font_30
from src.state_button import StateButton
from src.stats import stat_manager

class Button(pygame.sprite.Sprite):
    id = 0

    def __init__(self, *groups: Any):
        super().__init__()

        self.id = Button.id
        Button.id += 1

        self.rect: pygame.Rect = pygame.Rect(0, 0, 249, 50)
        settings = stat_manager.get_settings()
        settings = settings if type(settings) is dict else (stat_manager.Settings.DUMMY,)
        self.setting = list(settings)[self.id]
        self.text = font_30.render(
            str(self.setting.name).capitalize(), True, "black"
        ).convert_alpha()
        self.rect.center = groups[0]

        self.type = groups[1]

        self.image: pygame.Surface = pygame.Surface(
            (self.rect.width, self.rect.height), pygame.SRCALPHA
        )

        if self.type is ButtonTypes.BOOL:
            self.pressed = False

    def update(self, screen: pygame.Surface):
        if StateButton.current_game_state is GameState.SETTINGS:
            mouse_xy = pygame.mouse.get_pos()
            mouse_down = pygame.mouse.get_pressed()[0]

            if self.type is ButtonTypes.BOOL:
                clicked = False
                if mouse_down and self.rect.collidepoint(mouse_xy):
                    self.pressed = True
                elif not mouse_down and self.pressed:
                    self.pressed = False
                    clicked = True

                if self.pressed:
                    pygame.draw.rect(
                        self.image,
                        (255, 255, 255, 150),
                        (0, 0, self.rect.width, self.rect.height),
                    )  # main rect
                else:
                    pygame.draw.rect(
                        self.image,
                        (255, 255, 255, 255),
                        (0, 0, self.rect.width, self.rect.height),
                    )  # main rect

                screen.blit(
                    self.image, self.rect.topleft
                )  # blit alpha surface onto main screen
                pygame.draw.rect(screen, "black", self.rect, 5)  # outline
                screen.blit(
                    self.text,
                    (
                        self.rect.centerx - self.text.get_width() / 2,
                        self.rect.centery - self.text.get_height() / 2,
                    ),
                )  # text
                value = font_30.render(str(stat_manager.settings[self.setting]), True, "black")
                screen.blit(
                    value,
                    (
                        self.rect.centerx - value.get_width() / 2,
                        self.rect.centery - value.get_height() / 2 + 50,
                    ),
                )

                if clicked and self.rect.collidepoint(mouse_xy):
                    #stat_manager.settings[self.setting] = not settings[self.setting]
                    stat_manager.change_setting(self.setting, not stat_manager.get_setting(self.setting))

            elif self.type is ButtonTypes.SLIDE:
                pass


if TYPE_CHECKING:
    Type = pygame.sprite.Group[Button]
else:
    Type = pygame.sprite.Group

button_group: Type = pygame.sprite.Group()
