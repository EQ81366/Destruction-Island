import pygame
from enum import Enum

pygame.display.init()
pygame.font.init()

flags = pygame.NOFRAME | pygame.HIDDEN
pygame.display.set_mode(flags=flags)

font_50 = pygame.font.SysFont("knewave", 50)
font_30 = pygame.font.SysFont("knewave", 30)

SCREEN_BOX = pygame.Rect(0, 0, 1280, 720)

images = "src/images"


class RootPaths(Enum):
    BLOCKS = f"{images}/blocks"
    RUBBLE = f"{images}/rubble"
    DESTRUCTIONS = f"{images}/destructions"
    THUNDERCLOUD = f"{DESTRUCTIONS}/storm"


class Blocks(Enum):
    #                                                                                    hardness
    GRASS = (
        pygame.image.load(f"{RootPaths.BLOCKS.value}/grass_block.png").convert_alpha(),
        70,
    )
    DIRT = (
        pygame.image.load(f"{RootPaths.BLOCKS.value}/dirt_block.png").convert_alpha(),
        50,
    )
    STONE = (
        pygame.image.load(f"{RootPaths.BLOCKS.value}/stone_block.png").convert_alpha(),
        150,
    )
    MUD = (
        pygame.image.load(f"{RootPaths.BLOCKS.value}/mud_block.png").convert_alpha(),
        10,
    )


class Rubble(Enum):
    GRASS = pygame.image.load(
        f"{RootPaths.RUBBLE.value}/dirt_rubble.png"
    ).convert_alpha()
    DIRT = pygame.image.load(
        f"{RootPaths.RUBBLE.value}/dirt_rubble.png"
    ).convert_alpha()
    STONE = pygame.image.load(
        f"{RootPaths.RUBBLE.value}/dirt_rubble.png"
    ).convert_alpha()
    MUD = pygame.image.load(
        f"{RootPaths.RUBBLE.value}/dirt_rubble.png"
    ).convert_alpha()


class DestructionImages(Enum):
    BOMB = pygame.image.load(f"{RootPaths.DESTRUCTIONS.value}/bomb.png").convert_alpha()
    MISSILE = pygame.image.load(
        f"{RootPaths.DESTRUCTIONS.value}/missile.png"
    ).convert_alpha()
    # LASER_LINE = None
    # BLACK_HOLE = None
    BIG_BOMB = pygame.image.load(
        f"{RootPaths.DESTRUCTIONS.value}/big_bomb.png"
    ).convert_alpha()
    LASER = pygame.image.load(
        f"{RootPaths.DESTRUCTIONS.value}/laser_warning.png"
    ).convert_alpha()
    METEOR = pygame.image.load(
        f"{RootPaths.DESTRUCTIONS.value}/meteor.png"
    ).convert_alpha()
    BUNKER_MISSILE = pygame.image.load(f"{RootPaths.DESTRUCTIONS.value}/bunker_missile.png").convert_alpha()
    THUNDERCLOUD = pygame.image.load(f"{RootPaths.THUNDERCLOUD.value}/thunder_cloud.png").convert_alpha() 
    WIND = pygame.image.load(f"{RootPaths.THUNDERCLOUD.value}/wind.png").convert_alpha()
    WATER = pygame.image.load(f"{RootPaths.THUNDERCLOUD.value}/wooteer.png").convert_alpha()


class ButtonTypes(Enum):
    BOOL = 0
    SLIDE = 1


class StateButtons(Enum):
    ONE_PLAYER = 1
    TWO_PLAYER = 2
    COSTUME = 3
    SETTINGS = 4
    ONLINE = 5
    DESTROYER = 6
    BACK = 7


class GameState(Enum):
    MENU = 0
    ONE_PLAYER = 1
    TWO_PLAYER = 2
    COSTUME = 3
    SETTINGS = 4
    ONLINE = 5
    DESTROYER = 6
    BACK = 7
    DEATH_SCREEN = 8


DEFAULT_GAME_STATE: GameState = GameState.MENU


class DestrutionSpawns(Enum):
    BOMB = pygame.K_y, 200
    MISSILE = pygame.K_o, 100
    LASER_LINE = pygame.K_l, 600
    BLACK_HOLE = pygame.K_n, 1100
    BIG_BOMB = pygame.K_b, 800
    LASER = pygame.K_u, 500
    WHITE_HOLE = pygame.K_p, 2000
    METEOR = pygame.K_i, 1000
    BUNKER_MISSILE = pygame.K_m, 1400
    THUNDERSTORM = pygame.K_t, 2500