from emoji import emojize as em

from SessionStates.CalculationOfPlayers import CalculationOfPlayers
from SessionStates.IStates import IState
from Utils.KeyboardUtils import KeyboardFactory, MultiPageKeyboardFactory


class EveningHostAdd(IState):
    def __init__(self, session, previous=None):
        super().__init__(session, previous)
        self._next = CalculationOfPlayers
        self._evening = self._session.get_evening()

    def _greeting(self):
        self._message = self._session.send_message("Хотите добавить еще ведущих в игру?\n"
                                                   "Вы можете сделать это и позже с помощью команды /add_host",
                                                   reply_markup=KeyboardFactory.confirmation(
                                                       self._add_evening_host_callback, self._end_evening_host_manager))

    def _add_evening_host_callback(self, bot, update):
        self._message = self._session.edit_message(self._message, "Кандидаты в ведущие:", reply_markup=self.get_hosts_kb)

    def _add_host_callback(self, bot, update, argument):
        self._evening.add_host(self._session.db.get_member(int(argument)))
        self._message = self._session.edit_message(self._message, self.host_list(), reply_markup=self.get_hosts_kb)

    def host_list(self):
        return "\n".join("👁 🔛 👤{}".format(host) for host in self._evening.hosts)

    def _end_evening_host_manager(self, bot, update):
        self._session.edit_message(message=update.effective_message,
                                   text="Все администраторы могут зайти в текущий вечер из главного меню.")
        self._session.to_next_state()

    @property
    def get_hosts_kb(self):
        hosts = [host for host in self._session.db.get_hosts() if host.id not in self._evening.get_hosts_ids()]

        kb = KeyboardFactory.players_with_action(hosts,
                                                 em(":heavy_plus_sign:"),
                                                 self._session.send_player_info_callback,
                                                 self._add_host_callback)

        return MultiPageKeyboardFactory(kb, 5, KeyboardFactory.button(text="Закончить",
                                                                      callback_data=self._end_evening_host_manager))
