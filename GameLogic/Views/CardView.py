from GameLogic.Models.Models import ICardModel
from GameLogic.Views.Views import IGameView
from KeyboardUtils import KeyboardFactory as kbf, emoji_number


class CardView(IGameView):
    def __init__(self, session, game, next_state, model: ICardModel.__class__):
        self._model = model(game)
        super().__init__(session, game, next_state, self._model)

    def _greeting(self):
        self._session.send_message(text=f"Будет ли использована карта {self._model.get_name}",
                                   reply_markup=kbf.confirmation(self._ask_initiator_callback,
                                                                 self._end_action_callback))

    def _ask_target(self):
        self._session.send_message("Номер цели использования карты",
                                   reply_markup=self.get_alive_players_keyboard(self._init_target_callback))

    def _ask_initiator_callback(self, bot, update):
        self._session.send_message(text="Номер игрока, использующего карту:",
                                   reply_markup=self.get_alive_players_keyboard(self._init_initiator_callback))

    def _init_initiator_callback(self, bot, update, number):
        number = int(number)
        self._session.edit_message(message=update.effective_message,
                                   text="Карту {} использует игрок {}"
                                   .format(self._model.get_name, self.game[number].get_num_str))
        self._model.init_initiator(number)
        if self._model.is_target_needed:
            self._ask_target()
        else:
            self._end_action_callback(bot, update)

    def _init_target_callback(self, bot, update, number):
        number = int(number)
        self._session.edit_message(message=update.effective_message,
                                   text="На игрока {}"
                                   .format(self.game[number].get_num_str))

        self._model.init_target(number)
        self._end_action_callback(bot, update)

    def get_alive_players_keyboard(self, callback):
        kb = kbf.empty()
        for number in self.game.get_alive_players:
            kb += kbf.button(self.game[number].get_num_str, callback, number)
        return kb

    def _end_action_callback(self, bot, update):
        self._model.end()
        self._next = self._model.next_state

        self._session.to_next_state()