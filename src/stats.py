from enum import Enum


class Stats:
    high_score: int = 0
    accumulate_destruction: bool = False
    destruction: int = 0
    destruction_spawn_cd: int = 60
    class Settings(Enum):
        DUMMY = -1
        NAMETAGS = 0
        SCREENSHAKE = 1
        RUBBLE = 2

    def __init__(self):
        self.settings: dict[Stats.Settings, bool|float] = {Stats.Settings.NAMETAGS: True, Stats.Settings.SCREENSHAKE: True, Stats.Settings.RUBBLE: True}
        self.score: int = 0

    def change_setting(self, setting: Settings, new_setting: bool|float):
        if (type(self.settings[setting]) is bool and type(new_setting) is bool) or (type(self.settings[setting]) is float and type(new_setting) is float):
            self.settings[setting] = new_setting
        else:
            print("----------------")
            pass

    def get_settings(self):
        return self.settings

    def get_setting(self, setting: Settings):
        return self.settings[setting]

    def reset_score(self):
        self.score = 0

    def check_highscore(self):
        if self.score > Stats.high_score:
            Stats.high_score = self.score
            return True
        return False

    @classmethod
    def get_highscore(cls):
        return cls.high_score

    @classmethod
    def change_highscore(cls, new_score: int):
        cls.high_score = new_score
            

stat_manager = Stats()