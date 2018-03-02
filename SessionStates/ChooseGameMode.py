from GameLogic import GameMode
from SessionStates import IState, GameStartConfirmation

from Utils import kbf


class ChooseGameMode(IState):
    def __init__(self, session):
        super().__init__(session)
        self._next = GameStartConfirmation

    def _greeting(self) -> None:
        self._message = self._session.send_message("Выберите режим игры", reply_markup=self.game_mode_kb)

    @property
    def game_mode_kb(self):
        kb = kbf.empty()
        for mode_name, mode_id in [(GameMode.get_name(mode), mode.value) for mode in GameMode]:
            kb += kbf.button(mode_name, self.choose_mode, mode_id)
        return kb

    def choose_mode(self, bot, update, mode):
        mode = GameMode(mode)
        owner = self._session.owner
        self._session.evening.get_game(owner).set_mode(mode)
        self._session.edit_message(self._message, "Выбран {}".format(GameMode.get_name(mode)))
        self._session.to_next_state()

