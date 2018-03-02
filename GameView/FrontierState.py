from SessionStates import IState


class FrontierState(IState):
    def __init__(self, session, game, is_greeting=True, *args):
        super().__init__(session, is_greeting)
        self.game = game

    def _greeting(self) -> None:
        pass

    def next(self):
        return super().next()