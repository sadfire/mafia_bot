from enum import Enum

from GameLogic import Cards

from GameLogic.Models import DayTalkModel

from GameView import CivilianVotingView, Buttons as B, get_actions, Messages as M, IGameView
from GameView.TimerMessageHandler import TimerMessageHandler

from Utils.KeyboardUtils import KeyboardFactory as kbf, emoji_number


class TalkState(Enum):
    Pause = 0
    Play = 1
    Stop = 2


class DayTalkView(IGameView):
    def __init__(self, session, game, next_state, model=None):
        self._messages = {M.Main: None,
                          M.Timer: None,
                          M.Vote: None,
                          M.Card: None}

        self.timer = None
        self.action_dict = \
            {
                B.WarningCount: [":warning: {}", self.warning_callback],
                B.WarningBan: ("👺", self.ban_callback),
                B.Voting: (":white_circle:", self.to_vote_callback),
                B.NoVoting: (":red_circle:", "empty"),
                B.Card: (':flower_playing_cards:', self.card_button_callback),
                B.NoCard: ('🚬', "empty"),
                B.Clock: ("🔉", self.start_clock_button_callback),
                B.NoClock: ("🔇", "empty"),
                B.Timer: ("⏲", self.timer_callback),
                B.Immunitet: ("🤞", "empty"),
                B.ActiveTime: ["⏲ {}", "empty"],
                B.Aliby: ("👯", "empty"),
                B.Ghost: ("👻", "empty"),
                B.Leader: ("🤴🏼", "empty"),
                B.Undercover: ("💂🏼", "empty")
            }

        self.current_player = None
        self.timer_handler = None
        super().__init__(session, game, next_state, DayTalkModel(game))

    def _greeting(self):
        self._messages[M.Main] = self._session.send_message(text="Главное меню")
        self.update_message()

    def update_message(self) -> None:
        self._session.edit_message(self._messages[M.Main], text="Главное меню", reply_markup=self.main_kb())

    def pause_message(self) -> None:
        self._session.edit_message(self._messages[M.Main], text="Пауза")

    def main_kb(self):
        kb = kbf.empty()

        for number in self.game.get_alive():
            name = self.game[number].get_num_str + self.game[number].get_role_str
            buttons = get_actions(self.game, number, self.action_dict, self._model.additional_time)

            kb += kbf.action_line((name, self._session.send_player_info_callback, number), *buttons)

        if self._model.is_day_can_end:
            kb += kbf.button("Перейти к голосованию", self.end_for_vote_callback)

        return kb

    def send_confirmation(self, question, action, number_initiator, number_target=None):

        arguments = (action.__name__, str(number_initiator), str(number_target))

        question_text = question.format(emoji_number(number_initiator), emoji_number(number_target))

        self._session.send_message(text=question_text,
                                   reply_markup=kbf.confirmation(yes_callback=self.transfer_to_models,
                                                                 yes_argument=arguments,
                                                                 no_callback=self._session.delete_message_callback))

    def cancel_ask_card_callback(self, bot, update):
        self.update_message()
        self._session.delete_message_callback(bot, update)
        self._messages[M.Card] = None

    def warning_callback(self, bot, update, number):
        self._model.warning(number=int(number))
        self.update_message()

    def ban_callback(self, bot, update, number):
        self.send_confirmation("Вы действительно хотите удалить из игры {}?", self._model.kick, number)

    def to_vote_callback(self, bot, update, number):
        if self.current_player is not None:
            self.send_confirmation("Игрок {} выставляет игрока {}?", self._model.to_vote, self.current_player, number)

    def card_button_callback(self, bot, update, number):
        kb = kbf.empty()
        for card in self._model.get_possible_cards(True):
            kb += kbf.button(Cards.get_name(card), self.to_card_state, (number, card.value))
        self._session.send_message(text="Вы хотите применять карту?",
                                   reply_markup=kb + kbf.close_button())

    def to_card_state(self, bot, update, args):
        self._session.delete_message(self._messages[M.Main])
        card, number_initiator = args
        card = Cards(card)

        self.game.current_player = number_initiator

        if card is Cards.Alibi:
            from GameLogic.Models.Cards import AlibyModel
            self._next = AlibyModel
        elif card is Cards.Theft:
            from GameLogic.Models.Cards import TheftModel
            self._next = TheftModel
        elif card is Cards.Undercover:
            from GameLogic.Models.Cards import UndercoverModel
            self._next = UndercoverModel

        from GameView import CardView
        self._next = CardView, self._next
        self._session.to_next_state()

    def timer_callback(self, bot, update, number):
        number = int(number)
        self._model.additional_time.append(number)
        self.update_message()

    def transfer_to_models(self, bot, update, args):
        action = args[0]
        number_initiator = int(args[1])
        if len(args) > 2:
            number_target = int(args[2])
        else:
            number_target = None

        result = getattr(self._model, action)(int(number_initiator), int(number_target))
        self.update_message()
        self._session.edit_message(update.effective_message, result)

    def end_for_vote_callback(self, bot, update):
        if len(self.game.candidates) == 0:
            self._session.edit_message(self._messages[M.Main], "Никто не выставлен")
            from GameLogic.Models.Cards import UndercoverModel
            self._next = CardView, UndercoverModel
        else:
            self._session.edit_message(self._messages[M.Main],
                                       "Выставлены:\n\n".format("\n".join(self.game.candidates)))
            self._next = CivilianVotingView

        return self._session.to_next_state()

    def kill_callback(self, bot, update, number):
        number = int(number)
        self._model.try_kill(number)

        from GameLogic.Models.Cards import HealModel
        from GameView import CardView
        
        self._next = CardView, HealModel
        self._session.to_next_state()

    def start_clock_button_callback(self, bot, update, number):
        if self.current_player is not None:
            return
        self.current_player = number
        self.timer_handler = TimerMessageHandler(self._session, self.game[number], self._player_clock_callback, self._stop_clock_callback)

    def _player_clock_callback(self, bot, update, action):
        self.timer_handler.callback(action)

    def _stop_clock_callback(self, number):
        self.current_player = None
        self._model.ban_talk(number)
        self.timer_handler = None
        self.update_message()

