import operator
from random import shuffle

from KeyboardFactory import KeyboardFactory as KBF
from SessionHandler.States import IState, get_query_text, emoji_number
from SessionHandler.GameInProcess import GameInProcess


class CalculationOfPlayers(IState):
    # TODO Добавить счетчик игр и чтобы тут писался номер игры
    def _greeting(self) -> None:
        super()._greeting()
        self._message = self._session.send_message("Расчет игроков")

    def __init__(self, session, previous=None):
        super().__init__(session, previous)
        self.players = {}
        self._active_number = None
        self._active_member_id = None
        self._current_game = None
        self.process_randomize_calculation()

        self._update_message()
        self._next = GameInProcess

    def process_randomize_calculation(self):
        self.players.clear()
        indexes = list(range(len(self._session.evening.members)))
        shuffle(indexes)
        for id, member in self._session.evening.members.items():
            self.players[indexes.pop()] = member

    def process_callback(self, bot, update):
        data = get_query_text(update)

        if self.get_number_prefix in data:
            self._number_callback(data.split('_')[-1])

        elif self.get_member_prefix in data:
            self._member_callback(data.split('_')[-1])

        elif self.get_random_query == data:
            self.process_randomize_calculation()

        elif self.get_end_query == data:
            return True

        self._update_message()

    def _update_message(self):
        kb = KBF.button("Перемешать", self.get_random_query)
        for index, member in sorted(self.players.items(), key=operator.itemgetter(0)):

            text_left = member.name
            text_right = emoji_number(index + 1)

            if self._active_member_id == member.id:
                text_left = '*' + text_left
            if self._active_number == index:
                text_right = '*' + text_right

            kb = kb + KBF.button_line(
                ((text_left, f"{self.get_member_prefix}{member.id}"), (text_right, f"{self.get_number_prefix}{index}")))

        self._session.bot.edit_message_reply_markup(chat_id=self._message.chat_id, message_id=self._message.message_id,
                                                    reply_markup=kb + KBF.button("Закончить расчет игроков",
                                                                                 self.get_end_query))

    def _member_callback(self, id):
        self._active_member_id = int(id)
        self._update_calculating()

    def _number_callback(self, index):
        self._active_number = int(index)
        self._update_calculating()

    def _update_calculating(self):
        if self._active_member_id is None or self._active_number is None:
            return

        for index, player in self.players.items():
            if player.id == self._active_member_id:
                swap_index = index
                break
        else:
            raise ValueError()

        self.players[self._active_number], self.players[swap_index] = self.players[swap_index], self.players[
            self._active_number]
        self._active_number, self._active_member_id = None, None

    @property
    def get_random_query(self):
        return "randomize"

    @property
    def get_end_query(self):
        return "end"

    @property
    def get_number_prefix(self):
        return "select_number_"

    @property
    def get_member_prefix(self):
        return "select_member_"