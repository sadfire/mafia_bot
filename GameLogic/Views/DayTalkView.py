from enum import Enum
from threading import Timer

from emoji import emojize

from GameLogic.Cards import Cards
from GameLogic.Member import GameInfo
from GameLogic.Models.DayTalkModel import DayTalkModel
from GameLogic.Models.HealModel import HealModel
from GameLogic.Views.CardView import CardView
from GameLogic.Views.MainMenuButtons import Buttons as B, get_actions
from GameLogic.Views.Views import IGameView
from KeyboardUtils import KeyboardFactory as kbf, emoji_number


class TalkState(Enum):
    Pause = 0
    Play = 1
    Stop = 2


class DayTalkView(IGameView):
    def __init__(self, session, game, next_state, model=None):
        self.timer = None
        model = DayTalkModel(game)
        self.card_message = None
        self._timer_message = None
        self.timer_deque = []
        self.talk_state = TalkState.Pause
        self.talk_time = 60
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
            B.Immunitet: ("🤞", "empty"),
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
        if self._model.is_all_talks:
            kb += kbf.button("Перейти к голосованию", self.end_for_vote_callback)
        return kb

    def send_confirmation(self, question, action, number_initiator, number_target=None):
        argument = (action.__name__, str(number_initiator), str(number_target))
        self._session.send_message(text=question.format(emoji_number(number_initiator), emoji_number(number_target)),
                                   reply_markup=kbf.confirmation(no_callback=self._session.delete_message_callback,
                                                                 yes_callback=self.to_model,
                                                                 yes_argument=argument))

    def send_ask_card(self, number):
        kb = kbf.empty()
        for card in self._model.get_cards():
            kb += kbf.button(Cards.get_name(card), self.ask_target, (str(number), str(card.value)))

        self.card_message = self._session.send_message(text="Выберите карту.", reply_markup=kb + kbf.close_button())

    def warning_callback(self, bot, update, number):
        self._model.warning(number=int(number))
        self.update_message()

    def ban_callback(self, bot, update, number):
        self.send_confirmation("Вы действительно хотите удалить из игры {}?", self._model.kick, number)

    def to_vote_callback(self, bot, update, number):
        if self.current_player is not None:
            self.send_confirmation("Игрок {} выставляет игрока {}?", self._model.to_vote, self.current_player, number)

    def card_button_callback(self, bot, update, number):
        self.send_ask_card(number)

    def timer_callback(self, bot, update, number):
        number = int(number)
        self.timer_deque.append(number)
        self._model.timer_on(number)
        self.update_message()

    def start_time_callback(self, bot, update, number):
        if self.current_player is not None:
            return

        number = int(number)
        self.current_player = number
        if self._model.is_can_talk(number):
            self.send_timer_message(number)
        else:
            self._session.send_message("Нельзя начать минуту этого игрока.", reply_markup=kbf.close_button())

    def to_model(self, bot, update, args):
        action = args[0]
        number_initiator = int(args[1])
        if len(args) > 2:
            number_target = int(args[2])
        else:
            number_target = None

        result = getattr(self._model, action)(int(number_initiator), int(number_target))
        self.update_message()
        self._session.edit_message(update.effective_message, result)

    def ask_target(self, bot, update, args):
        initiator, card_id = args
        initiator = int(initiator)
        card_id = int(card_id)
        if card_id is Cards.Undercover.value:
            self.card_process(bot, update, (initiator, initiator, card_id))
            return

        kb = kbf.empty()
        candidates = self.game.get_alive_players
        if card_id is Cards.Theft.value:
            candidates = [candidate for candidate in candidates if not self.game[candidate][GameInfo.IsCardSpent] and candidates != initiator]

        for target in candidates:
            kb += kbf.button(self.game[target].get_num_str, self.card_process, (initiator, target, card_id))
        self._session.edit_message(message=update.effective_message,
                                   text="На кого применяется карта?",
                                   reply_markup=kb + kbf.close_button())

    def card_process(self, bot, update, args):
        initiator, target, card_id = args
        initiator = int(initiator)
        target = int(target)
        card_id = int(card_id)

        self._model.process_card(initiator=initiator,
                                 target=target,
                                 card_id=card_id)

        self._session.delete_message_callback(bot, update)
        self.update_message()

    def send_timer_message(self, number):
        self.current_player = number
        self.talk_state = TalkState.Pause
        self._timer_message = self._session.send_message("Минута игрока {}.\nОсталось {} секунд.")
        self.talk_time = 60
        self.timer_message_change(number=number)

    def timer_message_change(self, bot=None, update=None, number=None):
        if self.current_player != number:
            return

        if self.talk_state is TalkState.Play:
            self.talk_time -= 5

        number = int(number)
        if self.talk_time == 0:
            self.talk_state = TalkState.Stop
            self._session.edit_message(message=self._timer_message, text="Минута {} закончилась".format(self.game[number].get_num_str))
            self.current_player = None
            self.game[number][GameInfo.IsTalked] = False
            self.update_message()
            self._timer_message = None
            self.timer = None
            return

        self.timer_message_update(number)

        if self.timer is not None:
            self.timer = Timer(5.0, self.timer_message_change, (None, None, number))
            self.timer.start()

    def timer_message_update(self, number: int):
        kb = kbf.action_line(("▶️", self.play_callback, number) if self.talk_state is TalkState.Pause else (
            "⏸", self.pause_callback, number),
                             ("⏹", self.stop_callback, number))
        self._session.edit_message(message=self._timer_message,
                                   text="Минута игрока {}.\nОсталось {} секунд.".format(
                                       self.game[number].get_num_str,
                                       self.talk_time),
                                   reply_markup=kb)

    def pause_callback(self, bot, update, number):
        self.timer.cancel()
        self.talk_state = TalkState.Pause
        self.timer_message_update(number=int(number))

    def play_callback(self, bot=None, update=None, number=None):
        try:
            number = int(number)
            self.talk_state = TalkState.Play
            self.timer_message_update(number)
            self.timer = Timer(5.0, self.timer_message_change, (None, None, number))
            self.timer.start()
        except RuntimeError:
            pass

    def stop_callback(self, bot, update, number):
        number = int(number)
        if self.timer is not None:
            self.timer.cancel()

        self.talk_state = TalkState.Stop
        self.talk_time = 0
        self.timer_message_change(bot, update, number)

        if self.card_message is not None:
            self._session.delete_message(self.card_message)
            self.card_message = None


    def end_for_vote_callback(self, bot, update):
        if len(self.game.candidates) == 0:
            from GameLogic.Views.MafiaVotingView import MafiaVotingView
            self._next = MafiaVotingView
            self._session.to_next_state()
            return

        kb = kbf.empty()
        for number in self.game.candidates:
            kb += kbf.button("Убивают игрока номер{}".format(self.game[number].get_num_str), self.kill_callback, number)
        self._session.send_message(text="На голование выставлены", reply_markup=kb)

    def kill_callback(self, bot, update, number):
        number = int(number)
        self._model.kill(number)

        self._next = CardView, HealModel
        self._session.to_next_state()