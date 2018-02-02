from GameLogic.Cards import Cards
from GameLogic.Game import Event
from GameLogic.Models.HealModel import HealModel


class JacketModel(HealModel):
    @property
    def get_card(self):
        return Cards.FlakJacket

    @property
    def get_name(self):
        return super().get_name() + " Бронижелет"

    @property
    def _get_event(self):
        return Event.JacketSave

