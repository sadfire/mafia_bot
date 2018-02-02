from GameLogic.Cards import Cards
from GameLogic.Game import Event
from GameLogic.Models.HealModel import HealModel


class JacketModel(HealModel):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._event = Event.JacketSave

    @property
    def get_card(self):
        return Cards.FlakJacket

    @property
    def get_name(self):
        return super().get_name + " Бронижелет"


