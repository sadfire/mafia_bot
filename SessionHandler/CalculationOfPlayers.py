from random import shuffle

from KeyboardUtils import KeyboardFactory as KBF, emoji_number
from SessionHandler.IStates import IState
from SessionHandler.GameInProcess import GameInProcess


class CalculationOfPlayers(IState):
    # TODO Добавить счетчик игр и чтобы тут писался номер игры
    def _greeting(self) -> None:
        super()._greeting()
        self._message = self._session.send_message("Расчет игроков")

    @property
    def state_kb(self):
        kb = KBF.empty()
        for number, player in self.players.items():
            kb += KBF.double_button(right_text=("⚪️ " if player.id != self._active_id else "🔘 ") + player.name,
                                    right_callback=self._choose_player_callback,
                                    right_arguments=player.id,

                                    left_text=("⚪️ " if int(number) != self._active_number else "🔘 ") +
                                              str(emoji_number(number)),
                                    left_callback=self._choose_number_callback,
                                    left_arguments=number)
        return kb + \
               KBF.button("📊 Отсортировать по рейтингу", self._sort_by_rate_callback) + \
               KBF.button("➰ Случайный порядок", self._randomize_callback) + \
               KBF.button("☑️Закончить", self._end_players_calculating_callback)

    def __init__(self, session, previous=None):
        super().__init__(session, previous)
        self._next = GameInProcess
        self._active_number = None
        self._active_id = None

        self._randomize_callback()

    def _sort_by_rate_callback(self, bot, update):
        pass

    def _randomize_callback(self, _=None, __=None):
        self.players = self._session.evening.members.values()

        indexes = list(range(1, 1 + len(self.players)))
        shuffle(indexes)
        self.players = dict(
            sorted(
                [(indexes.pop(), player) for player in self.players],
                key=lambda elem: elem[0]))
        self.update_players_list()

    def _choose_player_callback(self, _, __, id):
        self._active_id = int(id)
        self.update_players_list()

    def _choose_number_callback(self, _, __, number):
        self._active_number = int(number)
        self.update_players_list()

    def update_players_list(self):
        if self._active_id is not None and self._active_number is not None:
            index = list(self.players.values()).index(self._session.evening.members[self._active_id]) + 1
            self.players[self._active_number], self.players[index] \
                = self.players[index], self.players[self._active_number]
            self._active_number = None
            self._active_id = None

        self._session.edit_message(self._message, "Расчёт игроков", self.state_kb)

    def _end_players_calculating_callback(self, bot, update):
        self._session.delete_message_callback(bot, update)
        message_text = "👁 🔛 👤{}".format(self._session.owner.name) + '\n\n'
        for number, player in self.players.items():
            message_text += "{} 🔛 👤{}\n".format(emoji_number(number), player.name)

        self._session.send_message(message_text)

        self._session.to_next_state()
