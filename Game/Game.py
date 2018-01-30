from enum import Enum

from Game.Roles import Roles as R
from Game.Member import GameInfo as GI


class Event(Enum):
    SuccessListen = 0,
    FailedListen = 1,
    SwapRole = 2,


class Game:
    def __init__(self, host, evening, players) -> None:
        super().__init__()
        self._evening = evening
        self._host = host
        self.players = players
        self.__init_game_info()

    def __init_game_info(self):
        for player in self.players:
            player.game_info = {GI.IsAlive: True,
                                GI.Card: None,
                                GI.Role: R.Civilian}

        self.players = dict([(player.number, player) for player in self.players])

    @property
    def get_alive_players(self):
        return [player for player in self.players if player.game_info[GI.IsAlive]]

    def log_event(self, event, initiator_player, target_player=None):
        pass
