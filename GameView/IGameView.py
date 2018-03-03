from types import ModuleType

from SessionStates.IStates import IState


class IGameView(IState):
    def __init__(self, session, game, model=None, is_greeting=True):
        self.game = game

        if isinstance(model, type):
            self._model = model(game)
        else:
            self._model = model

        self._target = None


        super(IGameView, self).__init__(session, is_greeting)

    def _greeting(self):
        pass

    def next(self):
        next_state_class = self._next
        model = None

        if isinstance(next_state_class, tuple):
            next_state_class, model = next_state_class
        try:
            next_state = next_state_class(session=self._session,
                                          game=self.game,
                                          model=model)
        except TypeError as e:
            print(next_state_class.__name__ if getattr(next_state_class, __name__, None) is not None else "None", self.__class__, e)
            exit(0)

        return next_state.next() if next_state.is_pseudo else next_state
