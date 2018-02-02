from GameLogic.Cards import Cards
from GameLogic.Game import Event
from GameLogic.Models.Models import ICardModel


class HealModel(ICardModel):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._target = game.gonna_die
        self._event = Event.Heal

    def get_candidate(self, is_target):
        candidate = list(self.game.get_alive_players)
        if not is_target:
            candidate.remove(self.game.gonna_die)
        return candidate

    @property
    def target(self):
        return self._target

    @property
    def get_card(self):
        return Cards.Heal

    @property
    def get_name(self):
        return super().get_name + " Лечение"

    @property
    def is_target_needed(self):
        return False

    def end(self):
        if self._initiator is None:
            if Cards.FlakJacket in self.game.wasted_cards:
                self.game.kill()
                return "Игрок {} умер"
            return ""

        super().end()
        self.game.gonna_die = None
        return "Игрок {} выжил"

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
