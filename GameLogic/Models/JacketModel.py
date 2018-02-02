from emoji import emojize

from GameLogic.Cards import Cards
from GameLogic.Game import Event
from GameLogic.Models.HealModel import HealModel


class JacketModel(HealModel):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._event = Event.JacketSave
        self.init_initiator(self.game.gonna_die)
        self.init_target(self.game.gonna_die)

    @property
    def is_initiator_needed(self):
        return False
    
    @property
    def get_card(self):
        return Cards.FlakJacket

    @property
    def get_name(self):
        return emojize(':flower_playing_cards:') + " Бронижелет"
