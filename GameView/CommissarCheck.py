from GameLogic import Cards, Event, GameInfo as GI

from GameLogic.Models.Cards import ListenerModel

from GameLogic import Roles as R

from GameView import CardView, IGameView

from Utils import kbf, emoji_number


class CommissarCheck(IGameView):
    def __init__(self, session, game, next_state, model=None):
        self._next = CardView, ListenerModel
        if not game.is_commissar:
            self._message = self._session.send_message("Коммисар мертв.\n")
            self._session.to_next_state()
            return

        super().__init__(session, game, next_state, model)

    def _greeting(self):
        if self.game.is_commissar:
            self._message = self._session.send_message("Доброй ночи коммиссар 👮\nКого будет проверять этой ночью?",
                                                       reply_markup=self.get_commissar_kb)

    @property
    def get_commissar_kb(self):
        players = list(self.game.get_alive_players)
        players.remove(self.game.get_commissar_number)

        kb = kbf.empty()

        cards = self.game.commissar_cards
        if len(cards) != 0:
            for card in cards:
                kb += kbf.button(Cards.get_name(card), self.card_callback, card.value)

        for number in players:
            kb += kbf.button("🔍 {}".format(emoji_number(number)), self.check_callback, number)
        return kb

    def card_callback(self, bot, update):
        pass

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
        self._session.remove_markup(update)
        self._session.to_next_state()
