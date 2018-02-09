from GameLogic.Models.ICardModel import ICardModel
from GameView.DayTalkView import DayTalkView


class AlibyModel(ICardModel):
    def get_candidate(self, is_target):
        return self.game.get_alive()

    @property
    def get_card(self):
        from GameLogic.Cards import Cards
        return Cards.Alibi

    @property
    def is_target_needed(self):
        return True

    @property
    def next_state(self):
        return DayTalkView

