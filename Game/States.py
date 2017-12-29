from Game.Game import Event


class IGameState:
    def __init__(self, game, next_state):
        self._game = game
        self._next_state = next_state

    def process(self, event) -> bool:
        pass

    def next(self) -> None:
        pass


class CardWait(IGameState):
    def __init__(self, card, game, next_state):
        super().__init__(game, next_state)
        self._card = card

    @staticmethod
    def _swap_role_callback(init_player, target_player):
        init_player.role, target_player.role = target_player.role, init_player.role

    def _listener_callback(self, player):
        self._game.send(player._role)
        if self._game.active_player.role != player.role:
            self._game.log_event(Event.SuccessListen, self._game.active_player.id, player.id)

    def _recruitment_callback(self, player):
        self._game.

class MafiaNight(IGameState):
    pass


class CommissarNight(IGameState):
    pass


class Morning(IGameState):
    pass


class Talking(IGameState):
    pass


class Voting(IGameState):
    pass


class Death(IGameState):
    pass
