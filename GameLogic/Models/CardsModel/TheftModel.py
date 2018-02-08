from GameLogic.Models.Models import ICardModel
from GameLogic.Views.DayTalkView import DayTalkView


class TheftModel(ICardModel):
    def get_candidate(self, is_target):
        candidate = self.game.get_alive()
        if is_target:
            candidate.remove(self._initiator)
        return candidate

    @property
    def get_card(self):
        from GameLogic.Cards import Cards
        return Cards.Theft

    @property
    def is_target_needed(self):
        return True

    @property
    def next_state(self):
        return DayTalkView

