from GameLogic.Views.IntroductionView import IntroductionView
from GameLogic.Views.Views import IGameView
from KeyboardUtils import KeyboardFactory as kbf
from SessionStates.IStates import IState


class GameStartConfirmation(IState):
    def _greeting(self) -> None:
        self._session.send_message(text="Вы готовы начать игру?",
                                   reply_markup=kbf.confirmation(self.start_game_callback,
                                                                 self._session.reset_session_state_callback))

    def start_game_callback(self, _, update):
        self._session.remove_markup(update)
        self._next = IntroductionView
        self._session.to_next_state()

    def next(self):
        if self._next is None:
            return self
        return self._next(session=self._session,
                          game=self._session.evening.get_game(self._session.owner),
                          model=None,
                          next_state=None,
                          is_mafia=True)
