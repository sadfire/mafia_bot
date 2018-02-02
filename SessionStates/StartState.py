from KeyboardUtils import KeyboardFactory as KBF
from SessionStates.IStates import IState
from SessionStates.PlayerManagement import PlayerManagement
from SessionStates.EveningManagement import EveningManagement
from SessionStates.OpenStatistic import OpenStatistic


class StartState(IState):
    def __init__(self, session, previous=None):
        self._evening_connect_mode = False
        super().__init__(session, previous)
        for evening in self._session.all_evenings:
            if self._session.owner.id in evening.hosts:
                self._evening_connect_mode = True
                self._session.evening = evening
                break

    def _greeting(self) -> None:
        appeal = self._session.owner.name if self._session.owner.name != "" else "Ведущий"
        self._session.send_message(text="Приветствую {}. \n "
                                        "Я бот учета статистики игры мафия {}".format(appeal, '🕵'),
                                   reply_markup=KBF.main(self._evening_manager_callback,
                                                         self._open_statistic_callback,
                                                         self._player_manager_callback,
                                                         "Меню вечера"))

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
