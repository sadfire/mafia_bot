from GameView.IGameView import IGameView
from Utils import kbf


class GameStartConfirmation(IGameView):
    def __init__(self, session, game=None, model=None, is_greeting=True):
        game = session.evening.get_game(session.owner)
        super().__init__(session, game, None, is_greeting)

    @property
    def _next(self):
        return self.game.get_state(None)

    def _greeting(self) -> None:
        self._session.send_message(text="Вы готовы начать игру?",
                                   reply_markup=kbf.confirmation(self.start_game_callback,
                                                                 self._session.reset_session_state_callback))

    def start_game_callback(self, _, update):
        self._session.remove_markup(update)
        self._session.to_next_state()