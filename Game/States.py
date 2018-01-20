from Game.Game import Event
from abc import *


class IGameAction:
    def __init__(self, game, next_state=None):
        self._game = game
        self._next_state = next_state

    @abstractmethod
    def _action_callback(self, event):
        pass

    def next(self) -> None:
        return self._next_state


# Мне кажется его надо выпелить
class CardWait(IGameAction):
    def __init__(self, card, game, next_state):
        super().__init__(game, next_state)
        self._card = card

    def _swap_role_callback(self, init_player, target_player):
        init_player.role, target_player.role = target_player.role, init_player.role
        self._game.log_event(Event.ChangeRole, init_player.id, target_player.id)

    def _listener_callback(self, player):
        self._game.send(player._role)

        if self._game.active_player.role != player.role:
            self._game.log_event(Event.SuccessListen, self._game.active_player.id, player.id)


class RoleChange(IGameAction):
    def _action_callback(self, init_player, target_player):
        init_player.role, target_player.role = target_player.role, init_player.role
        self._game.log_event(Event.ChangeRole, init_player.id, target_player.id)


class MafiaVoting(IGameAction):
    def _action_callback(self, vote_result):
        if str.isdecimal(vote_result):
            vote_number = int(vote_result)
        else:
            return

        if vote_number == -1:
            return

        if -1 < vote_number < len(self._game.active_player):
            self._game.selected_player = self._game.players[vote_number]


class MafiaRecruiting(IGameAction):
    def _action_callback(self, recruit_player):
        pass


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
