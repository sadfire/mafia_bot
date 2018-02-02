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


class Member:
    def __init__(self, id, name, is_host=False, phone_number=0, t_id=0) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.is_host = is_host
        self.phone_number = phone_number
        self.t_id = t_id
        self.game_info = None
        self.number = None

    def decode(self):
        return json.dumps((self.id, self.name, self.is_host, self.phone_number, self.t_id, self.game_info))

    @classmethod
    def encode(cls, raw):
        raw = json.loads(raw)
        member = Member(raw[0], raw[1], raw[2], raw[3], raw[4])
        member.game_info = raw[5]
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
