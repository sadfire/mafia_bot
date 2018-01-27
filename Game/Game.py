from enum import Enum

from Game.Player import Player


class Event(Enum):
    SuccessListen = 0,
    FailedListen = 1,


class Game:
    def __init__(self, evening) -> None:
        super().__init__()
        self.active_player = None
        #Q: Либо оставить общее поле для всех случаев, когда для чего-либо выбирается игрок (Голосование, выбор мафии)
        #   Либо для каждого такого события сделать отдельное поле
        self.selected_player = None
        self._evening = evening
        self.players = [Player(member.id, member.name) for member in self._evening.members.values()]

    @property
    def get_alive_players(self):
        return [player for player in self.players if player.is_alive]

    def log_event(self, event, initiator_player, target_player):
        pass

