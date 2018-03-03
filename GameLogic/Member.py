from enum import Enum

from GameLogic import Roles
from Utils import emoji_number


class GameInfo(Enum):
    Role = 0
    Card = 1
    Number = 3
    Warnings = 4

    IsAlive = 5
    IsNotTalked = 6
    IsNotSilence = 7
    IsOnVote = 8
    IsHaveVote = 9
    IsNotImmunity = 10
    IsNotHidden = 11
    Seconds = 12


class Member:
    def __init__(self, id, name, is_host=False, phone_number=0, t_id=0, t_name="") -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.is_host = is_host
        self.phone_number = phone_number
        self.t_id = t_id
        self.game_info = None
        self.number = None
        self.t_name = t_name

    @property
    def get_num_str(self):
        return emoji_number(self.number)

    @property
    def get_role_str(self):
        if self.game_info is None:
            return ""

        if self.game_info[GameInfo.Role] is Roles.Civilian:
            return '👨🏼‍💼'
        elif self.game_info[GameInfo.Role] is Roles.Mafia:
            return '🕵🏼'
        elif self.game_info[GameInfo.Role] is Roles.Commissar:
            return '👮'
        return ""

    def __str__(self):
        return self.name + self.get_role_str

    def __eq__(self, other):
        return self.id == other.id

    def __getitem__(self, key: GameInfo):
        return self.game_info.get(key, None)

    def __setitem__(self, key, value):
        self.game_info[key] = value
