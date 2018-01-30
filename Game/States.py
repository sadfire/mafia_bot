from Game import Roles
from Game.Game import Event
from abc import *


class IGameAction:
    _WRONG_PARAM_ = -1
    _FAIL_ = 0

    def __init__(self, game, next_state=None):
        self._game = game
        self._next_state = next_state

    @abstractmethod
    def _action_callback(self, event):
        pass

    def next(self) -> None:
        return self._next_state

    def _check_player(self, player_number):
        if not str.isdecimal(player_number) or -1 < int(player_number) < len(self._game.active_player):
            return IGameAction._WRONG_PARAM_

        return int(player_number)


class RoleChange(IGameAction):
    def _action_callback(self, init_index, target_index):
        self._game.players[init_index].role, self._game.players[target_index].role = \
            self._game.players[target_index].role, self._game.players[init_index].role

        self._game.log_event(Event.ChangeRole, self._game.players[init_index], self._game.players[init_index])


class MafiaVoting(IGameAction):
    def _action_callback(self, vote_index):
        if vote_index == MafiaVoting._FAIL_:
            self._game.log_event(Event.MafiaVoting, vote_index)
            return

        self._game.selected_player = self._game.players[vote_index]
        self._game.log_event(Event.MafiaVote, vote_index)


class MafiaRecruiting(IGameAction):
    def _action_callback(self, recruit_index):
        if recruit_index == MafiaVoting._FAIL_:
            self._game.log_event(Event.MafuaRecrute, recruit_index)
            return

        self._game.players[recruit_index].role = Roles.Mafia
        self._game.log_event(Event.MafiaRecrute, recruit_index)


class MafiaNight(IGameAction):
    pass


class CommissarNight(IGameAction):
    pass


class Morning(IGameAction):
    pass


class Talking(IGameAction):
    pass


class Voting(IGameAction):
    pass


class Death(IGameAction):
    pass
