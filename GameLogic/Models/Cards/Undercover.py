from GameLogic import GameInfo
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
        from GameView import CardView
        from GameLogic.Models.Cards import ChangeRoleModel

        return CardView, ChangeRoleModel

    def end(self):
        super().end()
        if self._initiator is not None:
            self.game[self._initiator][GameInfo.IsNotHidden] = False
