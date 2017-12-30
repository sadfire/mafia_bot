from enum import Enum

from Game.Player import Player


class Event(Enum):
    SuccessListen = 0,


class Game:
    def __init__(self, evening) -> None:
        super().__init__()
        self.active_player = None
        self._evening = evening
        self.players = [Player(member.id, member.name) for member in self._evening.members.values()]

    @property
    def get_alive_players(self):
        return [player for player in self.players if player.is_alive]

    def log_event(self, event, initiator_player, target_player):
        pass
