from GameLogic import Cards, GSP
from GameLogic.Models import ICardModel
from GameLogic.Models.Cards import HealModel


class HarakiriModel(HealModel):
    @property
    def get_card(self):
        return Cards.Harakiri

    def final(self):
        if super(ICardModel).final():
            return GSP.Death(self.game)
        else:
            return GSP.DeathOut(self.game)

