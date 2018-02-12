from emoji import emojize

from GameLogic.Cards import Cards
from GameLogic.GameEvents import Event
from GameLogic.Models import ICardModel


class JacketModel(ICardModel):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._event = Event.JacketSave
        self.init_initiator(self.game.gonna_die)

    def get_candidate(self, is_target) -> list:
        return [self.game.gonna_die]

    @property
    def is_wasted(self):
        return self.game.gonna_die is None or super().is_wasted

    @property
    def is_initiator_needed(self):
        return False

    @property
    def is_target_needed(self):
        return True

    def init_target(self, number=None):
        if number is None:
            self._target = self._initiator
        else:
            self._target = number

    def init_initiator(self, number):
        self._initiator = number

    @property
    def get_card(self):
        return Cards.FlakJacket

    @property
    def next_state(self):
        from GameView.DeathView import DeathView
        return DeathView

    def end(self):
        return super().end()
