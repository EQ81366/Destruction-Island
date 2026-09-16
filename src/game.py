def run_game(source: int):
    import pygame, numpy
    from src.functions import __init__, reset
    from src.block import block_group
    from src.player import (
        player_group,
        spawn_players,
    )
    from src.destruction_management.destruction_manager import (
        destruction_group,
        destruction_manager,
    )
    from src.explosion_manager import explosion_group
    from src.constants import (
        font_50,
        GameState,
        DEFAULT_GAME_STATE,
    )
    from src.state_button import state_button_group, StateButton
    from src.button import button_group, settings
    from src.nametag import nametag_group
    from src.screen_shake import shake
    from src.warning import warning
    from src.rubble_manager import rubble_group
    from src.server_script import server
    from src.client_script import client

    pygame.display.init()
    pygame.font.init()

    size = (1280, 720)
    screen = pygame.display.set_mode(size, pygame.SCALED)
    clock = pygame.time.Clock()

    in_game = [GameState.ONE_PLAYER, GameState.TWO_PLAYER]
    current_game_state = DEFAULT_GAME_STATE

    __init__()

    players = 0

    running = True

    destruction_manager.spawn_destruction()
    spawn_cooldown = 120

    # generate_island()
    block_rect_list = numpy.zeros(
        300, pygame.Rect
    )  # change this number for total tiles possible
    player_rect_list: list[pygame.FRect] = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((204, 255, 255))

        if current_game_state in in_game:
            if len(block_group) <= 25:
                reset(True, players=players)

            block_group.update()
            for i, block in enumerate(block_group):
                block.draw(screen)
                block_rect_list[i] = block.rect

            player_group.update(block_rect_list[: len(block_group)])
            player_rect_list.clear()
            for player in player_group:
                player.draw(screen)
                player.movement()
                player_rect_list.append(player.rect)

            destruction_group.update(
                screen, block_rect_list[: len(block_group)], player_rect_list
            )  # pass in all args
            if len(destruction_group) <= 0:
                spawn_cooldown -= 1
                if spawn_cooldown < 0:
                    destruction_manager.spawn_destruction()
                    spawn_cooldown = 60

            explosion_group.update(screen)

            nametag_group.update(player_rect_list, screen)

            rubble_group.update(screen)

            warning.update(screen)

            if settings["screenshake"]:
                shake.update()
            else:
                shake.reset_shake()

        elif current_game_state not in in_game:
            reset()
            button_group.update(screen)
            state_button_group.update(screen)
            current_game_state = StateButton.current_game_state
            if current_game_state in in_game:
                if current_game_state is GameState.ONE_PLAYER:
                    players = 1
                elif current_game_state is GameState.TWO_PLAYER:
                    players = 2
                    settings["screenshake"] = (
                        False  # screenshake is not possible with more than 1 player, as it would be QUITE weird
                    )

                spawn_players(players, settings["nametags"])

            if current_game_state is GameState.MENU:
                text = font_50.render("Destruction Island", True, (255, 0, 0))
                text2 = font_50.render("Destruction Island", True, (0, 0, 0))
                screen.blit(
                    text2,
                    ((screen.get_width() / 2) - (text2.get_width() / 2) - 5, 60),
                )
                screen.blit(
                    text,
                    ((screen.get_width() / 2) - (text.get_width() / 2) + 5, 55),
                )
            elif current_game_state is GameState.COSTUME:
                pass
            elif current_game_state is GameState.SETTINGS:
                pass
            elif current_game_state is GameState.ONLINE:
                if source == 0:
                    running = not server(screen, clock)
                elif source == 1:
                    running = not client(screen, clock)

                if not running:
                    break

                StateButton.current_game_state = GameState.MENU

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# elif source == 1:
#     player_rect_list: list[pygame.FRect] = []

#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         screen.fill((204, 255, 255))

#         if current_game_state in in_game:
#             pass
#         elif current_game_state not in in_game:
#             button_group.update(screen)
#             state_button_group.update(screen)
#             current_game_state = StateButton.current_game_state
#             if current_game_state in in_game:
#                 current_game_state = GameState.MENU

#             if current_game_state is GameState.MENU:
#                 text = font_50.render("Destruction Island", True, (255, 0, 0))
#                 text2 = font_50.render("Destruction Island", True, (0, 0, 0))
#                 screen.blit(
#                     text2,
#                     ((screen.get_width() / 2) - (text2.get_width() / 2) - 5, 60),
#                 )
#                 screen.blit(
#                     text,
#                     ((screen.get_width() / 2) - (text.get_width() / 2) + 5, 55),
#                 )
#             elif current_game_state is GameState.COSTUME:
#                 pass
#             elif current_game_state is GameState.SETTINGS:
#                 pass
#             elif current_game_state is GameState.ONLINE:
#                 running = client(screen, clock)
#                 if not running:
#                     break

#         pygame.display.flip()
#         clock.tick(60)

#     # pygame.quit()
