import operator
from random import shuffle, sample

from KeyboardFactory import KeyboardFactory as KBF
from SessionHandler.IStates import IState, get_query_text, emoji_number
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
            kb += KBF.double_button(left_text=player.name,
                                    left_callback=self._choose_player_callback,
                                    left_arguments=player.id,
                                    right_text=emoji_number(number),
                                    right_callback=self._choose_number_callback,
                                    right_arguments=number)
        return kb + KBF.button("Случайный порядок", self._randomize_callback) + KBF.button("Закончить", self._end_players_calculating_callback)

    def __init__(self, session, previous=None):
        super().__init__(session, previous)

        self.players = self._session.evening.members.values()
        self._randomize_callback()

        self._active_number = None
        self._active_id = None

        self.update_players_list()

    def _randomize_callback(self):
        indexes = list(range(1, 1 + len(self.players)))
        shuffle(indexes)
        self.players = dict(
            sorted(
                [(indexes.pop(), player) for player in self.players],
                key=lambda elem: elem[0]))

    def _choose_player_callback(self, bot, update, id):
        self._active_id = int(id)
        self.update_players_list()

    def _choose_number_callback(self, bot, update, number):
        self._active_number = int(number)
        self.update_players_list()

    def update_players_list(self):
        if self._active_id is not None and self._active_number is not None:
            index = list(self.players.values()).index(self._session.evening.members[self._active_id])
            self.players[self._active_number], self.players[index] \
                = self.players[index], self.players[self._active_number]
            self._active_number = None
            self._active_id = None

        self._message.edit_reply_markup(self.state_kb)

    def _end_players_calculating_callback(self, bot, update):
        # TODO Save players to evening
        self._session.to_next_state()
