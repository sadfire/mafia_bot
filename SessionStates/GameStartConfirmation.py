from GameLogic.Game import Game
from GameLogic.Views.IntroductionView import IntroductionView
from SessionStates.IStates import IState
from KeyboardUtils import KeyboardFactory as kbf


class GameStartConfirmation(IState):
    def _greeting(self) -> None:
        self._session.send_message(text="Вы готовы начать игру?",
                                   reply_markup=kbf.confirmation(self.start_game_callback,
                                                                 self._session.reset_session_state_callback))

    def start_game_callback(self, _, __):
        self._next = IntroductionView(self._session,
                                      self._session.evening.games[self._session.owner],
                                      None, True)
        self._session.to_next_state()