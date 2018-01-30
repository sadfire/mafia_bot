from SessionHandler.IStates import IState


class IGameView(IState):
    _WRONG_PARAM_ = -1
    _FAIL_ = 0

    def _greeting(self):
        pass

    def __init__(self, session, game, next_state, previous=None):
        super(IGameView, self).__init__(session, previous)
        self._game = game
        self._next = next_state

    def next(self):
        if self._next is None:
            return self
        return self._next(self._session, self._game, None, self.__class__)
