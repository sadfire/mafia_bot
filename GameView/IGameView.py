from types import ModuleType

from SessionStates.IStates import IState


class IGameView(IState):
    def _greeting(self):
        pass

    def __init__(self, session, game, next_state, model=None, is_greeting=True):
        self.game = game
        self._model = model
        self._next = next_state
        self._target = None
        super(IGameView, self).__init__(session, None, is_greeting)

    def next(self):
        model = None
        next_state = self._next

        if isinstance(next_state, ModuleType):
            raise TypeError(next_state.__name__)

        if next_state is None:
            raise TypeError(self.__class__.__name__)

        if isinstance(next_state, tuple):
            self._next, model = next_state

        next_state = self._next(session=self._session,
                                game=self.game,
                                model=model,
                                next_state=None)

        return next_state.next() if next_state.is_pseudo else next_state

