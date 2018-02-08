from SessionStates.IStates import IState


class IGameView(IState):
    def _greeting(self):
        pass

    def __init__(self, session, game, next_state, model=None):
        self.game = game
        self._next = next_state
        self._target = None
        self._model = model
        super(IGameView, self).__init__(session, None)

    def next(self):
        model = None
        next_state = self._next

        if isinstance(next_state, tuple):
            self._next, model = next_state

        return self._next(session=self._session,
                          game=self.game,
                          model=model,
                          next_state=None)
