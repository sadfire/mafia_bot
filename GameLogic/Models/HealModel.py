from GameLogic.Cards import Cards
from GameLogic.Game import Event
from GameLogic.Models.Models import ICardModel


class HealModel(ICardModel):
    @property
    def get_card(self):
        return Cards.Heal

    @property
    def get_name(self):
        return super().get_name() + " Лечение"

    @property
    def _get_event(self):
        return Event.Heal

    @property
    def is_target_needed(self):
        return False

    def end(self):
        self._target = self.game.gonna_die
        super().end()
        self.game.gonna_die = None

    @property
    def next_state(self):
        if self.game.gonna_die is not None:
            from GameLogic.Views.CardView import CardView
            from GameLogic.Models.JacketModel import JacketModel
            return CardView, JacketModel

        if self.game.is_day:
            from GameLogic.Views.DayTalkView import DayTalkView
            return DayTalkView
        else:
            from GameLogic.Views.MafiaVotingView import MafiaVotingView
            return MafiaVotingView
