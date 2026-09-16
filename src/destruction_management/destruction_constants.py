from enum import Enum
from src.destructions.bomb import bomb_group, Bomb
from src.destructions.missile import missile_group, Missile
from src.destructions.laser_line import laser_line_group, LaserLine
from src.destructions.block_hole import black_hole_group, BlackHole
from src.destructions.big_bomb import big_bomb_group, BigBomb
from src.destructions.laser import laser_group, Laser
from src.destructions.white_hole import white_hole_group, WhiteHole
from src.destructions.meteor import meteor_group, Meteor


class Destructions(Enum):
    BOMB = Bomb, bomb_group  # 0
    MISSILE = Missile, missile_group  # 1
    LASER_LINE = LaserLine, laser_line_group  # 2
    BLACK_HOLE = BlackHole, black_hole_group  # 3
    BIG_BOMB = BigBomb, big_bomb_group  # 4
    LASER = Laser, laser_group  # 5
    WHITE_HOLE = WhiteHole, white_hole_group  # 6
    METEOR = Meteor, meteor_group  # 7
