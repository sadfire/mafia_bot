import json
from enum import Enum


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

    def decode(self):
        return json.dumps((self.id, self.name, self.is_host, self.phone_number, self.t_id))

    @classmethod
    def encode(cls, raw):
        raw = json.loads(raw)
        return Member(raw[0], raw[1], raw[2], raw[3], raw[4])

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __getitem__(self, key: GameInfo):
        return self.game_info.get(key, None)