from enum import Enum

from GameLogic.Roles import Roles as R
from GameLogic.Member import GameInfo as GI


class Event(Enum):
    SuccessListen = 0,
    FailedListen = 1,
    SwapRole = 2,
    MafiaKilled = 3,
    CivilianKilled = 4,


class Game:
    def __init__(self, host, evening, players) -> None:
        super().__init__()
        self._evening = evening
        self._host = host
        self.players = players
        self.__init_game_info()
        self.candidates = []

    def __init_game_info(self):
        for player in self.players:
            player.game_info = {GI.IsAlive: True,
                                GI.Card: None,
                                GI.Role: R.Civilian,
                                GI.IsVoting: True}

        self.players = dict([(player.number, player) for player in self.players])

    def put_on_voting(self, number):
        self.candidates.append(self.players[number])

    def clear_candidates(self):
        self.candidates.clear()

    def __getitem__(self, key: int):
        return self.players.get(key, None)

    @property
    def get_alive_players(self, is_vote_mode=False):
        return [player for player in self.players
                if player[GI.IsAlive] and (True if not is_vote_mode else player[GI.IsVoting])]

    @property
    def get_mafia(self):
        return [player for player in self.get_alive_players if player[GI.Role] is R.Mafia]

    def log_event(self, event, initiator_players, target_player=None):
        pass
