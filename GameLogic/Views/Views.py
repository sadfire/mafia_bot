from SessionStates.IStates import IState


class IGameView(IState):
    def _greeting(self):
        pass

    def __init__(self, session, game, next_state, previous=None):
        super(IGameView, self).__init__(session, previous)
        self.game = game
        self._next = next_state
        self._target = None

    def next(self):
        if self._next is None:
            return self
        return self._next(self._session, self.game, None, self.__class__)
