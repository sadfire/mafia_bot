from GameLogic import GameInfo
from GameLogic.Models import ICardModel

from GameView import IGameView
from Utils import kbf


class CardView(IGameView):
    def __init__(self, session, game, model=None, is_greeting=True):

        self._model = model(game)
        self.is_pseudo = self._model.is_wasted

        super().__init__(session=session, game=game, model=self._model, is_greeting=not self.is_pseudo)

    @property
    def _next(self):
        if self._next_state is None:
            return self._model.final()
        return super()._next

    def _greeting(self):
        text = f"Будет ли использована {self._model.get_name}"

        if self._model.target is not None:
            text += f", на игрока {self.game[self._model.target].get_num_str}"

        self._message = self._session.send_message(text=text+"?",
                                                   reply_markup=kbf.confirmation(self._ask_initiator_callback,
                                                                                 self._end_action_callback))

    def _ask_target(self):
        if self._model.is_target_needed:
            self._session.send_message(self._model.get_target_question,
                                       reply_markup=self.get_alive_players_keyboard(callback=self._init_target_callback,
                                                                                    is_target=True))
        else:
            self._end_action_callback(None, None)

    def _ask_initiator_callback(self, bot, update):
        self._model.initiator_ask = True
        if self._model.is_initiator_needed:
            self._session.edit_message(message=update,
                                       text=self._model.get_initiator_question,
                                       reply_markup=self.get_alive_players_keyboard(callback=self._init_initiator_callback,
                                                                                    is_target=False))
        else:
            self._ask_target()

    def _init_initiator_callback(self, bot, update, number):
        number = int(number)
        self._session.edit_message(message=update,
                                   text="Карту {} использует игрок {}"
                                   .format(self._model.get_name, self.game[number].get_num_str))

        self._model.init_initiator(number)
        if self._model.is_target_needed:
            self._ask_target()
        else:
            self._model.init_target()
            self._end_action_callback(bot, update)

    def _init_target_callback(self, bot, update, number):
        number = int(number)
        if self._model.is_target_message_needed:
            self._session.edit_message(message=update.effective_message,
                                       text="На игрока {}"
                                       .format(self.game[number].get_num_str))
        else:
            self._session.delete_message(message=update.effective_message)

        self._model.init_target(number)
        self._end_action_callback(bot, update)

    def get_alive_players_keyboard(self, callback, is_target):
        kb = kbf.button("Отменить", "empty")
        for number in self._model.get_candidate(is_target):
            if is_target or self.game.is_player_card_closed(number):
                kb += kbf.button(self.game[number].get_num_str, callback, number)

        return kb

    def _end_action_callback(self, bot, update):
        self._next_state = self._model.final()

        end_result = self._model.end_message
        if end_result is None or end_result == "":
            self._session.delete_message(self._message)

        else:
            if "{}" in end_result:
                end_result = end_result.format(self.game[self._model.target].get_num_str)
            self._session.edit_message(self._message, end_result)

        self._session.to_next_state()
