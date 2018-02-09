from GameLogic.Models.ICardModel import ICardModel
from GameView.DayTalkView import DayTalkView
from GameView.IntroductionView import IntroductionView


class UndercoverModel(ICardModel):
    def get_candidate(self, is_target):
        return self.game.get_alive()

    @property
    def is_target_needed(self):
        return False

    @property
    def get_card(self):
        from GameLogic.Cards import Cards
        return Cards.Undercover

    @property
    def next_state(self):
        return IntroductionView, True

