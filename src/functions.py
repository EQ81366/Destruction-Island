from src.state_button import state_button_group, StateButton, StateButtons
from src.button import button_group, ButtonTypes, Button
from src.destruction_management.destruction_manager import destruction_manager
from src.block import block_group, generate_island
from src.player import player_group, client_group, spawn_players, spawn_clients
from src.nametag import nametag_group
from src.rubble_manager import rubble_group
from src.nametag import Nametag
from src.button import settings
from src.screen_shake import shake


def __init__():
    index = 0
    for a in range(2):
        for b in range(2):
            state_button_group.add(
                StateButton(
                    (640 + 300 * (a - 0.5), 250 + 140 * b),
                    StateButtons(index + 1),
                    (153, 255, 187),
                )
            )
            index += 1
    state_button_group.add(
        StateButton((640, 530), StateButtons(index + 1), (255, 0, 0))
    )
    state_button_group.add(
        StateButton((150, 650), StateButtons(index + 2), (150, 100, 100))
    )

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
        spawn_players(players, settings["nametags"])
        spawn_clients(clients, settings["nametags"])
        generate_island()
