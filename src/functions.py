import os, json, pygame, time
from math import sin, cos, radians
from contextlib import ExitStack
from typing import Any
from src.state_button import state_button_group, StateButton, StateButtons
from src.button import button_group, ButtonTypes, Button
from src.destruction_management.destruction_manager import destruction_manager
from src.block import block_group, generate_island
from src.player import player_group, client_group, spawn_players, spawn_clients
from src.nametag import nametag_group
from src.rubble_manager import rubble_group
from src.nametag import Nametag
from src.stats import stat_manager
from src.screen_shake import shake
from src.constants import font_30


def __init__():
    index = 0
    for a in range(2):
        for b in range(3):
            state_button_group.add(
                StateButton(
                    (640 + 300 * (a - 0.5), 250 + 140 * b),
                    StateButtons(index + 1),
                    (153, 255, 187),
                )
            )
            index += 1
    state_button_group.add(
        StateButton((150, 650), StateButtons(index + 1), (150, 100, 100))
    )
    # state_button_group.add(
        # StateButton((150, 650), StateButtons(index + 2), (150, 100, 100))
    # )

    for i in range(3):
        button_group.add(Button((640, 150 + 140 * i), ButtonTypes.BOOL))


def reset(spawn: bool = False, players: int = 0, clients: int = 0):
    destruction_manager.destroy()
    block_group.empty()
    player_group.empty()
    client_group.empty()
    nametag_group.empty()
    rubble_group.empty()
    shake.reset_shake()
    Nametag.id = 0
    if spawn:
        nametags: bool = bool(stat_manager.get_setting(stat_manager.Settings.NAMETAGS))
        spawn_players(players, nametags=nametags)
        spawn_clients(clients, nametags=nametags)
        generate_island()

def save_game(name: str="detrSave"):
    check_name = name
    tick = 0
    while os.path.exists(f"saves/{check_name}.json"):
        check_name = name
        check_name += f"({tick})"
        tick += 1
    name = check_name

    if os.path.exists(f"saves/{name}.json"):
        print("program selling rn")
    else:
        with open(f"saves/{name}.json", "w", encoding='utf-8') as file:
            stats = stat_manager.get_settings()
            if type(stats) is dict:
                converted = {
                    str(stat.name): stats[stat] for stat in list(stats)
                }
                converted["HIGHSCORE"] = stat_manager.get_highscore()
                json.dump(converted, file, indent=3)

def load_game(screen: pygame.Surface, clock: pygame.Clock):
    running = True

    time.sleep(0.1)
    save_files = os.listdir(f"{str(os.path.abspath("."))}/saves")
    names = [
        font_30.render(name.removesuffix(".json"), True, "black") for name in save_files
    ]
    with ExitStack() as stack:
        opened_files: list[Any] = []
        for path in save_files:
            file = stack.enter_context(open(f"saves/{path}", "r", encoding='utf-8'))
            opened_files.append(file)

        file_settings = [
            json.load(file) for file in opened_files
        ]
        file_settings_text = [
            font_30.render(str(info), True, (50, 50, 50)) for info in file_settings
        ]

        y_scroll = 0
        file_to_load: int = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        y_scroll = max(0, y_scroll-1)
                    elif event.y < 0:
                        y_scroll += 1

            screen.fill("white")

            rect_list: list[pygame.Rect] = []
            for i in range(len(names)):
                rect_list.append(pygame.Rect(90, 40 + i*100 - y_scroll, 1100, 80))
                pygame.draw.rect(screen, (200, 200, 200), rect_list[-1])
                if rect_list[-1].collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    file_to_load = i
                    running = False
                    break

            for i, name in enumerate(names):
                screen.blit(name, (640-name.get_width()/2, 50 + i*100 - y_scroll))
            for i, name in enumerate(file_settings_text):
                screen.blit(name, (640-name.get_width()/2, 85 + i*100 - y_scroll))

            


            pygame.display.flip()
            clock.tick(60)

        print(file_settings[file_to_load])
        for setting in file_settings[file_to_load]:
            try:
                stat_manager.change_setting(stat_manager.Settings[setting], file_settings[file_to_load][setting])
            except:
                stat_manager.change_highscore(file_settings[file_to_load][setting])



def make_branch_from_constant(rect: pygame.FRect, prev_rrect: pygame.FRect, color: str|tuple[int, int, int], offset: tuple[float, float], angle: int):
    center: list[float] = [prev_rrect.centerx, prev_rrect.centery]
    center[0] += offset[0]
    center[1] += offset[1]

    branch = pygame.Surface(rect.size, pygame.SRCALPHA)
    branch.fill(color)

    rotated_branch = pygame.transform.rotate(branch, angle)
    rotated_rect = rotated_branch.get_frect(centerx=center[0], centery=center[1])

    height = rect.height
    offset_xy = (
        int(sin(radians(angle)) * (height/2)),
        int(cos(radians(angle)) * (height/2)),
    )

    rotated_rect.x -= offset_xy[0]
    rotated_rect.y -= offset_xy[1]

    return rotated_branch, rotated_rect

def make_lightning_from_constant(branches_constant: dict[int, tuple[pygame.FRect, pygame.FRect, tuple[float, float], int]], color: str|tuple[int, int, int]):
    image: pygame.Surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
    for i in range(len(branches_constant)):
        branch, rect = make_branch_from_constant(branches_constant[i][1], branches_constant[i][0], color, branches_constant[i][2], branches_constant[i][3])
        image.blit(branch, rect)

    return image