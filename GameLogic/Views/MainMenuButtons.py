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
    Immunitet = 11


def get_actions(game, number: int, action_dict: dict, timer_deque) -> tuple:
    if game[number][GI.Warnings] == 3:
        warning_button = action_dict[Buttons.WarningBan]
    else:
        warning_button = list(action_dict[Buttons.WarningCount])
        warning_button[0] = warning_button[0].format(game[number][GI.Warnings])

    if game[number][GI.IsImmunitet]:
        vote_button = action_dict[Buttons.Immunitet]
    elif number in game.candidates:
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
        timer_button = list(action_dict[Buttons.ActiveTime])
        if number in timer_deque:
            count = timer_deque.index(number) + 1
        else:
            count = 0
        timer_button[0] = timer_button[0].format(count)
    else:
        timer_button = action_dict[Buttons.Timer]

    return warning_button, vote_button, card_button, timer_button, talk_button