import pygame
from enum import Enum

pygame.display.init()
pygame.font.init()

flags = (pygame.NOFRAME|pygame.HIDDEN)
pygame.display.set_mode(flags=flags)

font_50 = pygame.font.SysFont("knewave", 50)
font_30 = pygame.font.SysFont("knewave", 30)

images = "src/images"

class RootPaths(Enum):
    BLOCKS = f"{images}/blocks"
    DESTRUCTIONS = f"{images}/destructions"

class Blocks(Enum):                                
    #                                                                    hardness      
    GRASS = (pygame.image.load(f"{RootPaths.BLOCKS.value}/grass_block.png").convert_alpha(), 70)
    DIRT = (pygame.image.load(f"{RootPaths.BLOCKS.value}/dirt_block.png").convert_alpha(), 50)
    STONE = (pygame.image.load(f"{RootPaths.BLOCKS.value}/stone_block.png").convert_alpha(), 150)

class DestructionImages(Enum):
    BOMB = pygame.image.load(f"{RootPaths.DESTRUCTIONS.value}/bomb1.png").convert_alpha()
    MISSILE = pygame.image.load(f"{RootPaths.DESTRUCTIONS.value}/missile.png").convert_alpha()
    #LASER_LINE = None
    #BLACK_HOLE = None
    BIG_BOMB = pygame.image.load(f"{RootPaths.DESTRUCTIONS.value}/big_bomb.png").convert_alpha()
    LASER = pygame.image.load(f"{RootPaths.DESTRUCTIONS.value}/laser_warning.png").convert_alpha()

class ButtonTypes(Enum):
    BOOL = 0
    SLIDE = 1

class StateButtons(Enum):
    ONE_PLAYER = 1
    TWO_PLAYER = 2
    COSTUME = 3
    SETTINGS = 4
    ONLINE = 5
    BACK = 6

class GameState(Enum):
    MENU = 0
    ONE_PLAYER = 1
    TWO_PLAYER = 2
    COSTUME = 3
    SETTINGS = 4
    ONLINE = 5
    BACK = 6
    DEATH_SCREEN = 7

DEFAULT_GAME_STATE: GameState = GameState.MENU