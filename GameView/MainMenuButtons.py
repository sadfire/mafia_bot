from enum import Enum

from GameLogic import Cards
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
    Aliby = 12
    Ghost = 13
    Leader = 14
    Undercover = 15


class Messages(Enum):
    Main = 0,
    Timer = 1,
    Vote = 2,
    Question = 3
    Card = 4


def get_actions(game, number: int, action_dict: dict, timer_deque) -> tuple:
    warning_button = get_warning_button(action_dict, game, number)

    vote_button = get_vote_button(action_dict, game, number)

    card_button = get_card_button(action_dict, game, number)

    talk_button = get_clock_button(action_dict, game, number)

    timer_button = get_timer_button(action_dict, number, timer_deque)

    return warning_button, vote_button, card_button, timer_button, talk_button


def get_timer_button(action_dict, number, timer_deque):
    if number in timer_deque:
        timer_button = list(action_dict[Buttons.ActiveTime])
        if number in timer_deque:
            count = timer_deque.index(number) + 1
        else:
            count = 0
        timer_button[0] = timer_button[0].format(count)
    else:
        timer_button = action_dict[Buttons.Timer]
    return timer_button


def get_clock_button(action_dict, game, number):
    if game[number][GI.IsNotTalked]:
        talk_button = action_dict[Buttons.Clock]
    else:
        talk_button = action_dict[Buttons.NoClock]
    return talk_button


def get_card_button(action_dict, game, number):
    card = game[number][GI.Card]
    if card is not None and game.cards[card]:

        if game[number][GI.Card] is Cards.Leader:
            card_button = action_dict[Buttons.Leader]
        elif game[number][GI.Card] is Cards.Undercover:
            card_button = action_dict[Buttons.Undercover]
        elif game[number][GI.Card] is Cards.Ghost:
            card_button = action_dict[Buttons.Ghost]
        else:
            card_button = action_dict[Buttons.NoCard]

    else:
        card_button = action_dict[Buttons.Card]
    return card_button


def get_vote_button(action_dict, game, number):
    if not game[number][GI.IsNotImmunity]:
        vote_button = action_dict[Buttons.Immunitet]
    elif number in game.candidates:
        vote_button = action_dict[Buttons.NoVoting]
    else:
        vote_button = action_dict[Buttons.Voting]
    return vote_button


def get_warning_button(action_dict, game, number):
    if game[number][GI.Warnings] == 3:
        warning_button = action_dict[Buttons.WarningBan]
    else:
        warning_button = list(action_dict[Buttons.WarningCount])
        warning_button[0] = warning_button[0].format(game[number][GI.Warnings])
    return warning_button
