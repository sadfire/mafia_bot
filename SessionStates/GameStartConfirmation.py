from GameView import IGameView
from SessionStates import IState
from Utils import kbf


class GameStartConfirmation(IGameView):
    def __init__(self, session, previous=None, is_greeting=True):
        game = session.evening.get_game(session.owner)
        super().__init__(session, game, None, None, is_greeting)
        self._next = game.get_state(None)

    def _greeting(self) -> None:
        self._session.send_message(text="Вы готовы начать игру?",
                                   reply_markup=kbf.confirmation(self.start_game_callback,
                                                                 self._session.reset_session_state_callback))

    def start_game_callback(self, _, update):
        self._session.remove_markup(update)
        self._session.to_next_state()