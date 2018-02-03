import json
from enum import Enum

from GameLogic.Roles import Roles as R
from GameLogic.Member import GameInfo as GI, Member
from GameLogic.Roles import Roles as R, Roles


class Event(Enum):
    WTF = -1
    SuccessListen = 0,
    FailedListen = 1,
    SwapRole = 2,
    MafiaWantKilled = 3,
    CivilianWantKilled = 4,
    Heal = 5,
    JacketSave = 6
    MafiaKilled = 7,
    CivilianKilled = 8,
    SuccessCommissarCheck = 9,
    FailedCommissarCheck = 10,
    Kick = 11,
    Warning = 12,

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
        self.events = []

        if isinstance(host, Member):
            self._host_id = host.id
        elif isinstance(host, int):
            self._host_id = host

        self.players = players
        if not isinstance(players, dict):
            self.__init_game_info()

        self.candidates = []

<<<<<<< HEAD

=======
    @property
    def get_first_view(self):
        if self.mode is GameMode.Beginner:
            from GameLogic.Views.CardView import CardView
            from GameLogic.Models.SwapRoleModel import SwapRoleModel

            return CardView, SwapRoleModel
        elif self.mode is GameMode.Standard:
            from GameLogic.Views.IntroductionView import IntroductionView

            return IntroductionView, True
>>>>>>> main_scenario_process

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
                                GI.IsCardSpent: False,
                                GI.IsTalked: True,
                                GI.Warnings: 0,
                                GI.IsTimer: False}

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
        self.events.append(event)
        print(event._name_, str(initiator_players), str(target_player))
        if event is Event.MafiaKilled:
            self.gonna_die = target_player


    def get_next_event_number(self):
        self._evening += 1
        return self._evening

<<<<<<< HEAD
    def log_event(self, event: Event, initiator_players, target_player=None):
        db = self._evening.db
        #db.insert_event()


=======
    @property
    def get_commissar_number(self):
        for number, player in self.players.items():
            if player[GI.Role] == R.Commissar:
                return number
        return None

    def kill(self):
        self.players[self.gonna_die][GI.IsAlive] = False

        kill_event = Event.WTF
        role = None
        for event in self.events[::-1]:
            if event is Event.MafiaWantKilled:
                kill_event = Event.MafiaKilled
                role = Roles.Mafia
                break
            elif event is Event.CivilianWantKilled:
                kill_event = Event.CivilianKilled
                role = Roles.Civilian
                break

        self.log_event(kill_event, role, self.gonna_die)
        self.gonna_die = None
>>>>>>> main_scenario_process
