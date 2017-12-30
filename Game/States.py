from Game.Game import Event


class IGameState:
    def __init__(self, game, next_state):
        self._game = game
        self._next_state = next_state

    def _process(self, event):
        pass

    def next(self) -> None:
        pass


class CardWait(IGameState):
    def __init__(self, card, game, next_state):
        super().__init__(game, next_state)
        self._card = card

    def _process(self, event):
        pass

    def _swap_role_callback(self, init_player, target_player):
        init_player.role, target_player.role = target_player.role, init_player.role
        self._game.log_event(Event.ChangeRole, init_player.id, target_player.id)

    def _listener_callback(self, player):
        self._game.send(player._role)

        if self._game.active_player.role != player.role:
            self._game.log_event(Event.SuccessListen, self._game.active_player.id, player.id)

    def _recruitment_callback(self, player):
        pass


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
