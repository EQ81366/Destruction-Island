def run_game(source: int):
    import pygame, numpy, socket, json
    from math import degrees
    from typing import Any
    from src.block import block_group, generate_island
    from src.player import player_group, spawn_players, player_image, spawn_clients, client_group
    from src.destruction_management.destruction_manager import destruction_group, DestructionManager
    from src.explosion_manager import explosion_group
    from src.constants import font_50, StateButtons, GameState, DEFAULT_GAME_STATE, ButtonTypes, Blocks, DestructionImages
    from src.state_button import state_button_group, StateButton
    from src.button import Button, button_group, settings
    from src.nametag import nametag_group, Nametag, spawn_nametags
    from src.screen_shake import shake
    from src.warning import warning

    pygame.display.init()
    pygame.font.init()

    size = (1280, 720)
    screen = pygame.display.set_mode(size, pygame.SCALED)
    clock = pygame.time.Clock()

    in_game = [GameState.ONE_PLAYER, GameState.TWO_PLAYER]
    current_game_state = DEFAULT_GAME_STATE

    index = 0
    for a in range(2):
        for b in range(2):
            state_button_group.add(StateButton((640+300*(a-0.5), 250+140*b), StateButtons(index+1), (153, 255, 187)))
            index += 1
    state_button_group.add(StateButton((640, 530), StateButtons(index+1), (255, 0, 0)))
    state_button_group.add(StateButton((150, 650), StateButtons(index+2), (150, 100, 100)))

    for i in range(2):
        button_group.add(Button((640, 250+140*i), ButtonTypes.BOOL))

    players = 0
    client = 0

    running = True

    def reset(spawn: bool, clients: int):
        destruction_manager.destroy()
        block_group.empty()
        player_group.empty()
        client_group.empty()
        nametag_group.empty()
        Nametag.id = 0
        if spawn:
            spawn_players(players, settings["nametags"])
            spawn_clients(clients, settings["nametags"])
            generate_island()

    if source == 0:
        destruction_manager = DestructionManager()
        destruction_manager.spawn_destruction()
        spawn_cooldown = 120

        generate_island()
        block_rect_list = numpy.zeros(300, pygame.Rect) # change this number for total tiles possible
        player_rect_list: list[pygame.Rect] = []

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((204, 255, 255))

            if current_game_state in in_game:
                if len(block_group) <= 25:
                    reset(True, 0)

                block_group.update()
                for i, block in enumerate(block_group):
                    block.draw(screen)
                    block_rect_list[i] = block.rect

                player_group.update(block_rect_list[:len(block_group)])
                player_rect_list.clear()
                for player in player_group:
                    player.draw(screen)
                    player.movement()
                    player_rect_list += [player.rect]

                destruction_group.update(screen, block_rect_list[:len(block_group)], player_rect_list) # pass in all args
                if len(destruction_group) <= 0:
                    spawn_cooldown -= 1
                    if spawn_cooldown < 0:
                        destruction_manager.spawn_destruction()
                        spawn_cooldown = 60

                explosion_group.update(block_rect_list[:len(block_group)], screen)

                nametag_group.update(player_rect_list, screen)

                warning.update(screen)

                if settings["screenshake"]:
                    shake.update()
                else:
                    shake.reset_shake()

            elif current_game_state not in in_game:
                reset(False, 0)
                button_group.update(screen)
                state_button_group.update(screen)
                current_game_state = StateButton.current_game_state
                if current_game_state in in_game:
                    if current_game_state is GameState.ONE_PLAYER:
                        players = 1
                    elif current_game_state is GameState.TWO_PLAYER:
                        players = 2
                        settings["screenshake"] = False

                    spawn_players(players, settings["nametags"])

                if current_game_state is GameState.MENU:
                    text = font_50.render("Destruction Island", True, (255, 0, 0))
                    text2 = font_50.render("Destruction Island", True, (0, 0, 0))
                    screen.blit(text2, ((screen.get_width()/2) - (text2.get_width()/2) - 5, 60))
                    screen.blit(text, ((screen.get_width()/2) - (text.get_width()/2) + 5, 55))
                elif current_game_state is GameState.COSTUME:
                    pass
                elif current_game_state is GameState.SETTINGS:
                    pass
                elif current_game_state is GameState.ONLINE:
                    HOST = input("IP: ")
                    PORT = int(input("Port: "))
                    players = 1
                    #HOST = "127.0.0.1"
                    #PORT = 1234
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        connected = False
                        s.bind((HOST, PORT))
                        s.listen()
                        s.setblocking(False)

                        keys_pressed = pygame.key.get_pressed()
                        clients: dict[int, tuple[socket.socket, tuple[str, int]]] = {}
                        while not keys_pressed[pygame.K_s]:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    break
                            keys_pressed = pygame.key.get_pressed()

                            try:
                                conn, addr = s.accept()
                                clients[len(clients)] = (conn, addr)
                            except BlockingIOError:
                                pass

                            clock.tick(30)

                        connected = True

                        spawn_players(1, settings["nametags"])
                        spawn_clients(len(clients), settings["nametags"])

                        for i, client in clients.items():
                            per_data = json.dumps(len(clients)).encode()
                            client[0].sendall(per_data)                       

                        data: list[Any] = []

                        game_over = False

                        while connected:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    connected = False
                                    StateButton.current_game_state = GameState.MENU

                            if not game_over:
                                if len(block_group) <= 25:
                                    reset(True, len(clients))

                                screen.fill((204, 255, 255))

                                data.clear()
                                for client in clients.values():
                                    try:
                                        data.append(json.loads(client[0].recv(4096)))
                                    except:
                                        connected = False
                                        StateButton.current_game_state = GameState.MENU

                                if not connected:
                                    reset(False, 0)
                                    s.close()
                                    break

                                block_group.update()
                                for i, block in enumerate(block_group):
                                    block.draw(screen)
                                    block_rect_list[i] = block.rect

                                player_group.update(block_rect_list[:len(block_group)])
                                player_rect_list.clear()
                                for player in player_group:
                                    player.draw(screen)
                                    player.movement()
                                    player_rect_list += [player.rect]
                                    if not game_over:
                                        game_over = player.check_loss()
                                    #if game_over:
                                    #    break

                                client_group.update(block_rect_list[:len(block_group)])
                                for i, client in enumerate(client_group):
                                    current_info = data[i]
                                    client.draw(screen)
                                    client.movement_with_input(current_info[0], current_info[1], current_info[2])
                                    player_rect_list += [client.rect]
                                    if not game_over:
                                        game_over = client.check_loss()
                                    #if game_over:
                                    #    break

                                destruction_group.update(screen, block_rect_list[:len(block_group)], player_rect_list) # pass in all args
                                if len(destruction_group) <= 0:
                                    spawn_cooldown -= 1
                                    if spawn_cooldown < 0:
                                        destruction_manager.spawn_destruction()
                                        spawn_cooldown = 60

                                data_to_send = [player.serialize() for player in player_group], [client.serialize() for client in client_group], [block.serialize() for block in block_group], destruction_manager.serialize(), [explosion.serialize() for explosion in explosion_group]
                                for i, client in clients.items():
                                    per_data = json.dumps((i, data_to_send, game_over)).encode()
                                    client[0].sendall(per_data)

                                explosion_group.update(block_rect_list[:len(block_group)], screen)

                                nametag_group.update(player_rect_list, screen)

                                warning.update(screen)

                                if settings["screenshake"]:
                                    shake.update()
                                else:
                                    shake.reset_shake()

                            elif game_over:
                                reset(False, 0)
                                screen.fill((204, 255, 255))

                                text = font_50.render("Game Over! Press R to restart", True, (0, 0, 0))
                                screen.blit(text, (640-text.get_width()/2, 330-text.get_height()/2))

                                keys_pressed = pygame.key.get_pressed()
                                if keys_pressed[pygame.K_r]:
                                    game_over = False
                                    reset(True, len(clients))

                                for client in clients.values():
                                    try:
                                        client[0].sendall(json.dumps(game_over).encode())
                                    except:
                                        connected = False
                                        StateButton.current_game_state = GameState.MENU
                                        break

                            pygame.display.flip()
                            clock.tick(60)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()





    elif source == 1:
        player_rect_list: list[pygame.Rect] = []

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((204, 255, 255))

            if current_game_state in in_game:
                pass
            elif current_game_state not in in_game:
                button_group.update(screen)
                state_button_group.update(screen)
                current_game_state = StateButton.current_game_state
                if current_game_state in in_game:
                    current_game_state = GameState.MENU

                if current_game_state is GameState.MENU:
                    text = font_50.render("Destruction Island", True, (255, 0, 0))
                    text2 = font_50.render("Destruction Island", True, (0, 0, 0))
                    screen.blit(text2, ((screen.get_width()/2) - (text2.get_width()/2) - 5, 60))
                    screen.blit(text, ((screen.get_width()/2) - (text.get_width()/2) + 5, 55))
                elif current_game_state is GameState.COSTUME:
                    pass
                elif current_game_state is GameState.SETTINGS:
                    pass
                elif current_game_state is GameState.ONLINE:
                    HOST = input("IP: ") # type: ignore
                    PORT = int(input("Port: ")) # type: ignore
                    #HOST = "127.0.0.1" # type: ignore
                    #PORT = 1234 # type: ignore
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        connected = False
                        try: 
                            s.connect((HOST, PORT))
                            connected = True
                        except:
                            pass

                        if connected:
                            game_over = False
                            amount_of_clients: int = json.loads(s.recv(1024))

                            host_image = player_image
                            flip = False
                            players_image = {i: player_image for i in range(amount_of_clients)}
                            jumped = False
                            move_left = False
                            move_right = False
                            id = -1

                            spawn_nametags(amount_of_clients+1)

                            client_data: tuple[list[tuple[tuple[int, int], bool, float]], list[tuple[tuple[int, int], bool, float]], list[dict[str, str | list[float]]], list[Any], list[tuple[float, tuple[int, int], int]]] = ([((0, 0), False, 0)], [((0, 0), False, 0)], [{"": ""}], [], [(0, (0, 0), 0)])

                            while connected:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        connected = False
                                        current_game_state = GameState.MENU

                                if not game_over:
                                    explosion_image = pygame.Surface((1280, 720), pygame.SRCALPHA)

                                    keys_pressed = pygame.key.get_pressed()
                                    data_to_send = (move_left, move_right, jumped)
                                    s.sendall(json.dumps(data_to_send).encode())
                                    try:
                                        client_info: tuple[int, tuple[list[tuple[tuple[int, int], bool, float]], list[tuple[tuple[int, int], bool, float]], list[dict[str, str | list[float]]], list[Any], list[tuple[float, tuple[int, int], int]]], bool] = json.loads(s.recv(16384))
                                        id = client_info[0]
                                        client_data = client_info[1]
                                        game_over = client_info[2]
                                    except:
                                        pass

                                    screen.fill((204, 255, 255))

                                    shake.add_shake(client_data[1][id][2])
                                    shake_values = shake.get_shake()

                                    island_data = client_data[2]
                                    for block_data in island_data:
                                        image = Blocks[str(block_data["img"])].value[0]
                                        xy = block_data["xy"]
                                        if type(xy) is list:
                                            screen.blit(image, (xy[0]+shake_values[0], xy[1]+shake_values[1]))

                                    player_rect_list.clear()

                                    player_xy = client_data[0][0][0] # the host player
                                    flip = client_data[0][0][1]
                                    if flip:
                                        host_image = pygame.transform.flip(host_image, True, False)
                                    screen.blit(host_image, (player_xy[0]+shake_values[0], player_xy[1]+shake_values[1]))
                                    player_rect_list.append(host_image.get_rect(topleft=player_xy))

                                    for i, player_data in enumerate(client_data[1]):
                                        xy = player_data[0]
                                        if player_data[1]:
                                            players_image[i] = pygame.transform.flip(players_image[i], True, False)

                                        screen.blit(players_image[i], (xy[0]+shake_values[0], xy[1]+shake_values[1]))
                                        player_rect_list.append(players_image[i].get_rect(topleft=xy))

                                    for destruction in client_data[3]:
                                        if type(destruction[1]) is str:
                                            image = DestructionImages[destruction[1]].value
                                            if type(destruction[0][0]) is float or type(destruction[0][0]) is int:
                                                rect = image.get_rect(center=destruction[0])
                                            else:
                                                rect = image.get_rect(center=destruction[0][0])
                                                image = pygame.transform.rotate(image, degrees(destruction[0][1]))

                                            screen.blit(image, rect)

                                        elif type(destruction[0]) is int or type(destruction[0]) is float: # for circles
                                            image = pygame.Surface(destruction[3], pygame.SRCALPHA)
                                            rect = pygame.draw.circle(image, destruction[2], (destruction[0], destruction[0]), destruction[0])
                                            rect.center = destruction[1]
                                            screen.blit(image, rect)

                                        else:
                                            image = pygame.Surface(destruction[2], pygame.SRCALPHA)
                                            image.fill(destruction[1])

                                            if type(destruction[0][-1]) is int: # if angle included
                                                image = pygame.transform.rotate(image, destruction[0][-1])
                                                rect = image.get_rect(center=destruction[0][0])
                                            elif type(destruction[0][0]) is list: # for cases with xy and offset
                                                rect = image.get_rect(center=destruction[0][0])
                                            else: # for all other situations
                                                rect = image.get_rect(center=destruction[0])

                                            if type(destruction[0][1]) is list: # for offset values
                                                rect.x += destruction[0][1][0]
                                                rect.y += destruction[0][1][1]

                                            screen.blit(image, rect) # should always work

                                    for explosion in client_data[4]:
                                        explosion_strength = explosion[0]
                                        pygame.draw.circle(explosion_image, (255, 0, 0, 255-int(abs(explosion[2])*4.3220339)), (explosion_strength, explosion_strength), explosion_strength)
                                        screen.blit(explosion_image, (explosion[1][0]-explosion_strength, explosion[1][1]-explosion_strength))

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

                                    if settings["screenshake"]:
                                        shake.update()
                                    else:
                                        shake.reset_shake()

                                elif game_over:
                                    host_image = player_image
                                    try:
                                        game_over = json.loads(s.recv(1024))
                                    except:
                                        pass

                                    screen.fill((204, 255, 255))

                                    text = font_50.render("Game Over! Wait for host to restart", True, (0, 0, 0))
                                    screen.blit(text, (640-text.get_width()/2, 330-text.get_height()/2))

                                    if type(game_over) is not bool:
                                        game_over = True

                                pygame.display.flip()
                                clock.tick(60)

            pygame.display.flip()
            clock.tick(60)

        #pygame.quit()