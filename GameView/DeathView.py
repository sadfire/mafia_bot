from GameLogic import Cards
from GameLogic.Models import DeathModel
from GameView import IGameView

from Utils import kbf


class DeathView(IGameView):
    def __init__(self, session, game, next_state, model=None):
        super().__init__(session, game, next_state, DeathModel(game))

        self._init_next()

        if self._model.is_pseudo:
            if self._message is not None:
                self._session.delete_message(self._message)

            self.is_pseudo = True
            return

        if len(self._model.get_cards) == 0:
            self._session.edit_message(self._message, self._model.end(),
                                       reply_markup=kbf.button("Закончить посмертные 10 секунд.", self.end_callback))
            return

    def _init_next(self):
        from GameView import CardView, DayTalkView
        from GameLogic.Models.Cards import UndercoverModel
        self._next = DayTalkView if self.game.course_count % 2 == 0 else (CardView, UndercoverModel)

    def _greeting(self):
        if self.game.gonna_die is None:
            return
        number = self.game[self.game.gonna_die].get_num_str
        self._message = self._session.send_message("Игрок под номером {} умирает.\n"
                                                   "Будет ли использована посмертная карта?".format(number),
                                                   self.cards_keyboard)

    @property
    def cards_keyboard(self):
        cards = self._model.get_cards
        if len(cards) == 0:
            return None

        kb = kbf.empty()
        for card in cards:
            kb += kbf.button(Cards.get_name(card), self.card_callback, card.value)
        kb += kbf.button("Попрощаться с игроком", self.end_callback)
        return kb

    def card_callback(self, bot, update, card_id):
        # TODO AfterDeathCards model needed
        raise NotImplementedError

    def end_callback(self, bot, update):
        self._session.edit_message(self._message, "Игрок под номером {} умирает.\n")
        self._model.end()
        self._session.remove_markup(update)
        self._session.to_next_state()