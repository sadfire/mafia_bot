from KeyboardFactory import KeyboardFactory as KBF
from SessionHandler.IStates import IState
from SessionHandler.PlayerManagement import PlayerManagement
from SessionHandler.EveningManagement import EveningManagement
from SessionHandler.OpenStatistic import OpenStatistic


class StartState(IState):
    def _greeting(self) -> None:
        appeal = self._session.host.name if self._session.host.name != "" else "Ведущий"
        self._session.send_message(text="Приветствую {}. \n "
                                        "Я бот учета статистики игры мафия {}".format(appeal, '🕵'),
                                   reply_markup=KBF.main(self._evening_manager_callback,
                                                         self._open_statistic_callback,
                                                         self._player_manager_callback))

    def process_state(self, next_state, update):
        self._next = next_state
        self._session.remove_markup(update)
        self._session.to_next_state()

    def _open_statistic_callback(self, bot, update):
        self.process_state(OpenStatistic, update)

    def _evening_manager_callback(self, bot, update):
        self.process_state(EveningManagement, update)

    def _player_manager_callback(self, bot, update):
        self.process_state(PlayerManagement, update)
