from GameLogic.Cards import Cards
from GameLogic.GameEvents import Event
from GameLogic.Member import GameInfo as GI
from GameLogic.Models.ICardModel import ICardModel
from GameView.DayTalkView import DayTalkView


class ListenerModel(ICardModel):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._event = Event.SuccessListen, Event.FailedListen

    @property
    def next_state(self):
        return DayTalkView

    @property
    def get_card(self):
        return Cards.Retirement

    @property
    def get_name(self):
        return super().get_name + 'Прослушка'

    def get_candidate(self, is_target):
        return self.game.get_alive_players

    @property
    def is_target_needed(self):
        return True

    def end(self):
        if self._target is not None:
            self.game[self._initiator][GI.IsCardSpent] = True
            self.game.wasted_cards.append(Cards.Retirement)
            
            return "Игрок услышал " + self.game[self._target].get_role_str
        return None

