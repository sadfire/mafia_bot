from GameLogic.Models.HealModel import HealModel

from GameLogic.Cards import Cards
from GameLogic.GameEvents import Event
from GameLogic.Member import GameInfo as GI
from GameLogic.Models.CardsModel.ListenerModel import ListenerModel
from GameLogic.Roles import Roles as R
from GameLogic.Views.CardView import CardView
from GameLogic.Views.DayTalkView import DayTalkView
from GameLogic.Views.Views import IGameView
from KeyboardUtils import KeyboardFactory as kbf, emoji_number


class CommissarCheck(IGameView):
    def __init__(self, session, game, next_state, model=None):
        super().__init__(session, game, next_state, model)

    def _greeting(self):
        if self.game.is_commissar:
            self._message = self._session.send_message("Доброй ночи коммиссар 👮\nКого будет проверять этой ночью?",
                                                       reply_markup=self.get_check_kb)
        else:
            self._message = self._session.send_message("Коммисар мертв.",
                                                       reply_markup=kbf.button("Разбудить город", self._end_callback))

    @property
    def get_check_kb(self):
        players = list(self.game.get_alive_players)
        players.remove(self.game.get_commissar_number)

        kb = kbf.empty()
        for number in players:
            kb += kbf.button("🔍 {}".format(emoji_number(number)), self.check_callback, number)
        return kb

    def check_callback(self, bot, update, number):
        number = int(number)
        if self.game[number][GI.IsImmunitet]:
            check_result = False
        else:
            check_result = self.game[number][GI.Role] == R.Mafia

        self.game.log_event(Event.SuccessCommissarCheck if check_result else Event.FailedCommissarCheck,
                            self.game.get_commissar_number,
                            number)

        text = "{} - 🕵️!" if check_result else "{} это мирный житель 🤷🏼‍♂️."
        self._session.edit_message(message=self._message,
                                   text=text.format(emoji_number(number)) + "\nКоммиссар засыпает",
                                   reply_markup=kbf.button("Разбудить город", self._end_callback))

    def _end_callback(self, bot, update):
        self.game.is_day = True
        if Cards.Retirement in self.game.wasted_cards:
            self._next = DayTalkView if self.game.gonna_die is None or \
                                        self.game.gonna_die == -1 else CardView, HealModel
        else:
            self._next = CardView, ListenerModel

        self._session.remove_markup(update)
        self._session.to_next_state()
