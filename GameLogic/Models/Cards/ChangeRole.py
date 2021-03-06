from GameLogic import Cards, Event, GameInfo as GI
from GameLogic.Models.ICard import ICardModel


class ChangeRoleModel(ICardModel):
    def __init__(self, game) -> None:
        super().__init__(game)

    @property
    def is_wasted(self):
        return super().is_wasted or self.game.course_count != 0

    @property
    def get_card(self):
        return Cards.ChangeRole

    def get_candidate(self, is_target):
        if is_target:
            candidate = self.game.get_alive()
            candidate.remove(self._initiator)
            return candidate

        return self.game.get_alive(is_card_closed=True)

    @property
    def is_target_needed(self):
        return True

    def final(self):
        from GameView.IntroductionView import IntroductionView
        if super().final():
            self.end_message = "Обмен произошел"

        return IntroductionView, True


