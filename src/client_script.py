import pygame, socket, json
from typing import Any
from math import degrees
from src.player import player_image
from src.nametag import spawn_nametags, nametag_group
from src.constants import DestructionImages, font_50
from src.screen_shake import shake
from src.block import Blocks
from src.stats import stat_manager


def client(screen: pygame.Surface, clock: pygame.Clock):
    player_rect_list: list[pygame.FRect] = []

    running = True
    quit = False

    flicker = 0

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
        try:
            s.connect((HOST, PORT))
            connected = True
        except:
            pass

        if connected:
            game_over = False
            amount_of_clients, amount_of_players = json.loads(s.recv(1024))

            player_images = {i: player_image for i in range(amount_of_players)}
            client_images = {i: player_image for i in range(amount_of_clients)}
            jumped = False
            move_left = False
            move_right = False
            id = -1

            spawn_nametags(amount_of_clients + 1)

            client_data: tuple[
                list[tuple[tuple[int, int], bool, float]],
                list[tuple[tuple[int, int], bool, float]],
                list[tuple[str, list[float]]],
                list[Any],
                list[tuple[float, tuple[int, int], int]],
            ] = (
                [((0, 0), False, 0)], # host players
                [((0, 0), False, 0)], # client players
                [("", [0, 0])], # blocks
                [], # destructions
                [(0, (0, 0), 0)], # explosion
            )

            while connected:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        connected = False
                        running = False
                        quit = True

                if not game_over:
                    explosion_image = pygame.Surface((1280, 720), pygame.SRCALPHA)

                    keys_pressed = pygame.key.get_pressed()
                    data_to_send = (move_left, move_right, jumped)
                    try:
                        s.sendall(json.dumps(data_to_send).encode())
                    except BrokenPipeError:
                        connected = False
                        running = False
                        break
                    try:
                        client_info: tuple[
                            int,
                            tuple[
                                list[tuple[tuple[int, int], bool, float]],
                                list[tuple[tuple[int, int], bool, float]],
                                list[tuple[str, list[float]]],
                                list[Any],
                                list[tuple[float, tuple[int, int], int]],
                            ],
                            bool,
                        ] = json.loads(s.recv(16384))
                        id = client_info[0]
                        client_data = client_info[1]
                        game_over = client_info[2]
                    except:
                        pass

                    host_player_information = client_data[0]
                    client_information = client_data[1]
                    block_information = client_data[2]
                    destruction_information = client_data[3]
                    explosion_information = client_data[4]

                    self_information = client_information[id]

                    screen.fill((204, 255, 255))

                    shake.add_shake(self_information[2])
                    shake_values = shake.get_shake()

                    for block_data in block_information:
                        image = Blocks[block_data[0]].value[0]
                        xy = block_data[1]
                        if type(xy) is list:
                            screen.blit(
                                image,
                                (
                                    xy[0] + shake_values[0],
                                    xy[1] + shake_values[1],
                                ),
                            )

                    player_rect_list.clear()

                    for i, player_data in enumerate(host_player_information):
                        player_xy = player_data[0]
                        if player_data[1]:
                            player_images[i] = pygame.transform.flip(
                                player_images[i], True, False
                            )

                        screen.blit(
                            player_images[i],
                            (
                                player_xy[0] + shake_values[0],
                                player_xy[1] + shake_values[1],
                            ),
                        )
                        player_rect_list.append(
                            player_images[i].get_frect(topleft=player_xy)
                        )

                    for i, all_client_data in enumerate(client_information):
                        xy = all_client_data[0]
                        if all_client_data[1]:
                            client_images[i] = pygame.transform.flip(
                                client_images[i], True, False
                            )

                        screen.blit(
                            client_images[i],
                            (
                                xy[0] + shake_values[0],
                                xy[1] + shake_values[1],
                            ),
                        )
                        player_rect_list.append(
                            client_images[i].get_frect(topleft=xy)
                        )

                    for destruction in destruction_information:
                        if type(destruction[1]) is str:
                            image = DestructionImages[destruction[1]].value
                            if (
                                type(destruction[0][0]) is float
                                or type(destruction[0][0]) is int
                            ):
                                rect: pygame.Rect = image.get_rect(center=destruction[0])
                            else:
                                rect = image.get_rect(center=destruction[0][0])
                                image = pygame.transform.rotate(
                                    image, degrees(destruction[0][1])
                                )

                            screen.blit(image, rect)

                        elif (
                            type(destruction[0]) is int
                            or type(destruction[0]) is float
                        ):  # for circles
                            image = pygame.Surface(destruction[3], pygame.SRCALPHA)
                            rect = pygame.draw.circle(
                                image,
                                destruction[2],
                                (destruction[0], destruction[0]),
                                destruction[0],
                            )
                            rect.center = destruction[1]
                            screen.blit(image, rect)

                        else:
                            image = pygame.Surface(destruction[2], pygame.SRCALPHA)
                            image.fill(destruction[1])

                            if type(destruction[0][-1]) is int:  # if angle included
                                image = pygame.transform.rotate(
                                    image, destruction[0][-1]
                                )
                                rect = image.get_rect(center=destruction[0][0])
                            elif (
                                type(destruction[0][0]) is list
                            ):  # for cases with xy and offset
                                rect = image.get_rect(center=destruction[0][0])
                            else:  # for all other situations
                                rect = image.get_rect(center=destruction[0])

                            if type(destruction[0][1]) is list:  # for offset values
                                rect.x += destruction[0][1][0]
                                rect.y += destruction[0][1][1]

                            screen.blit(image, rect)  # should always work

                    for explosion in explosion_information:
                        explosion_strength = explosion[0]
                        xy = explosion[1]
                        time = explosion[2]
                        pygame.draw.circle(
                            explosion_image,
                            (
                                255,
                                0,
                                0,
                                255 - int(abs(time) * 4.3220339),
                            ),
                            (explosion_strength, explosion_strength),
                            explosion_strength,
                        )
                        screen.blit(
                            explosion_image,
                            (
                                xy[0] - explosion_strength,
                                xy[1] - explosion_strength,
                            ),
                        )

                    nametag_group.update(player_rect_list, screen)

                    jumped = False
                    move_left = False
                    move_right = False
                    if keys_pressed[pygame.K_w]:
                        jumped = True

                    if keys_pressed[pygame.K_a]:
                        move_left = True

                    if keys_pressed[pygame.K_d]:
                        move_right = True

                    if stat_manager.get_setting(stat_manager.Settings.SCREENSHAKE):
                        shake.update()
                    else:
                        shake.reset_shake()

                elif game_over:
                    try:
                        game_over, host_connected = json.loads(s.recv(1024))
                    except:
                        host_connected = True
                        pass

                    if not host_connected:
                        connected = False
                        break

                    screen.fill((204, 255, 255))

                    text = font_50.render(
                        "Game Over! Wait for host to restart",
                        True,
                        (0, 0, 0),
                    )
                    screen.blit(
                        text,
                        (
                            640 - text.get_width() / 2,
                            330 - text.get_height() / 2,
                        ),
                    )

                    if type(game_over) is not bool:
                        game_over = True

                pygame.display.flip()
                clock.tick(60)

        pygame.display.flip()
        clock.tick(60)

    if quit:
        pygame.quit()
    return quit
