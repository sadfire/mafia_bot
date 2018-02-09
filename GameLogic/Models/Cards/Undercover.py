from GameLogic.Models.ICardModel import ICardModel

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
        from GameView.IntroductionView import IntroductionView
        return IntroductionView, True

