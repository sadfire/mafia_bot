import json
from enum import Enum

from GameLogic.Member import GameInfo as GI, Member
from GameLogic.Roles import Roles as R


class Event(Enum):
    SuccessListen = 0,
    FailedListen = 1,
    SwapRole = 2,
    MafiaKilled = 3,
    CivilianKilled = 4,
    Heal = 5,
    JacketSave = 6


class GameMode(Enum):
    Beginner = 0,
    Standard = 1,


class Game:
    def __init__(self, host, evening, players, mode=GameMode.Beginner) -> None:
        self._event_number = 0
        self._evening = evening
        self.mode = mode
        self.gonna_die = None
        self.is_day = False
        self.wasted_cards = []

        if isinstance(host, Member):
            self._host_id = host.id
        elif isinstance(host, int):
            self._host_id = host

        self.players = players
        if not isinstance(players, dict):
            self.__init_game_info()

        self.candidates = []

    @property
    def get_first_view(self):
        if self.mode is GameMode.Beginner:
            from GameLogic.Views.CardView import CardView
            from GameLogic.Models.SwapRoleModel import SwapRoleModel

            return CardView, SwapRoleModel
        elif self.mode is GameMode.Standard:
            from GameLogic.Views.IntroductionView import IntroductionView

            return IntroductionView, True

    def decode(self):
        return json.dumps((self._host_id, [player.decode() for number, player in self.players.items()],
                           [candidate.decode() for candidate in self.candidates]))

    @staticmethod
    def encode(dump, evening):
        tmp = json.loads(dump)
        game = Game(tmp[0], evening, dict([(game_info, Member.encode(player_raw)) for game_info, player_raw in tmp[1]]))
        game.candidates = [Member.encode(candidate) for candidate in tmp[2]]
        return game

    def __init_game_info(self):
        for player in self.players:
            player.game_info = {GI.IsAlive: True,
                                GI.Card: None,
                                GI.Role: R.Civilian,
                                GI.IsVoting: True,
                                GI.IsImmunitet: False,
                                GI.IsCardSpent: False}

        self.players = dict([(player.number, player) for player in self.players])

    def put_on_voting(self, number):
        self.candidates.append(self.players[number])

    def clear_candidates(self):
        self.candidates.clear()

    def __getitem__(self, key: int):
        return self.players.get(key, None)

    def __setitem__(self, key, value):
        self.players[key] = value

    @property
    def get_alive_players(self, is_vote_mode=False) -> list:
        return [number for number, player in self.players.items()
                if player[GI.IsAlive] and
                (True if not is_vote_mode else player[GI.IsVoting])]

    @property
    def get_mafia_numbers(self):
        return [number for number in self.players if
                self.players[number][GI.Role] is R.Mafia and self.players[number][GI.IsAlive]]

    @property
    def mafia_count(self):
        return len(self.get_mafia_numbers)

    @property
    def is_commissar(self):
        return self.get_commissar_number is not None

    def log_event(self, event: Event, initiator_players, target_player=None):
        print(event._name_, str(initiator_players), str(target_player))
        if event is Event.MafiaKilled:
            self.gonna_die = target_player

    def get_next_event_number(self):
        self._evening += 1
        return self._evening

    @property
    def get_commissar_number(self):
        for number, player in self.players.items():
            if player[GI.Role] == R.Commissar:
                return number
        return None
