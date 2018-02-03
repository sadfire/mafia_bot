from GameLogic.Cards import Cards
from GameLogic.Models.DayTalkModel import DayTalkModel
from GameLogic.Views.MainMenuButtons import Buttons as B, get_actions
from GameLogic.Views.Views import IGameView
from KeyboardUtils import KeyboardFactory as kbf, emoji_number


class DayTalkView(IGameView):
    def __init__(self, session, game, next_state, model=None):
        model = DayTalkModel(game)

        self.timer_deque = []

        self.action_dict = {
            B.WarningCount: [":warning: {}", self.warning_callback],
            B.WarningBan: ("👺", self.ban_callback),
            B.Voting: (":white_circle:", self.to_vote_callback),
            B.NoVoting: (":red_circle:", "empty"),
            B.Card: (':flower_playing_cards:', self.card_button_callback),
            B.NoCard: ('🚬', "empty"),
            B.Clock: ("🔉", self.start_time_callback),
            B.NoClock: ("🔇", "empty"),
            B.Timer: ("⏲", self.timer_callback),
            B.ActiveTime: ["⏲ {}", "empty"]
        }
        self.current_player = None
        super().__init__(session, game, next_state, model)

    def _greeting(self):
        self._message = self._session.send_message(text="Главное меню", reply_markup=self.main_kb())

    def update_message(self) -> None:
        self._session.edit_message(self._message, text="Главное меню", reply_markup=self.main_kb())

    def main_kb(self):
        kb = kbf.empty()
        for number in self.game.get_alive_players:
            name = self.game[number].get_num_str + self.game[number].get_role_str
            buttons = get_actions(self.game, number, self.action_dict, self.timer_deque)
            kb += kbf.action_line((name, "empty", number), *buttons)
        return kb

    def send_confirmation(self, question, action, number_initiator, number_target=None):
        self._session.send_message(text=question.format(emoji_number(number_initiator), number_target),
                                   reply_markup=kbf.confirmation(no_callback=self._session.delete_message_callback,
                                                                 yes_callback=self.to_model,
                                                                 yes_argument=(
                                                                 action.__name__, number_initiator, number_target)))

    def send_ask_card(self, number):
        kb = kbf.empty()
        for card in self._model.get_cards():
            kb += kbf.button(Cards.get_name(card), self.ask_target, (number, card.value))

        self._session.send_message(text="Выберите карту.", reply_markup=kb)

    def warning_callback(self, bot, update, number):
        self._model.warning(number=int(number))
        self.update_message()

    def ban_callback(self, bot, update, number):
        self.send_confirmation("Вы действительно хотите удалить из игры {}?", self._model.kick, number)

    def to_vote_callback(self, bot, update, number):
        self.send_confirmation("Игрок {} выставляет игрока {}?", self._model.to_vote, self.current_player, number)

    def card_button_callback(self, bot, update, number):
        self.send_ask_card(number)

    def timer_callback(self, bot, update, number):
        self.timer_deque.append(number)
        self._model.timer_on(number)

    def start_time_callback(self, bot, update, number):
        pass

    def to_model(self, bot, update, action, number_initiator, number_target=None):
        try:
            getattr(self._model, action)(int(number_initiator), int(number_target))
            self.update_message()
        except:
            print("Error in DayTalkView")

    def ask_target(self, bot, update, number, card_id):
        if self._model.is_target_needed(card_id):
            kb = kbf.empty()
            for target in self.game.get_alive_players:
                kb += kbf.button(self.game[target].get_num_str(), self.card_process, (number, target, card_id))

            self._session.send_message(text="На кого применяется карта?",
                                       reply_markup=kb)
        else:
            self._model.process_card(initiator=number,
                                     card_id=card_id)
            self.update_message()

    def card_process(self, bot, update, initiator, target, card_id):
        self._model.process_card(initiator=initiator,
                                 target=target,
                                 card_id=card_id)

        self.update_message()
