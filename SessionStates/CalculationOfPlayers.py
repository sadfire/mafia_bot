from random import shuffle

from KeyboardUtils import KeyboardFactory as kbf, emoji_number
from SessionStates.IStates import IState
from SessionStates.GameStartConfirmation import GameStartConfirmation


class CalculationOfPlayers(IState):

    def __init__(self, session, previous=None):
        super().__init__(session, previous)
        self._next = GameStartConfirmation
        self._active_number = None
        self._active_id = None

        self._randomize_callback()

    # TODO Добавить счетчик игр и чтобы тут писался номер игры
    def _greeting(self) -> None:
        super()._greeting()
        self._message = self._session.send_message("Расчет игроков")

    @property
    def calculating_keyboard(self):
        kb = kbf.empty()
        for number, player in self.players.items():
            point_u = ("⚪️ " if int(number) != self._active_number else "🔘 ")
            point_n = ("⚪️ " if player.id != self._active_id else "🔘 ")
            kb += kbf.action_line((point_u + str(emoji_number(number)),
                                   self._choose_number_callback,
                                   number),
                                  (point_n + player.name,
                                   self._choose_player_callback,
                                   player.id)
                                  )
        return kb + \
               kbf.button("📊 Отсортировать по рейтингу", self._sort_by_rate_callback) + \
               kbf.button("➰ Случайный порядок", self._randomize_callback) + \
               kbf.button("☑️Закончить", self._end_players_calculating_callback)

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

        self._session.edit_message(self._message, "Расчёт игроков", self.calculating_keyboard)

    def _end_players_calculating_callback(self, bot, update):
        self._session.delete_message_callback(bot, update)
        message_text = "👁 🔛 👤{}".format(self._session.owner.name) + '\n\n'

        if len(self.players) > 10:
            self.players = dict(list(self.players.items())[:10])

        for number, player in self.players.items():
            player.number = number
            message_text += "{} 🔛 👤{}\n".format(emoji_number(number), player.name)

        self._session.start_game(self.players.values())

        self._session.send_message(message_text)

        self._session.to_next_state()
