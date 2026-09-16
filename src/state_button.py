import pygame
from typing import Any, TYPE_CHECKING
from src.constants import font_30, StateButtons, GameState, DEFAULT_GAME_STATE

back_invalid = [GameState.ONE_PLAYER, GameState.TWO_PLAYER, GameState.MENU]


class StateButton(pygame.sprite.Sprite):
    id = 0
    current_game_state = DEFAULT_GAME_STATE

    def __init__(self, *groups: Any):
        super().__init__()

        self.id = StateButton.id
        StateButton.id += 1

        self.rect: pygame.Rect = pygame.Rect(0, 0, 249, 90)
        self.rect.center = groups[0]

        self.button: StateButtons = groups[1]

        self.text = font_30.render(
            self.button.name.capitalize(), True, "black"
        ).convert_alpha()
        self.color: tuple[int, int, int] = groups[2]
        self.image: pygame.Surface = pygame.Surface((249, 90), pygame.SRCALPHA)

        self.pressed = False

    def update(self, screen: pygame.Surface):
        if (
            self.button is not StateButtons.BACK
            and StateButton.current_game_state in back_invalid
        ) or (
            self.button is StateButtons.BACK
            and StateButton.current_game_state not in back_invalid
        ):
            mouse_xy = pygame.mouse.get_pos()
            mouse_down = pygame.mouse.get_pressed()[0]

            clicked = False

            if mouse_down and self.rect.collidepoint(mouse_xy):
                self.pressed = True
            elif not mouse_down and self.pressed:
                self.pressed = False
                clicked = True

            if clicked and self.rect.collidepoint(mouse_xy):
                if self.button is StateButtons.BACK:
                    StateButton.current_game_state = GameState.MENU
                else:
                    StateButton.current_game_state = GameState(self.button.value)
            elif self.pressed:
                pygame.draw.rect(
                    self.image,
                    (self.color[0], self.color[1], self.color[2], 150),
                    (0, 0, self.rect.width, self.rect.height),
                )  # main rect

            if not self.pressed:
                pygame.draw.rect(
                    self.image,
                    (self.color[0], self.color[1], self.color[2], 255),
                    (0, 0, self.rect.width, self.rect.height),
                )  # main rect

            screen.blit(
                self.image, self.rect.topleft
            )  # blit alpha surface onto main screen
            pygame.draw.rect(screen, "black", self.rect, 10)  # outline
            screen.blit(
                self.text,
                (
                    self.rect.centerx - self.text.get_width() / 2,
                    self.rect.centery - self.text.get_height() / 2,
                ),
            )


if TYPE_CHECKING:
    Type = pygame.sprite.Group[StateButton]
else:
    Type = pygame.sprite.Group

state_button_group: Type = pygame.sprite.Group()
