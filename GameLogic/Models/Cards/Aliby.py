from GameLogic import GameInfo
from GameLogic.Models.ICard import ICardModel
from GameView.DayTalkView import DayTalkView


class AlibiModel(ICardModel):
    def get_candidate(self, is_target):
        return self.game.get_alive()

    @property
    def get_card(self):
        from GameLogic.Cards import Cards
        return Cards.Alibi

    @property
    def is_target_needed(self):
        return True

    def final(self) -> type:
        super().final()
        return DayTalkView
