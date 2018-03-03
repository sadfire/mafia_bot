from GameLogic.Models import ICardModel


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

    def final(self):
        super().final()
        from GameView.DayTalkView import DayTalkView
        return DayTalkView
