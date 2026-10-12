import random
from noise import pnoise2
from math import copysign

# shake is purely cosmetic, and 100% local


class Shake:
    def __init__(self):
        self.shake_value = 0
        self.shake_x = 0
        self.shake_y = 0
        self.seed = 0

    def add_shake(self, value: float):
        self.shake_value += value
        self.seed = random.randint(0, 100000)

    def update(self):
        x = pnoise2(
            self.shake_value, self.shake_value * 0.3 * self.seed, base=int(abs(self.seed))%1000, octaves=1 
        )
        y = pnoise2(self.shake_value * 0.2, self.shake_value * 0.15, base=int(abs(self.seed))%1000, octaves=1)
        self.shake_x = x * self.shake_value
        self.shake_y = y * self.shake_value
        self.shake_value *= 0.9
        if self.shake_value < 0.1:
            self.shake_value = 0

    def get_shake(self):
        return copysign(abs(self.shake_x) ** 1, self.shake_x), copysign(
            abs(self.shake_y) ** 1, self.shake_y
        )

    def reset_shake(self):
        self.shake_value = 0
        self.shake_x = 0
        self.shake_y = 0


shake = Shake()
