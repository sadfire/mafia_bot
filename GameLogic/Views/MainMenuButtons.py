from enum import Enum

from GameLogic.Member import GameInfo as GI


class Buttons(Enum):
    WarningCount = 1,
    WarningBan = 2,
    Voting = 3,
    NoVoting = 4,
    Card = 5,
    NoCard = 6,
    Clock = 7,
    NoClock = 8,
    Timer = 9
    ActiveTime = 10


def get_actions(game, number: int, action_dict: dict) -> tuple:
    if game[number][GI.Warnings] == 3:
        warning_button = action_dict[Buttons.WarningBan]
    else:
        warning_button = action_dict[Buttons.WarningCount]
        warning_button[0] = warning_button[0].format(game[number][GI.Warnings])

    if number in game.candidates:
        vote_button = action_dict[Buttons.NoVoting]
    else:
        vote_button = action_dict[Buttons.Voting]

    if game[number][GI.IsCardSpent]:
        card_button = action_dict[Buttons.NoCard]
    else:
        card_button = action_dict[Buttons.Card]

    if game[number][GI.IsTalked]:
        talk_button = action_dict[Buttons.Clock]
    else:
        talk_button = action_dict[Buttons.NoClock]

    if game[number][GI.IsTimer]:
        timer

    return warning_button, vote_button, card_button, talk_button