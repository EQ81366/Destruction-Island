from enum import Enum
from src.destructions.bomb import bomb_group, Bomb
from src.destructions.missile import missile_group, Missile
from src.destructions.laser_line import laser_line_group, LaserLine
from src.destructions.block_hole import black_hole_group, BlackHole
from src.destructions.big_bomb import big_bomb_group, BigBomb
from src.destructions.laser import laser_group, Laser
from src.destructions.white_hole import white_hole_group, WhiteHole

class Destructions(Enum):
    BOMB = Bomb, bomb_group
    MISSILE = Missile, missile_group
    LASER_LINE = LaserLine, laser_line_group
    BLACK_HOLE = BlackHole, black_hole_group
    BIG_BOMB = BigBomb, big_bomb_group
    LASER = Laser, laser_group
    WHITE_HOLE = WhiteHole, white_hole_group