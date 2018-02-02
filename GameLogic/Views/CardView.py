from GameLogic.Models.Models import ICardModel
from GameLogic.Views.Views import IGameView
from KeyboardUtils import KeyboardFactory as kbf, emoji_number


class CardView(IGameView):
    def __init__(self, session, game, next_state, model: ICardModel.__class__):
        super().__init__(session, game, next_state, model)
        self._action = model(game)

    def _greeting(self):
        self._session.send_message(text=f"Будет ли использована карта {self._action.get_name}",
                                   reply_markup=kbf.confirmation(self._ask_initiator_callback,
                                                                 self._end_action_callback))

    def _ask_target(self):
        self._session.send_message("Номер цели использования карты",
                                   reply_markup=self.get_alive_players_keyboard(self._init_target_callback))

    def _ask_initiator_callback(self, bot, update):
        self._session.send_message(text="Номер игрока, использующего карту:",
                                   reply_markup=self.get_alive_players_keyboard(self._init_initiator_callback))

    def _init_initiator_callback(self, bot, update, number):
        self._action.init_inititor(number)
        if self._action.is_target_needed:
            self._ask_target()
        else:
            self._end_action_callback(bot, update)

    def _init_target_callback(self, bot, update, number):
        self._action.init_target(number)
        self._end_action_callback(bot, update)

    def get_alive_players_keyboard(self, callback):
        kb = kbf.empty()
        for player in self.game.get_alive():
            kb += kbf.button(emoji_number(player.number), callback, player.num)
        return kb

    def _end_action_callback(self, bot, update):
        self._action.end()
        self._next = self._action.next_state

        self._session.next_state()