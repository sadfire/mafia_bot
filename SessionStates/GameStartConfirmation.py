from SessionStates.IStates import IState
from Utils.KeyboardUtils import KeyboardFactory as kbf


class GameStartConfirmation(IState):
    def _greeting(self) -> None:
        self._session.send_message(text="Вы готовы начать игру?",
                                   reply_markup=kbf.confirmation(self.start_game_callback,
                                                                 self._session.reset_session_state_callback))

    def start_game_callback(self, _, update):
        self._session.remove_markup(update)
        self._session.to_next_state()

    def next(self):
        game = self._session.evening.get_game(self._session.owner)
        next_state = game.get_first_view
        model = None
        if isinstance(next_state, tuple):
            model = next_state[1]
            next_state = next_state[0]

        self._next = next_state
        return self._next(session=self._session,
                          game=game,
                          model=model,
                          next_state=None)
