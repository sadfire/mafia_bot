from GameLogic import Cards, Event, GameInfo as GI
from GameLogic.Models.ICardModel import ICardModel


class ChangeRoleModel(ICardModel):
    def __init__(self, game) -> None:
        super().__init__(game)

    @property
    def is_wasted(self):
        return self.game.day_count != 0

    @property
    def next_state(self):
        from GameView.IntroductionView import IntroductionView
        return IntroductionView, True

    @property
    def get_card(self):
        return Cards.ChangeRole

    def get_candidate(self, is_target):
        return self.game.get_alive()

    @property
    def is_target_needed(self):
        return True

    def end(self):
        return "Обмен ролями состоялся" if super().end() else None

