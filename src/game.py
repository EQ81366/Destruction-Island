def run_game(source: int):
    import pygame
    from typing import Any
    from src.functions import __init__, reset, save_game, load_game
    from src.block import block_group
    from src.constants import DestrutionSpawns
    from src.player import (
        player_group,
        spawn_players,
    )
    from src.destruction_management.destruction_manager import (
        destruction_group,
        destruction_manager,
    )
    from src.destruction_management.destruction_constants import Destructions
    from src.explosion_manager import explosion_group
    from src.constants import (
        font_50,
        GameState,
        DEFAULT_GAME_STATE,
    )
    from src.state_button import state_button_group, StateButton
    from src.button import button_group
    from src.nametag import nametag_group
    from src.screen_shake import shake
    from src.warning import warning
    from src.rubble_manager import rubble_group
    from src.server_script import server
    from src.client_script import client
    from src.stats import stat_manager

    pygame.display.init()
    pygame.font.init()

    size = (1280, 720)
    screen = pygame.display.set_mode(size, pygame.SCALED)
    clock = pygame.time.Clock()

    in_game = [GameState.ONE_PLAYER, GameState.TWO_PLAYER, GameState.DESTROYER]
    current_game_state = DEFAULT_GAME_STATE

    __init__()

    players = 0

    running = True
    #save_game()
    #load_game(screen, clock)

    # generate_island()
    block_rect_list: list[Any] = [None] * 50000  # change this number for total tiles possible
    player_rect_list: list[pygame.FRect] = []
    spawn_cooldown = 60

    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((204, 255, 255))

        if current_game_state in in_game:
            if not game_over:
                if stat_manager.accumulate_destruction:
                    print(stat_manager.destruction)
                    stat_manager.destruction += 1
                    stat_manager.destruction_spawn_cd -= 1
                    keys_pressed = pygame.key.get_pressed()
                    destructions = list(DestrutionSpawns)
                    for destruction in destructions:
                        if keys_pressed[destruction.value[0]] and stat_manager.destruction >= destruction.value[1] and stat_manager.destruction_spawn_cd <= 0:
                            destruction_manager.spawn_destruction(destruction_name=destruction.name)
                            stat_manager.destruction -= destruction.value[1]
                            stat_manager.destruction_spawn_cd = 30

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
                    if not game_over:
                        game_over = player.check_loss()

                destruction_group.update(
                    screen, block_rect_list[: len(block_group)], player_rect_list
                )  # pass in all args
                if not stat_manager.accumulate_destruction:
                    if len(destruction_group) <= 0:
                        spawn_cooldown -= 1
                        # if spawn_cooldown < 0:
                        #     destruction_manager.spawn_destruction()

                explosion_group.update(screen)

                nametag_group.update(player_rect_list, screen)

                rubble_group.update(screen)

                warning.update(screen)

                if stat_manager.get_setting(stat_manager.Settings.SCREENSHAKE):
                    shake.update()
                else:
                    shake.reset_shake()

            elif game_over:
                reset()
                screen.fill((204, 255, 255))

                text = font_50.render(
                    "Game Over! Press R to restart", True, (0, 0, 0)
                )
                screen.blit(
                    text,
                    (
                        640 - text.get_width() / 2,
                        330 - text.get_height() / 2,
                    ),
                )

                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_r]:
                    game_over = False
                    reset(True, players=players)

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
                    stat_manager.change_setting(stat_manager.Settings.SCREENSHAKE, False) # screenshake is not possible with more than 1 player, as it would be weird
                elif current_game_state is GameState.DESTROYER:
                    players = 2
                    stat_manager.change_setting(stat_manager.Settings.SCREENSHAKE, False)
                    stat_manager.accumulate_destruction = True

                spawn_players(players, bool(stat_manager.get_setting(stat_manager.Settings.NAMETAGS)))
                spawn_cooldown = 120

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