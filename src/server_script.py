import pygame, numpy, socket, json
from typing import Any
from src.destruction_management.destruction_manager import (
    destruction_manager,
    destruction_group,
)
from src.explosion_manager import explosion_group
from src.player import player_group, client_group
from src.functions import reset
from src.constants import font_50
from src.block import block_group
from src.nametag import nametag_group
from src.warning import warning
from src.screen_shake import shake
from src.stats import stat_manager


def server(screen: pygame.Surface, clock: pygame.Clock):
    spawn_cooldown = 120

    block_rect_list = numpy.zeros(
        300, pygame.Rect
    )  # change this number for total tiles possible
    player_rect_list: list[pygame.FRect] = []

    quit = False
    running = True

    flicker = 0
    players = 2 # TODO

    host: str = ""
    port: str = ""

    getting_host = True

    info = ""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit = True
            elif event.type == pygame.KEYDOWN:
                flicker = 0
                if event.key == pygame.K_RETURN:
                    if getting_host:
                        host = info
                        info = ""
                        getting_host = False
                    else:
                        port = info
                        info = ""
                        running = False
                        break
                elif event.key == pygame.K_BACKSPACE:
                    info = info[:-1]
                else:
                    info += pygame.key.name(event.key)

        screen.fill((204, 255, 255))

        text = font_50.render(info, True, "gray")

        screen.blit(text, (640 - text.get_width()/2, 100))

        flicker %= 60
        if flicker < 30:
            pygame.draw.rect(screen, "black", (640 + text.get_width()/2, 100, 5, 50))

        pygame.display.flip()
        clock.tick(60)
        flicker += 1

    if quit:
        pygame.quit()
        return True
        
    if len(host) and len(port) < 2:
        return
    
    HOST = "127.0.0.1" if host == "" else host
    PORT = int(port) if port.strip().isdigit() else 8888


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        connected = False
        s.bind((HOST, PORT))
        s.listen()
        s.setblocking(False)

        keys_pressed = pygame.key.get_pressed()
        clients: dict[int, tuple[socket.socket, tuple[str, int]]] = {}
        waiting = True
        while not keys_pressed[pygame.K_s] and waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    quit = True
                    break

            screen.fill("white")

            keys_pressed = pygame.key.get_pressed()

            try:
                conn, addr = s.accept()
                clients[len(clients)] = (conn, addr)
            except BlockingIOError:
                pass

            pygame.display.flip()
            clock.tick(30)

        if waiting:
            connected = True

        reset(True, players=players, clients=len(clients))

        for i, client in clients.items():
            per_data = json.dumps((len(clients), players)).encode()
            client[0].sendall(per_data)

        data: list[Any] = []

        game_over = False

        while connected:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    connected = False
                    quit = True

            if not game_over:
                if len(block_group) <= 25:
                    reset(True, players=players, clients=len(clients))

                screen.fill((204, 255, 255))

                data.clear()
                for client in clients.values():
                    try:
                        data.append(json.loads(client[0].recv(4096)))
                    except:
                        connected = False
                        break

                if not connected:
                    reset()
                    s.close()
                    break

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
                    # if game_over:
                    #    break

                client_group.update(block_rect_list[: len(block_group)])
                for i, client in enumerate(client_group):
                    current_info = data[i]
                    client.draw(screen)
                    client.movement_with_input(
                        current_info[0],
                        current_info[1],
                        current_info[2],
                    )
                    player_rect_list.append(client.rect)
                    if not game_over:
                        game_over = client.check_loss()
                    # if game_over:
                    #    break

                destruction_group.update(
                    screen,
                    block_rect_list[: len(block_group)],
                    player_rect_list,
                )  # pass in all args
                if len(destruction_group) <= 0:
                    spawn_cooldown -= 1
                    if spawn_cooldown < 0:
                        destruction_manager.spawn_destruction()
                        spawn_cooldown = 60

                data_to_send = (
                    [player.serialize() for player in player_group],
                    [client.serialize() for client in client_group],
                    [block.serialize() for block in block_group],
                    destruction_manager.serialize(),
                    [explosion.serialize() for explosion in explosion_group],
                )

                for i, client in clients.items():
                    per_data = json.dumps((i, data_to_send, game_over)).encode()
                    client[0].sendall(per_data)

                explosion_group.update(screen)

                nametag_group.update(player_rect_list, screen)

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
                    reset(True, players=players, clients=len(clients))

                for client in clients.values():
                    try:
                        client[0].sendall(json.dumps((game_over, connected)).encode())
                    except:
                        connected = False
                        break

            pygame.display.flip()
            clock.tick(60)

    if quit:
        pygame.quit()
    return quit
