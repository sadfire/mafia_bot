import json
from enum import Enum

from emoji import emojize

from GameLogic.Roles import Roles
from KeyboardUtils import emoji_number


class GameInfo(Enum):
    Role = 0
    Card = 1
    IsAlive = 2
    Number = 3
    IsVoting = 4
    IsSilence = 5
    IsImmunitet = 6
    Warnings = 7
    IsCardSpent = 8
    IsTalked = 9
    IsTimer = 10

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

    def decode(self):
        gi = None
        if self.game_info is not None:
            gi = {}
            for info in self.game_info:
                gi[info._name_] = self.game_info[info] if info != GameInfo.Role else self.game_info[info]._name_

        return json.dumps((self.id, self.name, self.is_host, self.phone_number, self.t_id, gi))

    @classmethod
    def encode(cls, raw):
        raw = json.loads(raw)
        member = Member(raw[0], raw[1], raw[2], raw[3], raw[4])
        if raw[5] is not None:
            member.game_info = {}

            for raw_key, raw_info in raw[5].items():

                type = getattr(GameInfo, raw_key, None)
                if type is GameInfo.Role:
                    raw_info = getattr(Roles, raw_info, None)

                member.game_info[type] = raw_info

        return member

    @property
    def get_num_str(self):
        return emoji_number(self.number)

    @property
    def get_role_str(self):
        if self.game_info[GameInfo.Role] is Roles.Civilian:
            return '👨🏼‍💼'
        elif self.game_info[GameInfo.Role] is Roles.Mafia:
            return '🕵🏼'
        elif self.game_info[GameInfo.Role] is Roles.Commissar:
            return emojize(':cop:')
        return ""

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __getitem__(self, key: GameInfo):
        return self.game_info.get(key, None)

    def __setitem__(self, key, value):
        self.game_info[key] = value
