from enum import Enum

from GameLogic.Member import GameInfo as GI
from GameLogic.Models.DayTalkModel import DayTalkModel
from GameLogic.Views.Views import IGameView
from KeyboardUtils import KeyboardFactory as kbf, emoji_number as emn


class Buttons(Enum):
    WarningCount = 1,
    WarningBan = 2,
    Voting = 3,
    NoVoting = 4,
    Card = 5,
    NoCard = 6,
    Clock = 7,
    NoClock = 8


def get_actions(game, number: int, action_dict: dict) -> tuple:
    if game[number][GI.Warnings] == 3:
        warning_button = action_dict[Buttons.WarningBan]
    else:
        warning_button = action_dict[Buttons.WarningCount]
        warning_button[0].format(game[number][GI.Warnings])

    if number in game.candidates:
        vote_button = action_dict[Buttons.NoVoting]
    else:
        vote_button = action_dict[Buttons.Voting]

    if game[number][GI.IsCardSpent]:
        card_button = action_dict[Buttons.NoCard]
    else:
        card_button = action_dict[Buttons.Card]

    if game[number][GI.IsTalked]:
        talk_button = action_dict[Buttons.NoClock]
    else:
        talk_button = action_dict[Buttons.Clock]

    return warning_button, vote_button, card_button, talk_button


class DayTalkView(IGameView):
    def __init__(self, session, game, next_state, model=None):
        model = DayTalkModel

        self.action_dict = {
            Buttons.WarningCount: [":warning: {}", self.warning_callback],
            Buttons.WarningBan: ("👺", self.ban_callback),
            Buttons.Voting: (":white_circle:", self.to_vote_callback),
            Buttons.NoVoting: (":red_circle:", self.on_vote_callback),
            Buttons.Card: (':flower_playing_cards:', self.card_button_callback),
            Buttons.NoCard: ('🚬', "empty"),
            Buttons.Clock: (":sound:", self.start_time_callback),
            Buttons.NoClock: (":mute:", "empty")
        }

        super().__init__(session, game, next_state, model)

    def _greeting(self):
        self._message = self._session.send_message(text="Главное меню", reply_markup=self.main_kb)

    @property
    def main_kb(self):
        kb = kbf.empty()
        for number in self.game.get_alive_players:
            name = self.game[number].get_num_str + self.game[number].get_role_str
            buttons = get_actions(self.game, number, self.action_dict)
            kb += kbf.action_line((name, "empty", number), *buttons)
        return kb

    def warning_callback(self, bot, update):
        pass

    def ban_callback(self, bot, update):
        pass

    def to_vote_callback(self, bot, update):
        pass

    def on_vote_callback(self, bot, update):
        pass

    def card_button_callback(self, bot, update):
        pass

    def start_time_callback(self, bot, update):
        pass
