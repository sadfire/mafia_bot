from GameLogic.Models.DayTalkModel import DayTalkModel
from GameLogic.Views.MainMenuButtons import Buttons as B, get_actions
from GameLogic.Views.Views import IGameView
from KeyboardUtils import KeyboardFactory as kbf, emoji_number


class DayTalkView(IGameView):
    def __init__(self, session, game, next_state, model=None):
        model = DayTalkModel

        self.action_dict = {
            B.WarningCount: [":warning: {}", self.warning_callback],
            B.WarningBan: ("👺", self.ban_callback),
            B.Voting: (":white_circle:", self.to_vote_callback),
            B.NoVoting: (":red_circle:", "empty"),
            B.Card: (':flower_playing_cards:', self.card_button_callback),
            B.NoCard: ('🚬', "empty"),
            B.Clock: (":sound:", self.start_time_callback),
            B.NoClock: (":mute:", "empty"),
            B.Timer: (":timer:", self.timer_callback)
        }
        self.current_player = None
        super().__init__(session, game, next_state, model)

    def _greeting(self):
        self._message = self._session.send_message(text="Главное меню", reply_markup=self.main_kb)

    def update_message(self):
        self._session.edit_message(self._message, text="Главное меню", reply_markup=self.main_kb)

    @property
    def main_kb(self):
        kb = kbf.empty()
        for number in self.game.get_alive_players:
            name = self.game[number].get_num_str + self.game[number].get_role_str
            buttons = get_actions(self.game, number, self.action_dict)
            kb += kbf.action_line((name, "empty", number), *buttons)
        return kb

    def send_confirmation(self, question, action, number_initiator, number_target=None):
        self._session.send_message(text=question.format(emoji_number(number_initiator), number_target),
                                   reply_markup=kbf.confirmation(no_callback=self._session.delete_message_callback,
                                                                 yes_callback=self.to_model,
                                                                 yes_argument=(action.__name__, number_initiator, number_target)))

    def send_ask_card(self, number):
        cards = self._model.get_cards()
        for card in cards:

        self._session.send_message(text="",
                                   reply_markup=)

    def warning_callback(self, bot, update, number):
        self._model.warning(number)
        self.update_message()

    def ban_callback(self, bot, update, number):
        self.send_confirmation("Вы действительно хотите удалить из игры {}?", self._model.kick, number)

    def to_vote_callback(self, bot, update, number):
        self.send_confirmation("Игрок {} выставляет игрока {}?", self._model.to_vote, self.current_player, number)

    def card_button_callback(self, bot, update, number):
        self.send_ask_card(number)

    def timer_callback(self, bot, update):
        pass

    def start_time_callback(self, bot, update, number):
        pass

    def to_model(self, bot, update, action, number_initiator, number_target=None):
        try:
            getattr(self._model, action)(int(number_initiator), int(number_target))
            self.update_message()
        except:
            print("Error in DayTalkView")